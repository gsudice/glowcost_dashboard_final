import pandas as pd
import numpy as np

def merge_4paddle_logs(new_logs):
    ''' 
    Uses the newest downloaded log file for the 4Paddle detector and 
    merges them with the current logs csv file. This function is unique because each detector
    log file follows a specific format and name.
    
    Args:       logs_csv -> csv file name containing all merged logs since last execution of function
                new_logs -> log file name downloaded from a detector server by the cosmic server, then
                        downloaded to the database server for this web app
            
    Returns:   merged_logs -> csv file with all merged logs as df, then also stores new csv version
    
    * DISCLAIMER: It assumes the paths for the csv file is fixed and no need
    to be directly provided. If administrator changes path route, he must correctly assign new path

    '''
    # CSV file into a dataframe and format to have datetime and numeric columns
    df1 = pd.read_csv('4paddle_merged_logs.csv', names=['date','counts'])[1:] # Remove extra first row
    df1["date"] = pd.to_datetime(df1['date'])
    df1['date'] = df1['date'].dt.tz_convert('UTC') # convert time zone to UTC
    df1 = df1.set_index('date')
    df1["counts"] = df1["counts"].apply(pd.to_numeric)

    # Create new df with downloaded logs file, example name -> "./logs/4Paddle_2024-08-07_to_2024-08-16.log"
    df2 = pd.read_csv(new_logs, sep='\t', names=['counts'])
    # Split data by spacing, then into a group of 3 elements (i.e., column 1: 385 column 2: 0 column 3:0 column 4: Wed Oct 11 17:17:30 2023)
    df2 = df2['counts'].str.split(" ", n=3, expand=True)
    # Create df and indicate column names for new columns
    dft2 = pd.DataFrame(df2.values, columns=["counts", "junk1", "junk2", "date"])
    
    # Format date column to date value
    dft2["date"] = pd.to_datetime(dft2['date'], format="%a %b %d %H:%M:%S %Y")
    # Transform date into current timezone
    dft2['date'] = dft2['date'].dt.tz_localize('America/New_York', ambiguous='infer')
    # convert time zone to UTC (Cordinated Universal Time)
    dft2['date'] = dft2['date'].dt.tz_convert('UTC')
    
    # make date column the index
    dft2 = dft2.set_index('date')

    # convert counts column data to numeric format -> in case strings appear, it won't cause errors in contrast with astype(int)
    dft2["counts"] = dft2["counts"].apply(pd.to_numeric)

    # clean df by removing columns junk1 and junk2
    dft2.drop(dft2.columns[[1, 2]], axis=1, inplace=True)

    # resampling hourly and getting sum due to logs being recorded for every minute
    dft2_hourly = dft2.resample('H').sum()

    # Drop first and last hour on log file due to hourly data count giving innacurate total
    # resulting from starting and ending halfway through the hour/incomplete count
    dft2_hourly.drop(dft2_hourly.head(1).index, inplace=True)
    dft2_hourly.drop(dft2_hourly.tail(1).index, inplace=True)

    # from physics student approach, not needed/errors
    # np.nan any values less than a set min count, this value is set by the lab and has
    # not been consistent, i.e. 12000 for 4paddle vs 1000 for 2paddle
    # dft2_hourly.loc[dft2_hourly[dft2_hourly['counts'] < min_count].index, 'counts'] = np.nan

    ''' 
    Obtain start and end times if the detector has shut off. This can be found via
    the log file's first entry as the new produced log files will only contain logs starting
    from the moment the detector went back online. If the first date (i.e. 2024-08-07)
    in the log file is already in the csv, it means they were successfully merged previously
    and np.nan values replaced the dates were the detector was offline.

    DISCLAIMER: This format is working as of 08/15/2025, implemented by Sara Edwards at DICE, GSU.
    Prior merges of log file were performed by physics students and therefore, no guarantee 
    of data handling the same way as this method.

    '''

    # Get first row's index name of log file df
    first_log_date = str(dft2_hourly.iloc[0].name)
    # If able to find first log date on merged logs, no detector has shutdown and just need to add at end of file
    try:
        last_log_date = str(df1.iloc[df1.index.get_loc(first_log_date) - 1].name)
        print('No shutdown since last log data integration')
        # Merge
        merged_logs = pd.concat([df1, updated_dft2_hourly])
        final_merged_logs = merged_logs[~merged_logs.index.duplicated(keep='last')]

    # else, retrieve detector shutoff date, because detector was shutoff and logs must be merged considering missing counts
    except:
        # Get last log date at end of merged logs file
        last_log_date = str(df1.iloc[-1].name)
        # Create index values for days and hours detector was shut down
        offline_index_values = pd.date_range(start=last_log_date, end=first_log_date, freq='H', tz='UTC')
        # Create df containing missing dates as index and np.nan values
        offline_df = pd.DataFrame(index=offline_index_values, columns=dft2_hourly.columns, data=np.nan)
        # Update current logs to include missing detector data
        updated_dft2_hourly = pd.concat([offline_df, dft2_hourly])
        merged_logs = pd.concat([df1, updated_dft2_hourly])
        final_merged_logs = merged_logs[~merged_logs.index.duplicated(keep='last')]
    
    # Merged logs into a csv file
    final_merged_logs.to_csv('4paddle_merged_logs.csv')
    return final_merged_logs