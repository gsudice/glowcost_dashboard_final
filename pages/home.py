import dash
from dash import html
import pylayout
import dash_bootstrap_components as dbc


dash.register_page(__name__, path='/')

layout = html.Div(
    [   
        pylayout.HTML_HEADER1,
        # Project description
        html.Div(
            [   
                dbc.Stack(
                    [
                        html.Div(
                            [
                                html.H2(
                                    ['The Problem'],
                                    className='text-center',
                                    style={'padding':'0px 0px 20px 0px'},
                                ),
                                html.Div(
                                    [
                                        "Current space weather monitoring is often expensive and inaccessible, leaving many communities vulnerable. Our cost-effective approach will improve predictions, mitigate risks, and build a more resilient future for all.",
                                    ],
                                    className='text-center',
                                    id='div-overview',
                                    # style={'padding':'20px 0px 70px 0px'},
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.H2(
                                    ['Our Solution'],
                                    className='text-center',
                                    style={'padding':'0px 0px 20px 0px'},
                                ),
                                html.Div(
                                    [
                                        "Our project aims to create a global network of affordable and sustainable cosmic ray detectors to monitor space weather and its effects on Earth. By expanding partnerships and providing accessible technology, we'll empower communities, especially in underserved regions, to participate in scientific research and education.",
                                    
                                    ],className='text-center',
                                    id='div-overview',
                                    # style={'padding':'20px 0px 70px 0px'},
                                ),
                            ],
                        ),
                        html.Div(
                            [
                                html.H2(
                                    ['Its Impact'],
                                    className='text-center',
                                    style={'padding':'0px 0px 20px 0px'},
                                ),
                                html.Div(
                                    [
                                        "This initiative will not only help mitigate the risks of severe space weather events but also foster global collaboration and inspire future generations of scientists and engineers to address shared challenges.",
                                    ],
                                    className='text-center',
                                    id='div-overview',
                                    # style={'padding':'20px 0px 70px 0px'},
                                ),
                            ],
                        ),
                    ],
                    style={'padding':'60px 0px 50px 0px'},
                    direction='horizontal',
                    gap=5,
                ),
                html.Hr(style = {'size' : '50', 'borderColor':'#332348','borderHeight': "10vh", "width": "95%",}),
                html.Div(
                    [
                        html.H3(
                            'Our Current Deployments',
                            className="float fw-bold text-center",
                            style={'padding':'0px 0px 20px 0px'},
                        ),
                        pylayout.HTML_MAPNAV2,
                    ],
                    style={'padding':'50px 0px 50px 0px'},
                ),
                html.Hr(style = {'size' : '50', 'borderColor':'#332348','borderHeight': "10vh", "width": "95%",}),
                html.H3(
                    ['Project Information Links'],
                    className='text-center',
                    style={'padding':'50px 0px 20px 0px'},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.A(
                                ['Additional technical info about our research'],
                                href='http://phynp6.phy-astr.gsu.edu/wordpress/index.php/research/cosmic-ray-science-at-gsu/',
                                target='_blank',
                            ),
                        ),
                        dbc.Col(
                            [
                                html.A(
                                    ["GSU Research Magazine's article"],
                                    href='https://news.gsu.edu/research-magazine/cosmic-rays-space-weather-and-larger-questions-about-the-universe',
                                    target='_blank',
                                ),
                            ],
                        ),
                    ],
                    className="text-muted text-center",
                    align='center',
                    justify='center',
                    style={
                        'fontSize':'20px',
                        'padding':'50px 0px 50px 0px'
                    }
                ),
                html.Hr(style = {'size' : '50', 'borderColor':'#332348','borderHeight': "10vh", "width": "95%",}),
                # pylayout.HTML_UPDATES,
            ],
            style={'padding':'0px 10vw 0px 10vw'},
        ),
    ],
    id='div-home-page',
    style={'padding':'0px 0px 0px 0px'},
)