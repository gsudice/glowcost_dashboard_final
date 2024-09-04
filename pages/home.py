import dash
from dash import html
import pylayout

dash.register_page(__name__, path='/')

layout = html.Div(
    [   
        html.H1(
            ['Our Project'],
            className='text-center',
            style={'padding':'20px 0px 20px 0px'},
        ),
        html.Div(
            [
                'Here goes content'
            ],
            className='text-center',
            id='div-overview',
            style={'padding':'20px 0px 20px 0px'},
        ),
        html.Div(
            [   
                # Video header and video container
                html.H3(
                ['Learn More About our Project'],
                className='text-center',
                style={'padding':'20px 0px 20px 0px'},
                ),
                html.Div(
                    [
                        html.Iframe(
                            id='intro_video',
                            src="https://www.youtube.com/embed/ClRUcufp28E?si=42Dwl07dS9Miry72",
                            style={
                                'width':'70vh',
                                'height':'40vh',
                                'display':'block',
                                'margin':'auto',
                            },
                        ),
                        # html.Video(
                        #     controls=True,
                        #     id='intro_video',
                        #     src='https://youtu.be/FsrMPexJkI4?si=5Qgh01PwrRt88i5j',
                        #     autoPlay=False
                        # ),
                    ],
                    style={'text-align':'center'},
                ),
            ],
            id='div-video',
            className='justify-content-center',
            style={
                'background-color': 'whitesmoke',
                'padding':'10px 0px 40px 0px', 
                'display':'block', 
                'margin':'auto',
                'text-align':'center'
            },
        ),
        html.H3(
            ['Devices Advancing Our Research'],
            className='text-center',
            style={'padding':'40px 0px 0px 0px'},
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
                )
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
            style={'padding':'50px 0px 25px 0px','display':'flex', 'flex-direction':'row'},
        ),
        pylayout.HTML_UPDATES,
    ],
    style={'padding':'10px 20px 10px 20px'},
)