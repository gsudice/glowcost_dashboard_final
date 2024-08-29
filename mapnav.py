import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv
import os
from os.path import exists
import plotly.express as px


def map_display():
    ''' 
    Creates a map via the mapbox graph_objects library that displays the geolocation of each
    monitor/sensor contained in a given csv file. This will output on an html container.

    '''
    load_dotenv()
    mapbox_access_token = os.getenv('MAPBOX_TOKEN')

    if exists('detector_info_settings/detector_locations.csv'):

        df = pd.read_csv('detector_info_settings/detector_locations.csv', sep=',', header=0)

        fig = go.Figure()
        fig.add_trace(go.Scattermapbox(
                text=df.name,
                lat=df.lat,
                lon=df.long,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color='rgb(255, 159, 102)',
                    opacity=0.7
                ),
                cluster=dict(enabled=True),
            ))

        fig.update_layout(
            hovermode='closest',
            title='Detectors located Worldwide',
            margin={"r": 0, "t": 0, "l": 0, "b": 0},
            mapbox_style="open-street-map",
            autosize=True,
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=0,
                center=dict(
                    lat=38,
                    lon=-94
                ),
                pitch=0,
                zoom=1,
                style='light'
            ),
        )
        return fig
    return None