''' 
Module containing functions to generate graphs for each detector

'''

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from os.path import exists
from database import connect_to_db
from sqlalchemy import text


LABEL_GRAPH_DETECTOR = {
    "title": "<b>Detector</b>",
    "yaxis": {"title": "<b>Flux percentage change</b>"},
    "xaxis": {"title": "<b>Date</b>"},
    "legend": {"title": "Percentages"},
}

def format_sql(sql_data):
    ''' 
    Formats sql data fetched from table into datetime and numeric columns
    Args:       sql_data -> sqlalchemy row.Row object
    Returns:    pandas df

    '''
    # CSV file into a dataframe
    df = pd.DataFrame(sql_data)
    return df


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
        # margin={"t": 55, "l": 55, "r": 55, "b": 55},
        margin={"t": 0, "l": 0, "r": 20, "b": 0},
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
        height=400,
    )
    return go.Figure(data, layout)


def update_detector_figure(detector_name, og_detector_name):
    '''
    Generates graph figure based on provided detector data
    
    Args:       - detector_name (str): Name of detector for which data is being retrieved

    Returns:    - px.line figure: An plotly express figure showing glowcost data

    '''


    # Extract table from db
    try:
        # print(f'Attempting to fetch data for monitor {detector_name}')
        db = connect_to_db()
        print(detector_name)
        with db.connect() as conn:
            query = text(f'SELECT * FROM {detector_name}')
            result = conn.execute(query)
            data = result.fetchall()
            conn.close()
            # Format data into pandas df
            df = format_sql(data)

        # Close connection
        db.dispose()

        df = df.set_index('date')

        # Calculate hourly moving average
        df['hourly_average'] = df['counts'].rolling(window='24h').mean()

        # Create a figure
        fig = go.Figure(
            [   # Offline
                go.Scatter(
                    x=df.index,
                    y=df['counts'],
                    name='Offline',
                    line=dict(dash='dash', color='red', width=0.5),
                    connectgaps=True
                ),
                # Raw Muon counts
                go.Scatter(
                    x=df.index,
                    y=df['counts'],
                    name='Hourly Muon Counts',
                    line=dict(color='red', width=2)
                ),
                # Hourly average
                go.Scatter(
                    x=df.index,
                    y=df['hourly_average'],
                    name='Hourly Counts Moving Ave.',
                    line=dict(color='blue', width=2)
                ),
            ]
        )

        fig.update_layout(
            title = {
                'text': f'{og_detector_name} : Real Time Cosmic Muon Monitor (Updated Daily)',
                'x':0.5,
                'y':0.9,
                'xanchor':'center',
                'yanchor':'top',
                'font_color':"#002379",
                'font_size':20
            }
        )

        return fig
    
    except:
        print('Data fetch failed')
        return None




def update_moving_average_figure(detector_name, og_detector_name):
    '''
    Generates graph figure based on provided detector data
    based on the toggle button's request for the last 24 hours

    Args:
        detector_name (str): Name of detector for which data is being retrieved
    
    Returns:
        px.line figure: An plotly express figure showing glowcost data

    '''
    # # Extract table from db
    # try:
    # print(f'Attempting to fetch data for monitor {detector_name}')
    db = connect_to_db()
    print(detector_name)
    with db.connect() as conn:
        query = text(f'SELECT * FROM {detector_name}')
        result = conn.execute(query)
        data = result.fetchall()
        conn.close()
        # Format data into pandas df
        df = format_sql(data)

    # Close connection
    db.dispose()
    df = df.set_index('date')
    # Calculate hourly moving average
    df['hourly_average'] = df['counts'].rolling(window='24h').mean()
    print(df.iloc[:50])

    # # Create a figure of the moving average data using Plotly Express
    # fig_hr_avg = px.line(
    #     df_last_day, 
    #     x='date', 
    #     y=['One_hourly_avg', 'Two_hourly_avg', 'Three_hourly_avg'],
    #     title=f'{detector_name} : Hourly Moving Average of Muon Data',
    # )
    # fig_hr_avg.update_layout(
    #     title = {
    #         'text': f'{detector_name} : Hourly Moving Average of Muon Data',
    #         'x':0.5,
    #         'y':0.9,
    #         'xanchor':'center',
    #         'yanchor':'top',
    #         'font_color':"#002379",
    #         'font_size':20
    #     }
    # )

    # return fig_hr_avg
    
    # # If no data found
    return None