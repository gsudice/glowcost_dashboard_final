import dash
from dash import callback, Input, Output, State, dcc, ctx
import dash_bootstrap_components as dbc
import pylayout
from os.path import exists
dash.register_page(__name__)
import pandas as pd
from pathlib import Path
import pyfigure
from data_downloads import download_csvs

layout = dbc.Container(
    [
        pylayout.HTML_MAPNAV,
        pylayout.HTML_GRAPHS,
        pylayout.HTML_DATA_HISTORY,
    ],
    fluid=True,
    className="dbc",
    style={
        "padding": "0px 0px 0px 0px", 
        'margin':"-16px 0px 0px 0px" # Quick fix: Need to figure out why random space 
        # between page and browser on top
    },
)

''' 
Callback for displaying graphs of selected detector data on multiple
choice dropdown menu.

Args:   - int 0 or 1 depending if user clicked button

Returns:
        - Tuple [
            html.H2 header object,
            ggc.Graph object,
            dcc.Button style dictionary,
            dcc.Button style dictionary,
            dcc.Button style dictionary,
            dcc.Button style dictionary,
        ]
'''
@callback(
    [
        Output('h-warnings', 'children'),
        Output('load-graph','children'),
        Output('toggle-moving-average', 'style'),
        Output("btn-download-24", 'style'),
        Output("btn-download-mov", 'style'),
        Output("btn-download-all", 'style'),
    ],
    Input('map_plot','clickData'),
    Input('toggle-moving-average', 'n_clicks'),
    State('map_plot', 'map'),
    prevent_initial_call=True
)
def update_graph(clickData, n_clicks, state):

    # Extract id of current input being used
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    
    # If user clicked on map, display graph for corresponding detector for the first time
    if clickData:

        # Extract detector name and use to display graph
        detector = clickData['points'][0]['text']
        # print('button name: ', button_id, 'detector: ', detector)
        # Format detector name to lowercase and check formatting of name 
        # doesn't have number up front
        detector_name = detector.lower()
        if detector_name.startswith('2') or detector_name.startswith('4'):
            detector_name = detector_name[1:]+detector_name[0]

        # Update graph to replace empty graph figure or current graph
        # by returning a dash component
        if button_id == 'map_plot':
            
            fig = pyfigure.update_detector_figure(detector_name, detector)
        
        # If current input is from toggle clicks, change graph for same current detector
        elif button_id == 'toggle-moving-average':
            # Cast string clicks into int number
            n_clicks = int(n_clicks)

            if n_clicks % 2 == 0:
                fig = pyfigure.update_detector_figure(detector_name, detector)
            else:
                fig = pyfigure.update_moving_average_figure(detector_name, detector)

        # Notify user if graph can be reproduced via title change and 
        # Set up additional buttons for display accordingly
        if fig != None:
            detector_graph = dcc.Graph(
                        id='graph-detector-display',
                        # Initial empty graph display bf user selects detector
                        figure=fig,
            ),
            title = None
            style = {}
        else:
            # In case data is not available, revert to empty figure display
            detector_graph = dcc.Graph(
                        id='graph-detector-display',
                        # Initial empty graph display bf user selects detector
                        figure=pyfigure.generate_empty_figure(),
                        config={'staticPlot':True},
            ),
            title = f'Data for {detector} Detector Not Available at This Time. Try again.'
            style = {'display':'none'}
        
        return [
            title, 
            detector_graph, 
            style, 
            style, 
            style, 
            style
        ]
    # else, no update occurs
    return dash.no_update

''' 
Callback to handle download data requests depending on prefered type

Args:   - int 0 or 1 depending if user clicked button(s)

Returns:    - csv file

'''
@callback(
    Output('download_df_csv', 'data'),
    Input("btn-download-24", 'n_clicks'),
    Input("btn-download-mov", 'n_clicks'),
    Input("btn-download-all", 'n_clicks'),
    State('load-graph', 'children'),
    prevent_initial_call=True,
)
def download_csv(btn24, btnmov, btnall, state):

    # If a button has been clicked extract id of current input being used
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    # Retrieve detector of choice
    detector = state[0]['props']['figure']['layout']['title']['text'].strip().split(':')[0].strip()
    # Get DF and filename
    df, filename = download_csvs(detector, button_id)
    # Return a csv for download
    return dcc.send_data_frame(df.to_csv, filename)



''' 
Callback for refreshing and displaying available history of 
actions performed for data collected.

Args:   - int 0 or 1 depending if user clicked button
        - Boolean True or False depending state of current collapsible
Returns:
        - Tuple [Bool, str]
'''
@callback(
    [
        Output('div-data-history-collapse', 'is_open'),
        Output('card-collapse-data-history', 'children')
    ],
    [Input('button-data-history', 'n_clicks')],
    [State('div-data-history-collapse', 'is_open')],
)
def callback_data_history(n, is_open):
    if n:
        if exists('./app_data/data_history.txt'):
            text_md = ''
            with open('./app_data/data_history.txt') as f:
                for line in f.read():
                    if '\n' in line:
                        text_md += '\n\n'
                    else:
                        text_md += line
            return [not is_open, text_md]
        return [not is_open, 'No updates available.']
    return [is_open, '']
