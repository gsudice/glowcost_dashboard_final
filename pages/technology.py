import dash
from dash import html
import pylayout
import dash_bootstrap_components as dbc


dash.register_page(__name__)

layout = dbc.Container(
    [
        pylayout.HTML_HEADER2,
        html.Div(
            [
                html.H3(
                    ['Technology Advancing Our Research'],
                    className='text-center',
                    style={'padding':'50px 0px 0px 0px'},
                ),
                # Telescope
                html.Div(
                    [   
                        html.Div(
                            [
                                html.H5('Cosmic Ray Telescope'),
                                html.Div('A novel, portable and low-cost cosmic ray detector has been developed by the Nuclear Physics Group at Georgia State University. This detector is designed to measure cosmic ray muon and neutron flux variation simultaneously in time series. One of the major goals of this project is to install this detector around the world for monitoring cosmic ray flux variation at global scale for space and earth weather.'),
                            ],
                            className='div-description',
                            style={'width':'50%', 'padding':'30px 40px 0px 0px'}
                        ),
                        html.Img(src='assets/cosmicRayTelescopeDevelopment.png',
                            className='home-img',
                        ),
                    ],
                    style={'padding':'50px 0px 50px 0px','display':'flex', 'flex-direction':'row'},
                ),
                # Mark V
                html.Div(
                    [   
                        html.Div(
                            [
                                html.H5('Mark V Liquid Scintillator Prototype'),
                                html.Div('The Mark V liquid scintillator prototype is the fifth generation of cosmic ray neutron detectors developed by the Nuclear Physics Group at Georgia State University. This detector is designed to be installed in cosmic ray telescope frames.'),
                            ],
                            className='div-description',
                            style={'width':'50%', 'padding':'30px 40px 0px 0px'}
                        ),
                        html.Img(src='assets/MarkVDevelopment.png',
                            className='home-img',
                                #  style={'display':'flex', 'width':'50%'}
                        )
                    ],
                    style={'padding':'50px 0px 25px 0px','display':'flex', 'flex-direction':'row'},
                ),
                # Mark I
                html.Div(
                    [   
                        html.Div(
                            [
                                html.H5('Mark I Liquid Scintillator Prototype'),
                                html.Div('The Mark I liquid scintillator prototype is the first generation of cosmic ray neutron detectors developed by the Nuclear Physics Group at Georgia State University using a silicon photomultiplier and wavelength shifting fibers. '),
                            ],
                            className='div-description',
                            style={'width':'50%', 'padding':'30px 40px 0px 0px'}
                        ),
                        html.Img(src='assets/MarkIDevelopment.png',
                            className='home-img',
                                #  style={'display':'flex', 'width':'50%'}
                        )
                    ],
                    style={
                        'padding':'50px 0px 25px 0px',
                        'display':'flex', 
                        'flex-direction':'row'
                    },
                ),
            ],
            style={'padding':'0px 10vw 50px 10vw'},
        ),
        html.Hr(style = {'size' : '50', 'borderColor':'#332348','borderHeight': "10vh", "width": "95%",}),
    ],
    fluid=True,
    className='dbc p-0 m-0',
)