""" 
This module defines layout components for Dash application
"""
from dash import html, dcc
import dash_bootstrap_components as dbc
import pyfigure
from mapnav import map_display

# Create website main title
HTML_TITLE = html.Div(
    [
        html.H4(
            'Global CosmicRay Network for Space Weather Monitoring and STEM Outreach',
            className="float fw-bold text-left fw-bold",
            style={"color":'white'},
        ),
        html.Span(
            html.A(
                ['More info about our research at GSU Research Magazine'],
                href='https://news.gsu.edu/research-magazine/cosmic-rays-space-weather-and-larger-questions-about-the-universe',
                target='_blank',
            ),
            className="text-muted",
            style={'fontSize':'12px', 'padding-top':10}
        ),
    ],
    style={
        # "background-color": '#002379', 
        'padding':'40px 0px 20px 0px',
        'margin': '0px 0px 0px 0px'
    },
    id='div-title',
)

# Update report section
HTML_UPDATES = html.Div(
    [
        html.Div("Updated May 2019 by Xiaochun He"),
        html.Div(
            [
                "Nuclear Physics Group @ GSU (",
                html.A("xhe@gsu.edu", href='mailto:xhe@gsu.edu', target='_blank'),
                ")",
            ],
        )
    ],
    className="text-center",
    id='div-updates',
    style={
        'padding':'50px 10px 25px 10px',
    }
)

# Create website bottom title related to maintenance and version updates for web application
HTML_FOOTER = html.Div(
    [
        html.Div(
            [
                "Website development directed by ",
                html.A("Chetan Tiwari, Ph.D.", href="https://cas.gsu.edu/profile/chetan-tiwari/"),
                " and created and maintained by graduate researchers ",
                html.A("Sara Edwards", href="https://github.com/Sedwards8900"),
                " and ",
                html.A("Jean Guo", href="https://github.com/tguo4"),
                ".",
            ],
        ),
    ],
    className="text-muted text-center",
    id='div-footer',
    style={
        'padding':'25px 10px 25px 10px', 
        'background-color': 'whitesmoke',
        'position':'sticky',
        'top':'100%',
    }
)

HTML_NAVBAR = dbc.Navbar(
    dbc.Container(
        [   
            dbc.Row(
                [
                    dbc.Col(className='col-extra'),
                    dbc.Col(
                        dbc.NavbarToggler(
                            id="navbar-toggler", 
                            n_clicks=0,
                        ),
                    ),
                    dbc.Col(className='col-extra'),
                ],
                className="g-0",
            ),
            # dbc.NavbarToggler(
            #     id="navbar-toggler", 
            #     n_clicks=0,
            # ),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink('Home', href='/')),
                        dbc.NavItem(dbc.NavLink('Detectors', href='/detectors')),
                        # dbc.NavItem(dbc.NavLink('Liquid Scintillator', href='/scintillator')),
                        dbc.NavItem(dbc.NavLink('Collaborators', href='/collaborators')),
                        dbc.NavItem(dbc.NavLink('External Links', href='/external-links')),
                        dbc.NavItem(dbc.NavLink('Contact', href='/contact')),
                    ],
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
                style={
                    'min-width':'60%',
                }
            ),
        ],
        className='container-navbar',
        style={
            'padding':'6px 0px 0px 0px',
        },
    ),
    style={
        'padding':'6px 0px 0px 0px', 
    },
    dark=True,
    color='transparent',
    expand='md',
    className='navbar-base'
)


HTML_DATA_HISTORY = html.Div(
    [
        dbc.Button(
            'Data History',
            color='primary',
            outline=False,
            class_name='text-center',
            id='button-data-history',
            size='md',
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody(
                    dcc.Markdown(
                    id='card-collapse-data-history'
                    ),
                ),
            ),
            id='div-data-history-collapse',
            style={'paddingTop':10},
            is_open=False,
        ),
    ],
    style={'textAlign':'center', 'padding': '20px 0px 80px 0px'},
    id='div-data-history',
)


# Container display for map
HTML_MAPNAV = html.Div(
    [   
        html.H2(
            "Detector Locations Worldwide", 
            className="float fw-bold text-center",
            style={'padding':'0px 0px 20px 0px'},
        ),
        html.Div(
            [
                dcc.Graph(
                    figure=map_display(), 
                    id='map-plot', 
                    style={'height':250}
                ),
            ],
        )
    ],
    id='div-mapnav',
    style={'padding':'20px 20px 20px 20px'},
)


# Container display for graphs
HTML_GRAPHS = html.Div(
    [
        html.Div(
            [
                html.H5(
                    'Click detectors on the map to display real time data below',
                    className="float fw-bold text-center",
                    id='h-graph-title'
                ),
                html.H5(
                    id='h-warnings',
                    className="float text-center",
                    style={'color':'red', 'paddingTop':10},
                )
            ],
            style={'paddingTop': 10, 'paddingBottom':50, 'color':'dimgray'}
        ),
        html.Div(
            [
                dcc.Loading(
                    id = 'load-graph',
                    children = dcc.Graph(
                        id='graph-detector-display',
                        # Initial empty graph display bf user selects detector
                        figure=pyfigure.generate_empty_figure(),
                        config={'staticPlot':True},
                    )
                ),
                # Only shows if user wants dual display
                # ontains graph with data from second detector
                html.Div(
                    dcc.Loading(
                        id = 'load-graph2',
                        children = dcc.Graph(
                            id='graph-detector-display2',
                            # Initial empty graph display bf user selects detector
                            figure=pyfigure.generate_empty_figure(),
                            config={'staticPlot':True},
                        ),
                    ),
                    id='div-dual-detector',
                    style={'display':'none'},
                ),
            ],
        ),
        # Buttons for downloading data that become visible when user clicks on map detector
        html.Div(
            [
                dbc.Button(
                    "Download Data for Last 30 Days", 
                    id="btn-download-30", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download Moving Average Data", 
                    id="btn-download-mov", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download All Data", 
                    id="btn-download-all", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                    ),
                dcc.Download(id="download_df_csv"),
            ],
            style={'padding': '50px 0px 50px 0px'},
            className='gap-5 d-md-flex justify-content-center',
        ),
        html.H5(
            id='download-warnings',
            className="float text-center",
            style={'color':'red', 'paddingTop':10}
        ),
    ],
    id='div-detector-graph',
)

# Container display for map
HTML_DUAL_DET = html.Div(
    [
        html.H2(
            "Detector Location's Worldwide", 
            className="float fw-bold text-center",
            style={'padding':'0px 0px 20px 0px'},
        ),
        # Det 1 Row
        dbc.Row(
            [   dbc.Col(
                    html.H5(
                        "Choose Detector 1",
                        className="float fw-bold text-center",
                        style={'padding':'0px 0px 20px 0px'},
                    ),
                    style={'padding':'20px 0px 0px 0px'}
                ),
                dbc.Col(),
                dbc.Col(),
                dbc.Col(),
            ],
        ),
        dbc.Row(
            [   
                # Map for det 1
                dbc.Col(
                    [
                        
                        dcc.Graph(
                            figure=map_display(), 
                            id='map-plot', 
                            style={'height':200}
                        ),
                    ],
                    style={'padding':'50px 0px 0px 0px'},
                    width=3
                ),
                # Graph for det 1
                dbc.Col(
                    [
                        html.H5(
                            id='h-warnings',
                            className="float text-center",
                            style={'color':'red'},
                        ),
                        dcc.Loading(
                            id = 'load-graph',
                            children = dcc.Graph(
                                id='graph-detector-display',
                                # Initial empty graph display bf user selects detector
                                figure=pyfigure.generate_empty_figure(),
                                config={'staticPlot':True},
                            )
                        ),
                    ],
                ),
            ],
        ),
        # Det 2 Row
        dbc.Row(
            [   dbc.Col(
                    html.H5(
                        "Choose Detector 2",
                        className="float fw-bold text-center",
                        style={'padding':'0px 0px 20px 0px'},
                    ),
                    style={'padding':'40px 0px 0px 0px'}
                ),
                dbc.Col(),
                dbc.Col(),
                dbc.Col(),
            ],
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(
                            figure=map_display(), 
                            id='map-plot2', 
                            style={'height':200}
                        ),
                    ],
                    style={'padding':'50px 0px 0px 0px'},
                    width=3
                ),
                # Graph for det 2
                dbc.Col(
                    [
                        html.H5(
                            id='h-warnings2',
                            className="float text-center",
                            style={'color':'red', 'paddingTop':10},
                        ),
                        dcc.Loading(
                            id = 'load-graph2',
                            children = dcc.Graph(
                                id='graph-detector-display-2',
                                # Initial empty graph display bf user selects detector
                                figure=pyfigure.generate_empty_figure(),
                                config={'staticPlot':True},
                            )
                        ),
                    ],
                ),
            ],
        ),
        # Det 1 Download buttons
        html.Div(
            [   
                html.H5('Detector 1 Downloads'),
                dbc.Button(
                    "Download Data for Last 30 Days", 
                    id="btn-download-30", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download Moving Average Data", 
                    id="btn-download-mov", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download All Data", 
                    id="btn-download-all", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                    ),
                dcc.Download(id="download_df_csv"),
            ],
            style={'padding': '40px 0px 30px 0px'},
            className='gap-5 d-md-flex justify-content-center',
        ),
        html.H5(
            id='download-warnings',
            className="float text-center",
            style={'color':'red', 'paddingTop':10, 'paddingBottom':30}
        ),
        # Det 2 downloads
        html.Div(
            [   
                html.H5('Detector 2 Downloads'),
                dbc.Button(
                    "Download Data for Last 30 Days", 
                    id="btn-download-30-2", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download Moving Average Data", 
                    id="btn-download-mov-2", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                ),
                dbc.Button(
                    "Download All Data", 
                    id="btn-download-all-2", 
                    style = {'display':'none'},
                    color = 'secondary',
                    outline=False,
                    class_name='text-center',
                    size='md',
                    ),
                dcc.Download(id="download_df_csv-2"),
            ],
            style={'padding': '0px 0px 50px 0px'},
            className='gap-5 d-md-flex justify-content-center',
        ),
        html.H5(
            id='download-warnings-2',
            className="float text-center",
            style={'color':'red', 'paddingTop':10}
        ),
    ],
    id='div-dual-det',
    style={'padding':'20px 20px 50px 20px'},                        
)


HTML_ROW_OPTIONS_GRAPH_RAINFALL = html.Div(
    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Label("Small Dataset (<= 2,920 data points) Options:"),
                            dbc.RadioItems(
                                options=[
                                    {"label": "Stack", "value": "stack"},
                                    {"label": "Group", "value": "group"},
                                    {"label": "Line", "value": "line"},
                                ],
                                value="stack",
                                id="radio-graphbar-options",
                                inline=True,
                            ),
                        ],
                        width="auto",
                    )
                ],
                justify="center",
            )
        ],
        fluid=True,
        style={"visibility": "hidden"},
        id="container-graphbar-options",
    )
)