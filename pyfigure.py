''' 

Module containing functions to generate graphs for each detector

'''
import plotly.graph_objects as go
from database import connect_to_db, format_sql
from sqlalchemy import text
import pandas as pd

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

    # Extract table from db
    # try:
    db = connect_to_db()
    # Format detector name to lowercase and check formatting of name 
    # doesn't have number up front
    detector_name = detector_name_og.lower()
    if detector_name.startswith('2') or detector_name.startswith('4'):
        detector_name = detector_name[1:]+detector_name[0]

    detectors = pd.read_csv('detector_info_settings/detector_locations.csv', sep=',')
    detector_station = detectors.loc[detectors['name'] == detector_name_og, 'weather_station'].item()
    detector_station = detector_station.lower()

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

        # Format data into pandas df
        df = format_sql(counts_data)
        wdf = format_sql(weather_data)

        print('heads: ', df.head(1), wdf.head(1), '\n')
        print('tails: ', df.tail(1), wdf.tail(1))

        wdf = wdf.loc[df.head(1).index.values[0]:]
        # print(wdf)
        print('found: ')
        # print(wdf.loc[df.tail(1).index.values[0]])
        # wdf = wdf.loc[:df.tail(1).index.values[0]]
        # print(wdf)

        # print('heads: ', df.head(1), wdf.head(1), '\n')

    # Close connection
    db.dispose()

    # Calculate hourly moving average
    df['hourly_average'] = df['counts'].rolling(window='24h').mean()
    print('err1')
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
    print('error2')
    # fig.append_trace(
    #     [
    #         # temperature
    #         go.Scatter(
    #             x=wdf.index,
    #             y=df['temp_in_f'],
    #             name='Temp(°F)',
    #             line=dict(color='green', width=2)
    #         ),
    #         # Sea level pressure
    #         go.Scatter(
    #             x=df.index,
    #             y=df['sea_l_pressure_millibar'],
    #             name='Sea Level Pressure',
    #             line=dict(color='orange', width=2)
    #         ),
    #     ]
    # )

    print('fig type: ', type(fig))
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