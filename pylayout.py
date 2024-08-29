""" 
This module defines layout components for Dash application
"""

from dash import html, dcc
from pyconfig import appConfig
import dash_bootstrap_components as dbc
import pyfigure
from mapnav import map_display

# Create website main title
HTML_TITLE = html.Div(
    [
        html.H4(
            appConfig.DASH_APP.APP_TITLE,
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
                "Website created and maintained by graduate researchers ",
                html.A("Sara Edwards", href="https://github.com/Sedwards8900"),
                " and ",
                html.A("Jean Guo", href="https://github.com/tguo4"),
                ",",
            ],
        ),
        html.Div(
            [
                " directed by ",
                html.A("Chetan Tiwari, Ph.D.", href="https://cas.gsu.edu/profile/chetan-tiwari/"),
                ", Director of ",
                html.A(
                    "Disaster Informatics and Computational Epidemiology (DICE)", 
                    href="https://gsudice.dataconn.net/"
                ),
                ' Lab.',
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
        html.H2("Detector Location's Worldwide", className="float fw-bold text-center",),
        dcc.Graph(figure=map_display(), id='map_plot', style={'height':300})
    ],
    id='div-mapnav',
    style={'padding':'80px 20px 80px 20px'},
)


# Container display for graphs
HTML_GRAPHS = html.Div(
    [
        html.Div(
            [
                html.H4(
                    'Click detectors on the map to display real time data below',
                    className="float fw-bold text-center",
                    id='h2-graph-title'
                ),
            ],
            style={'paddingTop': 10, 'paddingBottom':10}
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Button(
                            'Toggle Moving Average',
                            id='toggle-moving-average',
                            n_clicks=0,
                            style = {'display':'none'},
                            color = 'success',
                            outline=False,
                            class_name='text-center',
                            size='md',
                        ),
                    ],
                    className='d-md-flex justify-content-end',
                ),
                # Contains graph with data from detector
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
        # Buttons for downloading data that become visible when user clicks on map detector
        html.Div(
            [
                dbc.Button(
                    "Download Data for Last 24h", 
                    id="btn-download-24", 
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
    ],
    id='div-detector-graph',
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