import dash
from dash import callback, html, Input, Output, State, dcc, ctx
import dash_bootstrap_components as dbc
import pylayout
from os.path import exists
dash.register_page(__name__)
import pandas as pd
import pyfigure
from datetime import datetime, timedelta
from io import StringIO

layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Button(
                    'Display Two Detectors',
                    id='btn-dual-detector',
                    n_clicks=0,
                    color = 'success',
                    outline=True,
                    class_name='text-center',
                    size='md',
                ),
            ],
            style={'paddingTop': 50, 'paddingRight':20, 'paddingBottom':0},
            className='d-md-flex justify-content-end',
        ),
        html.Div(
            children= [   
                pylayout.HTML_MAPNAV,
                pylayout.HTML_GRAPHS,
            ],
            id='div-det-display'
        ),
        pylayout.HTML_DATA_HISTORY,
        dcc.Store(id='graph1-df'),
        dcc.Store(id='graph2-df'),
    ],
    fluid=True,
    className="dbc",
    style={
        "padding": "0px 0px 0px 0px", 
        'margin':"0px 0px 0px 0px" # Quick fix: Need to figure out why random space 
        # between page and browser on top
    },
)
''' 
Callback to display two detector graphs instead of one

Args:       - int 0 or 1 depending if user clicked button

Returns:     - Tuple [
                    html.Button text object,
                    dcc.Button style dictionary,
                    dcc.Button style dictionary,
                ]
'''
@callback(
    [
        Output('btn-dual-detector', 'children'),
        Output('div-det-display', 'children'),
    ],
    Input('btn-dual-detector', 'n_clicks'),
    prevent_initial_call=True,
)
def dual_detector(n_clicks):
    if n_clicks:
        # Cast string clicks into int number
        n_clicks = int(n_clicks)
        print('nclicks: ', n_clicks)

        if n_clicks % 2 == 0:
            content='Display Two Detectors'
            layout = [pylayout.HTML_MAPNAV, pylayout.HTML_GRAPHS]
        else:
            content='Display One Detector'
            layout = pylayout.HTML_DUAL_DET

        return [content, layout]
    else:
        return dash.no_update


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
        ]
'''
@callback(
    [
        Output('h-warnings', 'children'),
        Output('load-graph','children'),
        Output('graph1-df', 'data'),
        Output("btn-download-30", 'style'),
        Output("btn-download-mov", 'style'),
        Output("btn-download-all", 'style'),
    ],
    Input('map-plot','clickData'),
    State('map-plot', 'map'),
    prevent_initial_call=True
)
def update_graph(clickData, state):

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
        if button_id == 'map-plot':
            
            fig, data_df = pyfigure.update_detector_figure(detector_name, detector)

            
        # Notify user if graph can be reproduced via title change and 
        # Set up additional buttons for display accordingly
        if fig != None:
            detector_graph = dcc.Graph(
                        id='graph-detector-display',
                        # Initial empty graph display bf user selects detector
                        figure=fig,
            ),

            if not data_df.empty:
                json_data = data_df.to_json()
            else:
                json_data = None

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
            json_data = None
        
        return [
            title, 
            detector_graph,
            json_data,
            style, 
            style, 
            style, 
        ]
    # else, no update occurs
    return dash.no_update

''' 
Callback for displaying graph # 2 of selected detector data when dual detector
displaying

Args:   - int 0 or 1 depending if user clicked button

Returns:
        - Tuple [
            html.H2 header object,
            ggc.Graph object,
            dcc.Button style dictionary,
            dcc.Button style dictionary,
            dcc.Button style dictionary,
        ]
'''
@callback(
    [
        Output('h-warnings2', 'children'),
        Output('load-graph2','children'),
        Output('graph2-df', 'data'),
        Output("btn-download-30-2", 'style'),
        Output("btn-download-mov-2", 'style'),
        Output("btn-download-all-2", 'style'),
    ],
    Input('map-plot2','clickData'),
    State('map-plot2', 'map'),
    prevent_initial_call=True
)
def update_graph(clickData, state):

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
        if button_id == 'map-plot2':
            
            fig, data_df = pyfigure.update_detector_figure(detector_name, detector)

            
        # Notify user if graph can be reproduced via title change and 
        # Set up additional buttons for display accordingly
        if fig != None:
            detector_graph = dcc.Graph(
                        id='graph-detector-display-2',
                        # Initial empty graph display bf user selects detector
                        figure=fig,
            ),

            if not data_df.empty:
                json_data = data_df.to_json()
            else:
                json_data = None

            title = None
            style = {}
        else:
            # In case data is not available, revert to empty figure display
            detector_graph = dcc.Graph(
                        id='graph-detector-display-2',
                        # Initial empty graph display bf user selects detector
                        figure=pyfigure.generate_empty_figure(),
                        config={'staticPlot':True},
            ),
            title = f'Data for {detector} Detector Not Available at This Time. Try again.'
            style = {'display':'none'}
            json_data = None
        
        return [
            title, 
            detector_graph,
            json_data,
            style, 
            style, 
            style, 
        ]
    # else, no update occurs
    return dash.no_update


''' 
Callback to handle download data requests depending on prefered type

Args:   - int 0 or 1 depending if user clicked button(s)

Returns:    - csv file

'''
@callback(
    Output('download-warnings', 'children'),
    Output('download_df_csv', 'data'),
    [   
        Input('graph1-df','data'),
        Input("btn-download-30", 'n_clicks'),
        Input("btn-download-mov", 'n_clicks'),
        Input("btn-download-all", 'n_clicks'),
    ],
    State('load-graph', 'children'),
    prevent_initial_call=True,
)
def download_csv(json_data, btn24, btnmov, btnall, state):

    # If a button has been clicked extract id of current input being used
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    
    # List of buttons for sorting task
    download_buttons = ["btn-download-30", "btn-download-mov", "btn-download-all"]
    
    if button_id in download_buttons:
        text = None
        # Retrieve detector name
        detector_name = state[0]['props']['figure']['layout']['title']['text'].strip().split(':')[0].strip()

        # Read json data from dcc.Store
        df = pd.read_json(StringIO(json_data))
        print(df.iloc[0].name)
        print(type(df.iloc[0].name))

        # Trim based on request
        if button_id == "btn-download-all":
            final_df = df
            filename = f'{detector_name}_all_data.csv'

        elif button_id == "btn-download-30":
            # Get current datetime and 30 days prior
            today = datetime.now()
            day30 = today - timedelta(30)

            # Slice df
            final_df = df.loc[:day30]

            filename = f'{detector_name}_30days_data.csv'

        else: # button_id == "btn-download-mov":
            # Slice df
            final_df = df.loc[:,'hourly_average']
            filename = f'{detector_name}_hourly_moving_ave_data.csv'

        if final_df.empty:
            final_df = None
            filename = ''
            text = f'Unable to download data'

        # Return a csv for download
        return [text, dcc.send_data_frame(final_df.to_csv, filename)]
    
    else:
        return dash.no_update


''' 
Callback # 2 to handle download data requests depending on prefered type
for detector 2 when dual detector display is chosen

Args:   - int 0 or 1 depending if user clicked button(s)

Returns:    - csv file

'''
@callback(
    Output('download-warnings-2', 'children'),
    Output('download_df_csv-2', 'data'),
    [   
        Input('graph2-df','data'),
        Input("btn-download-30-2", 'n_clicks'),
        Input("btn-download-mov-2", 'n_clicks'),
        Input("btn-download-all-2", 'n_clicks'),
    ],
    State('load-graph2', 'children'),
    prevent_initial_call=True,
)
def download_csv(json_data, btn24, btnmov, btnall, state):

    # If a button has been clicked extract id of current input being used
    button_id = ctx.triggered_id if not None else 'No clicks yet'
    
    # List of buttons for sorting task
    download_buttons = ["btn-download-30-2", "btn-download-mov-2", "btn-download-all-2"]
    
    if button_id in download_buttons:
        text = None
        # Retrieve detector name
        detector_name = state[0]['props']['figure']['layout']['title']['text'].strip().split(':')[0].strip()

        # Read json data from dcc.Store
        df = pd.read_json(StringIO(json_data))
        print(df.iloc[0].name)
        print(type(df.iloc[0].name))

        # Trim based on request
        if button_id == "btn-download-all-2":
            final_df = df
            filename = f'{detector_name}_all_data.csv'

        elif button_id == "btn-download-30-2":
            # Get current datetime and 30 days prior
            today = datetime.now()
            day30 = today - timedelta(30)

            # Slice df
            final_df = df.loc[:day30]

            filename = f'{detector_name}_30days_data.csv'

        else: # button_id == "btn-download-mov":
            # Slice df
            final_df = df.loc[:,'hourly_average']
            filename = f'{detector_name}_hourly_moving_ave_data.csv'

        if final_df.empty:
            final_df = None
            filename = ''
            text = f'Unable to download data'

        # Return a csv for download
        return [text, dcc.send_data_frame(final_df.to_csv, filename)]
    
    else:
        return dash.no_update


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
