# %%
import pandas as pd
import numpy as np
import requests
from io import StringIO
from datetime import date, datetime, timedelta
from detector_info_settings.detector_format_settings import detector_settings
from database import connect_to_db, connect_to_db_upload, format_sql
from os import listdir
import os
from sqlalchemy import text
import glob
import warnings

# %%
pd.options.mode.chained_assignment = None
warnings.simplefilter(action='ignore', category=FutureWarning)

# %% [markdown]
# # Formatting and download functions

# %% [markdown]
# ## format_name

# %%
def format_name(detector_name_og):
    ''' 
    Creates formatted string for access to detector db info and others

    Args:       detector_name_og  -> str
    Returns:    str

    '''
    print('format_name fn')
    # Get current data table from db
    detector_name = detector_name_og.lower()

    # Format detector name to lowercase and check formatting of name 
    # doesn't have number up front
    detector_name = detector_name_og.lower()
    if detector_name.startswith('2') or detector_name.startswith('4'):
        detector_name = detector_name[1:]+detector_name[0]
        
    return detector_name

# %% [markdown]
# ## get_detector_data

# %%
def get_detector_data(detector_name):
    ''' 
    Connects to db and downloads data for specified detector

    Args:       detector_name       -> str containing detector name for access to settings
    Returns:    pandas df

    '''
    print('get detector data fn')
    db = connect_to_db()

    with db.connect() as conn:
        query = text(f'SELECT * FROM {detector_name}')
        result = conn.execute(query)
        counts_data = result.fetchall()
        conn.close()
        db.dispose()

        # Format data into pandas df
        df = format_sql(counts_data)
        
    return df

# %% [markdown]
# ## get_weather_data

# %%
def get_weather_data(station_id):
    ''' 
    Connects to db and downloads data for specified weather station

    Args:       station_id      -> str containing detector name for access to settings
    Returns:    pandas df

    '''
    print('get_weather_data fn')
    # Connect to db via sqlalchemy
    db = connect_to_db()
        
    with db.connect() as conn:
        #Query
        query = text(f'SELECT * FROM {station_id}')
        result = conn.execute(query)
        weather_data = result.fetchall()
        conn.close()
        db.dispose()
        
        # Format data
        wdf = format_sql(weather_data)

        # Format index to allow for querying via datetime format and avoid compatibility issues
        if str(wdf.index.tz) != 'UTC':
            wdf.index = wdf.index.tz_localize('UTC')
    
    return wdf

# %% [markdown]
# # Weather data processing functions

# %% [markdown]
# ## fetch_weather

# %%
def fetch_weather(my_station, enddt, startdt):
    ''' 
    Downloads specified station's data from Iowa State University's website

    Args:       my_station      -> str with station id name
                enddt           -> str with datetime index for latest known recorded weather data on site
                startdt         -> str with datetime index for the last known recorded data on db
    Returns:    pandas df

    '''

    print('fetch_weather fn')
    """Main loop."""
    # print('Entered fetch_weather function')
    # Step 1: Fetch global METAR geojson metadata
    # https://mesonet.agron.iastate.edu/sites/networks.php
    req = requests.get(
        "http://mesonet.agron.iastate.edu/geojson/network/AZOS.geojson",
        timeout=60,
    )
    geojson = req.json()
    for feature in geojson["features"]:
        station_id = feature["id"]
        if station_id == my_station:
            
            props = feature["properties"]
            # We want stations with data to today (archive_end is null)
            if props["archive_end"] is None:
                print('archive_end is null = data to today')

            # print(f'Fetching data for station {station_id}')
            # uri = (
            #     "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
            #     f"station={station_id}&data=all&year1=1928&month1=1&day1=1&"
            #     f"year2={enddt.year}&month2={enddt.month}&day2={enddt.day}&"
            #     "tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&"
            #     "direct=yes&report_type=3"
            # )
            uri = (
                "http://mesonet.agron.iastate.edu/cgi-bin/request/asos.py?"
                f"station={station_id}&data=all&year1={startdt.year}"
                f"&month1={startdt.month}&day1={startdt.day}&"
                f"year2={enddt.year}&month2={enddt.month}&day2={enddt.day}&"
                "tz=Etc%2FUTC&format=onlycomma&latlon=no&elev=no&missing=M&trace=T&"
                "direct=yes&report_type=3"
            )
            # print('uri: ', uri)

            res = requests.get(uri, timeout=300)
            # print('received response type: ', type(res))
            return res

# %% [markdown]
# ## daily_weather_to_db fn

# %%
def daily_weather_to_db():
    ''' 
    Downloads specified station's data from Iowa State University's website

    Args:       my_station      -> str with station id name
                enddt           -> str with datetime index for latest known recorded weather data on site
                startdt         -> str with datetime index for the last known recorded data on db
    Returns:    pandas df

    '''
    print('daily_weather_to_db fn')
    # Get detector name, path, and station ids from detector settings
    detectors = pd.read_csv('detector_info_settings/detector_locations.csv')
    station_ids = list(set(detectors['weather_station'].to_list()))
    
    for my_station in station_ids:

        print('Station id: ', my_station, ' counts: ', station_ids.count(my_station))
        # Get table from database then sort from most recent to least
        weather_db = get_weather_data(my_station)
        weather_db = weather_db.resample('h').sum()
        weather_db.sort_index(ascending=True, inplace=True)

        # Get last known date of data from current table
        oldest_ts = pd.to_datetime(weather_db.tail(1).index.values[0])

        # fetch
        weatherjson = fetch_weather(my_station, date.today(), oldest_ts)
        # Read as cvs from json file format
        wdf = pd.read_csv(StringIO(weatherjson.text), sep=',')
        wdf[wdf=='M'] = np.nan

        # Slice only for needed information based on dates and consider if temperature in farenheit
        # print('Columns: ', wdf.columns.to_list())
        if 'tmpc' in wdf.columns.to_list() and 'tmpf' not in wdf.columns.to_list():
            wdf['tmpc'] = wdf['tmpc'].apply(pd.to_numeric)
            wdf['tmpf'] = (wdf['tmpc'] * 9/5) + 32
        wdf['tmpf'] = wdf['tmpf'].apply(pd.to_numeric)

        if 'mslp' in wdf.columns.to_list():
            wdf['mslp'] = wdf['mslp'].apply(pd.to_numeric)
        else:
            wdf['mslp'] = np.nan
        
        if 'alti' in wdf.columns.to_list():
            wdf['alti'] = wdf['alti'].apply(pd.to_numeric)
        else:
            wdf['alti'] = np.nan
        
        # Rename columns
        wdf = wdf.rename(columns={'valid':'date', 'tmpf':'temp_in_f', 'mslp':'sea_l_pressure_millibar', 'alti':'alti_pressure'})

        # Transform dates and make into index
        wdf['date'] = pd.to_datetime(wdf['date'], utc=True)
        wdf = wdf[['date','temp_in_f', 'sea_l_pressure_millibar', 'alti_pressure']]
        wdf = wdf.set_index('date')
        wdf.sort_index(inplace=True, ascending=True)

        # Merge old and newly downloaded data
        merged = pd.concat([weather_db, wdf])
        f_merged = merged[~merged.index.duplicated(keep='last')]
        f_merged.sort_index(ascending=True, inplace=True)
        wdf = f_merged
        print('merged: ', wdf.head(1), wdf.tail(1))

        # Resample as an hourly df with mean instead of sum
        wdf = wdf.resample('h').mean()
        
        # Remove any 0 values and make into np.nan
        wdf.loc[wdf['temp_in_f'] == 0, 'temp_in_f'] = np.nan
        wdf.loc[wdf['sea_l_pressure_millibar'] == 0, 'sea_l_pressure_millibar'] = np.nan
        wdf.loc[wdf['alti_pressure'] == 0, 'alti_pressure'] = np.nan
        
        # Remove potential data errors due to shutdowns in some areas
        # Caused by power outages like Abuja
        wdf.loc[
            (wdf['temp_in_f'] > wdf['temp_in_f'].mean() + (4*wdf['temp_in_f'].std())) |
            (wdf['temp_in_f'] < wdf['temp_in_f'].mean() - (4*wdf['temp_in_f'].std()))] = np.nan
        wdf.loc[
            (wdf['sea_l_pressure_millibar'] > wdf['sea_l_pressure_millibar'].mean() + (4*wdf['sea_l_pressure_millibar'].std())) |
            (wdf['sea_l_pressure_millibar'] < wdf['sea_l_pressure_millibar'].mean() - (4*wdf['sea_l_pressure_millibar'].std()))] = np.nan
        wdf.loc[
            (wdf['alti_pressure'] > wdf['alti_pressure'].mean() + (4*wdf['alti_pressure'].std())) |
            (wdf['alti_pressure'] < wdf['alti_pressure'].mean() - (4*wdf['alti_pressure'].std()))] = np.nan

        # Connect to DB via postgresql and send to db
        engine, conn = connect_to_db_upload()
        wdf.to_sql(
            con=engine, name=f'{my_station.lower()}', if_exists='replace', index_label='date')
        print(f'Table {my_station.lower()} sent to DB successfully')

        # Make primary key for table via PSYCOPG2
        cur = conn.cursor()
        cur.execute(f"""ALTER TABLE {my_station.lower()} ADD PRIMARY KEY (date)""")
        conn.commit()
        cur.close()
        print('Query for primary key sent successfully')


# %% [markdown]
# # Detector Data processing functions

# %% [markdown]
# ## merge_adding_all_timestamps_hourly

# %%
def merge_adding_all_timestamps_hourly(merged_logs, log_df, lfreq, trim_base_df, trim_log_df):
    ''' 
    Merges two provided log df files, first being the base or earliest data, second, most recent data,
    then trims for error reduction and adjusts data frequency to hourly

    Args:       detector_name_path  -> folder containing log files to be merged
                detector_name       -> str containing detector name for access to settings
    Returns:    merged pandas df

    '''
    print('merge_adding_all_timestamps_hourly fn')
    # Format df to hourly and trim if requested
    if not merged_logs.empty and trim_base_df:
        temp = merged_logs.resample('h').sum()
        # Basic trimming of first and last hour due to timestamps missing
        temp.drop(temp.head(1).index, inplace=True)
        temp.drop(temp.tail(1).index, inplace=True)
        # Replace 0 values to nan
        temp.loc[temp['counts'] == 0] = np.nan
        # If initial values on df are all nan, remove until valid value found
        temp = temp[temp.first_valid_index():]
        merged_logs = temp

    if not log_df.empty and trim_log_df:
        temp = log_df.resample('h').sum()
        temp.drop(temp.head(1).index, inplace=True)
        temp.drop(temp.tail(1).index, inplace=True)
        temp.loc[temp['counts'] == 0] = np.nan
        temp = temp[temp.first_valid_index():]
        log_df = temp

    # Check if df is not empty after trimming and perform merge
    if not merged_logs.empty and not log_df.empty:

        # Extract first date from log df to be merged at end of current base df
        first_log_date = str(log_df.head(1).index[0])
        # Extract last date from base df
        last_log_date = str(merged_logs.tail(1).index[0])

        # Check if dates are equal or in the right chronological order ascending
        if str(merged_logs.head(1).index[0]) <= first_log_date:
            # If able to find first log date from log df on merged_logs, no detector 
            # has shutdown and just need to add at end of file whatever is not yet part of base df
            try:
                bf_first_log_date = str(merged_logs.iloc[merged_logs.get_loc(first_log_date) - 1].name)
                print('No shutdown since last log data integration')
                # Merge
                merged = pd.concat([merged_logs, log_df])
                final_merged_logs = merged[~merged.index.duplicated(keep='last')]
                # Sort fixed merged log files
                merged = final_merged_logs.sort_index()
            
            # else, logs must be merged considering missing counts due to detector shutoff time
            except:
                print('Last log date bf shutdown: ', last_log_date, '\nFirst log date after shutdown: ', first_log_date)
                # Create continuous range of dates to complete df timeline for missing date indexes
                date_range = pd.date_range(start=last_log_date, end=first_log_date, freq=lfreq, tz='UTC')
                # Create df containing missing dates as index and np.nan values
                offline_df = pd.DataFrame(index=date_range, columns=merged_logs.columns, data=np.nan)
                # Update current logs to include missing detector data time stamps but with nan values for graph
                complete_logs = pd.concat([offline_df, log_df])
                merged = pd.concat([merged_logs, complete_logs])
                final_merged_logs = merged[~merged.index.duplicated(keep='last')]
                # Sort fixed merged log files
                merged = final_merged_logs.sort_index()

        # Reverse which file is merged at end of the other to ensure chronological order
        else:
            # Extract first date from log df to be merged at end of current base df
            first_log_date = str(merged_logs.head(1).index[0])
            # Extract last date from base df
            last_log_date = str(log_df.tail(1).index[0])

            try:
                bf_first_log_date = str(log_df.iloc[log_df.get_loc(first_log_date) - 1].name)
                print('No shutdown since last log data integration')
                # Merge
                merged = pd.concat([log_df, merged_logs])
                final_merged_logs = merged[~merged.index.duplicated(keep='last')]
                # Sort fixed merged log files
                merged = final_merged_logs.sort_index()
            
            # else, logs must be merged considering missing counts due to detector shutoff time
            except:
                print('Last log date bf shutdown: ', last_log_date, '\nFirst log date after shutdown: ', first_log_date)
                # Create continuous range of dates to complete df timeline for missing date indexes
                date_range = pd.date_range(start=last_log_date, end=first_log_date, freq=lfreq, tz='UTC')
                # Create df containing missing dates as index and np.nan values
                offline_df = pd.DataFrame(index=date_range, columns=merged_logs.columns, data=np.nan)
                # Update current logs to include missing detector data time stamps but with nan values for graph
                complete_logs = pd.concat([offline_df, merged_logs])
                merged = pd.concat([log_df, complete_logs])
                final_merged_logs = merged[~merged.index.duplicated(keep='last')]
                # Sort fixed merged log files
                merged = final_merged_logs.sort_index()
    
    # Only merged logs remains after trimming
    elif not merged_logs.empty:
        merged = merged_logs
    # Only log df remains after trimming
    elif not log_df.empty:
        merged = log_df
    # None have data, return empty df
    else:
        merged = pd.DataFrame()

    return merged

# %% [markdown]
# ## merge_logs_dfs

# %%
def merge_log_dfs(log_dfs_list, detector_name):
    '''  
    Organizes each log df within a list of dfs chronologically, then merges them all.
    This includes adding missing time between end of one log to the other as np.NaN
    values due to monitor shutdowns.

    Args:       detector_name -> string containing detector name from settings
                log_dfs_list -> list containing n number of log dfs from a specific
                                monitor data folder
    Returns:    merged pandas df with all logs

    '''
    print('merge_log_dfs fn')
    if len(log_dfs_list) == 0 or log_dfs_list == None:
        print('Given list of log dfs is empty. Try again with to run the all_monitor_logs_to_dfs() with correct file path')
    elif len(log_dfs_list) > 1:
        
        # Sort logs from latest to earliest based on initial log date to ensure optimal merging
        # Extract first row date of each log df into list
        logs_l = [str(df.head(1).index[0]) for df in log_dfs_list]
        # Make dictionary containing index of corresponding date on provided logs list
        logs_dict = {}
        for i in range(len(logs_l)):
            logs_dict[logs_l[i]] = i
        # sort values in ascending order
        logs_l.sort()
        # Create sorted list of logs
        new_logs_df_list = []
        for i in range(len(logs_l)):
            new_logs_df_list.append(log_dfs_list[logs_dict[logs_l[i]]])
        
        # Extract first df on list and to start merging with rest of dfs
        merged_logs = new_logs_df_list[0].copy(deep=True)
        # Extract frequency of data from given monitor
        lfreq = detector_settings[detector_name]['freq']
        # Flag for initial merged df to be trimmed for incomplete hourly logs
        trim_initial_merged = True

        # Navigate through list of dfs and merge, making the df hourly
        for i in range(1, len(new_logs_df_list)):
            print(f'Log file index {i}')
            merged_logs = merge_adding_all_timestamps_hourly(merged_logs, new_logs_df_list[i], lfreq, trim_initial_merged, True)
            trim_initial_merged = False # Set flag to false to no longer trim base df as it has been done

    # Else, the df list only has one df so no merging within list
    else: 
        merged_logs = log_dfs_list[0].copy(deep=True)
        # Sample by hour
        merged_logs1 = merged_logs.resample('h').sum()
        # Trim first and last hour because of data missing due to log being incomplete
        merged_logs1.drop(merged_logs1.head(1).index, inplace=True)
        merged_logs1.drop(merged_logs1.tail(1).index, inplace=True)
        merged_logs1.loc[merged_logs1['counts'] == 0] = np.nan
        
        # Reassign for return statement accuracy
        merged_logs = merged_logs1

    return merged_logs

# %% [markdown]
# ## log_df_formatting

# %%
def log_df_formatting(logs_df, detector_name):
    ''' 
    Formats given logs into a datetime and counts column df. If desired, you can keep the
    additional counts columns in case needed for later.
    
    Args:       logs_df         -> pandas df containing non-formatted data where only one column
                                    named 'counts' exists and has all data.
                detector_name    -> indicates how to split the row based on specific detector's
                                    row content, since some have more data than others
    
    Returns:    pandas df containing formatted logs as date index and counts column

    '''
    print('log_df_formatting fn')
    # Get specific split number of elements depending monitor log file data format
    splits = detector_settings[detector_name]['splits']
    # Get counts column
    counts_col = detector_settings[detector_name]['counts_col']
    # Get index for date column
    date_col = detector_settings[detector_name]['date_col']
    # Get corresponding timezone
    monitor_tz = detector_settings[detector_name]['timezone']

    # Make copy to ensure it is not damaging current logs data
    temp = logs_df.copy(deep=True)

    # Format df to remove tracing commas after counts values if the separation is based on spacing
    if temp['counts'].str.contains(' ').any() & temp['counts'].str.contains(',').any():
        temp['counts'] = temp['counts'].str.replace(',','', regex=True)
        
    # Split counts column into n elements (i.e.: if n=4, containing count1, count2, count3, day)
    # separation is space-based " "
    if temp['counts'].str.contains(' ').any():
        temp = temp['counts'].str.split(" ", n = splits, expand=True)
    # else, separation is comma-based ","
    else:
        temp = temp['counts'].str.split(",", n=splits, expand=True)
    
    # Slice df to only have desired columns counts and date
    temp = temp.rename(columns={date_col:'date',counts_col:'counts'})
    ldf = temp[['date', 'counts']]

    # transform date column string into a datetime format type
    ldf['date'] = pd.to_datetime(ldf['date'], format='mixed')
    
    # Localize to monitor location's timezone, ambiguous to infer fall DST change an hour back, 
    # and nonexistent for clocks moving forward due to DST
    try:
        # It infers the date and shifts forward if dailight savings causes errors
        ldf['date'] = ldf['date'].dt.tz_localize(monitor_tz, ambiguous='infer', nonexistent='shift_forward')
    except:
        try:
            # If duplicate dates due to localization into a timezone with daylight, choose to keep one
            ldf['date'] = ldf['date'].dt.tz_localize(monitor_tz, ambiguous=True, nonexistent='shift_forward')
        except:
            # Else, the df is already localized to a particular timezone
            print('DF date already timezone aware so no need!')

    # Format to UTC so it can be merged with the weather app's data that is also UTC
    if str(ldf['date'].dt.tz) != 'UTC':
        ldf['date'] = ldf['date'].dt.tz_convert('UTC')

    # # Function to handle individual rows in the event df has both tz-aware and tz-unaware data
    # def convert_to_utc(date):
    #     # If tz-aware
    #     if date.tzinfo is not None: 
    #         # Convert to UTC right away
    #         return date.tz_convert('UTC')
    #     else: # If not tz-aware
    #         try:
    #             # Localize to local tz if no DST
    #             date = date.tz_localize(monitor_tz)
            
    #         except:
    #             # Handle any tz DST issues present
    #             try:
    #                 date = date.tz_localize(monitor_tz, ambiguous='infer', nonexistent='shift_forward')
    #             except:
    #                 date = date.tz_localize(monitor_tz, ambiguous=True, nonexistent='shift_forward')
    #         # Finish by converting row to UTC after localizing
    #         return date.tz_convert('UTC')
    
    # # Utilize individual row function if convert fails after having tried tz_localize previously too
    # try:
    #     if str(ldf['date'].dt.tz) != 'UTC':
    #         ldf['date'] = ldf['date'].dt.tz_convert('UTC')
    # except:
    #     print('Entering row by row conversion')
    #     ldf['date'] = ldf['date'].apply(convert_to_utc)

    # Set date column as index
    ldf = ldf.set_index('date')
    # Make counts column into numeric type
    ldf['counts'] = ldf['counts'].apply(pd.to_numeric)

    # Remove any errors due to NaT values on index date column
    try:
        ldf2 = ldf.drop('NaT')
    except:
        ldf2 = ldf

    # Sort df based on date index
    ldf2.sort_index()
    
    return ldf2

# %% [markdown]
# ## all_detector_logs_to_dfs

# %%
def all_detector_logs_to_dfs(detector_name_path, detector_name):
    ''' 
    Creates a df of merged log files. This assumes all logs within given monitor folder
    name share same format style. Log files should be reviewed before applying this function.

    Args:       detector_name_path  -> folder containing log files to be merged
                detector_name       -> str containing detector name for access to settings
    Returns:    merged pandas df

    '''
    print('all_detector_logs_to_dfs fn')
    # list of files within selected monitor
    all_files = listdir(detector_name_path)
    # filter based on ending being .log
    logs_list = [f for f in all_files if f.endswith('.log')]

    # df = pd.DataFrame()
    logs_df_list = []

    for log_file in logs_list:
        # Read log file as df separating rows
        temp = pd.read_csv(detector_name_path+'/'+log_file, sep='\t', names=['counts'])
        # If df has column titles, remove as it causes issues with below functions
        if temp.head(1)['counts'].str.contains('date').any():
            temp.drop(temp.head(1).index, inplace=True)
        # Format df based on monitor settings
        temp = log_df_formatting(temp, detector_name)
        # Append to list of dfs
        logs_df_list.append(temp)

    return logs_df_list

# %% [markdown]
# ## reduce_shutdown_count_errors

# %%
def reduce_shutdown_count_errors(df):
    ''' 
    Removes any values before and after shutdowns (up to 3) where values are greater or less than
    the mean for a 24 (or less, if not enough available) window of data +- the standard dev.*1.5

    Args:       df
    Returns:    df

    '''
    print('reduce_shutdown_count_errors fn')

    # Ensure df is hourly
    df = df.resample('h').sum()
    # Re-establish np.nan values due to above function replacing them with 0s
    df.loc[df['counts'] == 0] = np.nan

    # Add missing dates to ensure graph shows correct on website (i.e. offline is demarket instead of assuming online)
    start = pd.to_datetime(df.head(1).index.values[0], utc=True)
    end = pd.to_datetime(df.tail(1).index.values[0], utc=True)
    t = pd.date_range(start=start, end=end, freq='h', tz='UTC')
    tdf = pd.DataFrame(index=t, columns=df.columns, data=np.nan)
    df1 = pd.concat([tdf, df])
    df2 = df1[~df1.index.duplicated(keep='last')]
    df = df2.sort_index(ascending=True)

    # Do initial cleanup of anything above or below the mean + std*3
    df.loc[(df['counts'] > df['counts'].mean() + (3*df['counts'].std())) | (df['counts'] < df['counts'].mean() - (3*df['counts'].std()))] = np.nan
    df = df[(df.first_valid_index()):df.last_valid_index()]
    
    # Extract initial indexes if any
    f = df.index.get_loc(df.first_valid_index())
    l = df.index.get_loc(pd.to_datetime(df.isna().idxmax().head(1).values[0], utc=True))

    # If the last index for interval is the same as initial index of df, it means
    # there have never been any disruptions on data due to shutdowns
    if l != f:

        while l <= len(df) and f != l:
            # Deal with spikes after shutdowns, calculate mean and std
            if (f+24) < l:
                mean = df[f:(f+24)].mean().values[0]
                std = df[f:(f+24)].std().values[0]
            else:
                mean = df[f:(l - 1)].mean().values[0]
                std = df[f:(l - 1)].std().values[0]
            
            # Check if first three values are lesser or greater than mean +- std, then assign np.nan
            if df.iloc[f]['counts'] < (mean - (std*1.5)) or df.iloc[f]['counts'] > (mean + (std*2)):
                df.iloc[f]['counts'] = np.nan
            if f+1 < len(df) and df.iloc[f+1]['counts'] < (mean - (std*1.5)) or df.iloc[f+2]['counts'] > (mean + (std*2)):
                df.iloc[(f+1)]['counts'] = np.nan
            if f+2 < len(df) and df.iloc[f+2]['counts'] < (mean - (std*1.5)) or df.iloc[f+2]['counts'] > (mean + (std*2)):
                df.iloc[(f+2)]['counts'] = np.nan

            # Deal with spikes before shutdowns
            if (l-25) > f:
                mean = df[(l - 25):(l - 1)].mean().values[0]
                std = df[(l - 25):(l - 1)].std().values[0]
            else:
                mean = df[f:(l - 1)].mean().values[0]
                std = df[f:(l - 1)].std().values[0]

            # Check if last three values are lesser or greater than mean +- std, then assign np.nan
            if df.iloc[l-1]['counts'] < (mean - (std*1.5)) or df.iloc[l-1]['counts'] > (mean + (std*2)):
                df.iloc[(l-1)]['counts'] = np.nan
            if  l-2 > 0 and df.iloc[l-2]['counts'] < (mean - (std*1.5)) or df.iloc[l-2]['counts'] > (mean + (std*2)):
                df.iloc[(l-2)]['counts'] = np.nan
            if l-3 > 0 and df.iloc[l-3]['counts'] < (mean - (std*1.5)) or df.iloc[l-3]['counts'] > (mean + (std*2)):
                df.iloc[(l-3)]['counts'] = np.nan

            # Obtain new start and end index for evaluation of next df slice
            f = df.index.get_loc(df[l:].first_valid_index())
            l = df.index.get_loc(pd.to_datetime(df[f:].isna().idxmax().head(1).values[0], utc=True))
            
            # if l == f:
            #     break

    # Ensure all values == 0 are not accounted numerically during graphing and mean/std calculations
    df.loc[df['counts'] == 0] = np.nan
    
    df = df.sort_index()

    return df

# %% [markdown]
# ## process_and_upload_logs

# %%
def process_and_upload_logs(detector_data, detector_file_path, detector_name_og, detector_name):
    ''' 
    Function that handles the overall processing of new logs and insertion into table

    Args:       detector_data       -> df containing all detector logs
                detector_file_path  -> local/server path for files for specified detector locations
                detector_name_og    -> name as str without any formatting enforced for naming files and subfolder
                detector_name       -> name as str having been formatted for purposes of accessing right table on 
                                        db

    '''
    print('process_and_upload_logs fn')
    # List of formatted logs into dfs
    log_dfs_list = all_detector_logs_to_dfs(detector_file_path, detector_name_og)

    # Merge all found logs into a df
    hourly_logs = merge_log_dfs(log_dfs_list, detector_name_og)

    # Merge db data with new log data
    df = pd.concat([detector_data, hourly_logs])
    df1 = df[~df.index.duplicated(keep='last')]
    df1 = df1.sort_index(ascending=True)
    
    # Filter out low counts or out of standard deviation data each time detectors disconnect
    df = reduce_shutdown_count_errors(df1)
    
    # Upload to db
    engine, conn = connect_to_db_upload()
    cur = conn.cursor()
    df.to_sql(con=engine, name=f'{detector_name}', if_exists='replace', index_label='date')
    print('Table sent to DB successfully')
    
    # Make primary key for table via PSYCOPG2
    cur = conn.cursor()
    cur.execute(f"""ALTER TABLE {detector_name} ADD PRIMARY KEY (date)""")
    conn.commit()
    cur.close()
    print('Query for primary key sent successfully')

    # Delete log files to avoid clutter since already on db
    l=glob.glob(os.path.join(detector_file_path, '*.log'))

    if len(l) <=1:
        print('No files or only one file found.')
    else:
        l.sort(key=os.path.getmtime, reverse=True)
        print(l)

        del_l = l[1:]

        for file in del_l:
            try:
                os.remove(file)
                print(f'deleting {file}')
            except:
                print(f'Error deleting file/file not found - {file}')


# %% [markdown]
# # Main Function call

# %% [markdown]
# ## daily_logs_to_db fn

# %%
def daily_logs_to_db():
    print('daily_logs_and_weather_to_db fn')
    # Home directory
    homedir = 'data/'

    # Get detector name, path, and station ids from detector settings
    detectors = pd.read_csv('./detector_info_settings/detector_locations.csv')
    detectors_info = detectors[['name','name_path', 'weather_station']].values.tolist()
    

    # For each available detector row within settings csv as df
    for row in detectors_info:
        print('\n\n**************\nDetector: ', row[0])
        # Format name for file naming and db table access
        detector_name = format_name(detector_name_og=row[0])
        
        # Download db tables as dfs
        detector_db = get_detector_data(detector_name=detector_name)
        
        # Process detector count logs, join them to db table and upload to db, then delete older files
        process_and_upload_logs(detector_data=detector_db, detector_file_path=f'{homedir}/{row[1]}', detector_name_og=row[0], detector_name=detector_name)


# %% [markdown]
# # Execute daily_logs_to_db

# %%
daily_logs_to_db()

# %% [markdown]
# # Execute daily_weather_to_db

# %%
# Format station data and upload to db
daily_weather_to_db()