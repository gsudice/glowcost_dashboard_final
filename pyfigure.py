''' 

Module containing functions to generate graphs for each detector

'''
import plotly.graph_objects as go
from database import connect_to_db, format_sql
from sqlalchemy import text
import pandas as pd
import numpy as np

LABEL_GRAPH_DETECTOR = {
    "title": "<b>Detector</b>",
    "yaxis": {"title": "<b>Flux percentage change</b>"},
    "xaxis": {"title": "<b>Date</b>"},
    "legend": {"title": "Percentages"},
}

def generate_empty_figure(text: str= '', size: int = 40):
    '''
    Generates graph figure 
    
    Args:
        text (str, optional): Text to be displayed as an annotation. Defaults to "".
        size (int, optional): Font size of the annotation. Defaults to 40.

    Returns:
        go.Figure: An empty figure with the specified text annotation.

    '''
    data = [{'x':[],'y':[]}]
    layout = go.Layout(
        title={'text':'', 'x':0.5},
        xaxis={
            'title':'',
            'showgrid': False,
            'showticklabels':False,
            'zeroline':False,
        },
        yaxis={
            "title": "",
            "showgrid": False,
            "showticklabels": False,
            "zeroline": False,
        },
        margin={"t": 0, "l": 0, "r": 0, "b": 0},
        annotations=[
            {
                "name": "text",
                "text": f"<i>{text}</i>",
                "opacity": 0.3,
                "font_size": size,
                "xref": "x domain",
                "yref": "y domain",
                "x": 0.5,
                "y": 0.05,
                "showarrow": False,
            }
        ],
        paper_bgcolor='rgb(229, 236, 246)',
        height=300,
    )
    return go.Figure(data, layout)


def update_detector_figure(detector_name_og):
    '''
    Generates graph figure based on provided detector data
    
    Args:       - detector_name (str): Name of detector for which data is being retrieved

    Returns:    - px.line figure: An plotly express figure showing glowcost data

    '''
    # Format detector name to lowercase and check formatting of name doesn't have number up front
    detector_name = detector_name_og.lower()
    if detector_name.startswith('2') or detector_name.startswith('4'):
        detector_name = detector_name[1:]+detector_name[0]

    detectors = pd.read_csv('detector_info_settings/detector_locations.csv', sep=',')
    detector_station = detectors.loc[detectors['name'] == detector_name_og, 'weather_station'].item()
    detector_station = detector_station.lower()

    # Extract tables from db
    # try:
    db = connect_to_db()
    with db.connect() as conn:
        query = text(f'SELECT * FROM {detector_name}')
        result = conn.execute(query)
        counts_data = result.fetchall()
        conn.close()
    
    db = connect_to_db()
    with db.connect() as conn:

        query = text(f'SELECT * FROM {detector_station}')
        result = conn.execute(query)
        weather_data = result.fetchall()
        conn.close()
    
    # Close connection
    db.dispose()
    
    # Format data into pandas df
    df = format_sql(counts_data)
    wdf = format_sql(weather_data)

    # Slice based on counts df indexes
    wdf = wdf.loc[pd.to_datetime(df.head(1).index.values[0],utc=True):]
    wdf = wdf.loc[:pd.to_datetime(df.tail(1).index.values[0],utc=True)]

    # Format all columns appropiately to a numeric type
    columns_types = wdf.dtypes.to_list()
    if len(set(columns_types)) > 1:
        for col in wdf.columns.to_list():
            wdf[col] = pd.to_numeric(wdf[col])
    
    # Remove spikes of data points that are errors via standard deviation
    wdf.loc[(wdf['alti_pressure'] > wdf['alti_pressure'].mean() + (4*wdf['alti_pressure'].std())) | (wdf['alti_pressure'] < wdf['alti_pressure'].mean() - (4*wdf['alti_pressure'].std()))] = np.nan

    df.sort_index(inplace=True)
    # Calculate hourly moving average
    df['hourly_mov_average'] = df['counts'].rolling(window='24h').mean()

    ''' 
    The Percentage Change quantifies the change from one number to another 
    and expresses the change as an increase or decrease.

        i.e.: 10 apples to 20 apples change = 100% increase (change)

    Percentage change equals the change in value divided by the 
    absolute value of the original value, multiplied by 100.

        i.e.: (V2 - V1)/ |V1|  * 100

    For purposes of this calculation, our V2 is the mean of the counts of muons
    '''
    df['counts_pct'] = ((df['counts'] - df['counts'].mean()) / df['counts'].mean() * 100)
    wdf['temp_pct']=0.2*((wdf['temp_in_f'] - wdf['temp_in_f'].mean())/ wdf['temp_in_f'].mean()*100)
    wdf['alti_press_pct'] = 5*((wdf['alti_pressure'] - wdf['alti_pressure'].mean()) / wdf['alti_pressure'].mean() * 100)
    wdf['sea_l_press_pct'] = ((wdf['sea_l_pressure_millibar'] - wdf['sea_l_pressure_millibar'].mean()) / wdf['sea_l_pressure_millibar'].mean() * 100)
    
    # Change/delta of counts, pressure and temp - not really used but physics lab was calculating for later use
    df['delta_counts'] = np.log(df['counts'] / df['counts'].mean())
    wdf['delta_temp'] = wdf['temp_in_f'] - wdf['temp_in_f'].mean()
    wdf['delta_alti_pressure'] = wdf['alti_pressure'] - wdf['alti_pressure'].mean()
    wdf['delta_sea_l_pressure'] = wdf['sea_l_pressure_millibar'] - wdf['sea_l_pressure_millibar'].mean()
    
    
    # make counts df tz-naive
    # df.index = df.index.tz_localize(None)
    
    # Create a figure
    fig = go.Figure(
        [   # Offline
            go.Scatter(
                x=df.index,
                y=df['counts_pct'],
                name='Offline',
                line=dict(dash='dash', color='red', width=0.5),
                connectgaps=True
            ),
            # Muon counts
            go.Scatter(
                x=df.index,
                y=df['counts_pct'],
                name='Muon Counts % Change',
                line=dict(color='red', width=1)
            ),
            # temperature
            go.Scatter(
                x=wdf.index,
                y=wdf['temp_pct'],
                name='Temp(°F) % Change',
                line=dict(color='green', width=1),
                connectgaps=True
            ),
            # Altitude pressure
            go.Scatter(
                x=wdf.index,
                y=wdf['alti_press_pct'],
                name='Alt. Pressure % Change',
                line=dict(color='blue', width=1),
                connectgaps=True
            ),
        ]
    )
    
    # If sea level pressure available, plot it
    # print('any sea: ', pd.isna(wdf['sea_l_pressure_millibar']).all())
    if not pd.isna(wdf['sea_l_pressure_millibar']).all():
        fig.add_trace(
            # Sea level pressure
            go.Scatter(
                x=wdf.index,
                y=wdf['sea_l_press_pct'],
                name='Sea Level Press % Change',
                line=dict(color='orange', width=1)
            ),
        )
    
    fig.update_layout(
        title = {
            'text': f'{detector_name_og} : Real Time Cosmic Muon Monitor (Updated Daily)',
            'x':0.5,
            'y':0.99,
            'xanchor':'center',
            'yanchor':'top',
            'font_color':"#002379",
            'font_size':15
        },
        height=280,
        margin=dict(l=0, r=0, t=25, b=0),
    )
    
    return fig, df
    
    # except:
    #     print('Data fetch failed')
    #     return None, None