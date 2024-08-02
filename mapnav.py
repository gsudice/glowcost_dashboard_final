import plotly.graph_objects as go
from dash import html
import pandas as pd
from dotenv import load_dotenv
import os
from os.path import exists

def map_display():

    load_dotenv()
    mapbox_access_token = os.getenv('MAPBOX_TOKEN')

    if exists('app_data/detector_locations.csv'):

        df = pd.read_csv('app_data/detector_locations.csv')
        site_lat = df.lat
        site_lon = df.lon
        locations_name = df.text

        fig = go.Figure()

        fig.add_trace(go.Scattermapbox(
                lat=site_lat,
                lon=site_lon,
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=10,
                    color='rgb(255, 159, 102)',
                    opacity=0.7
                ),
                text=locations_name,
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
                zoom=3,
                style='light'
            ),
        )
        return fig
    return None