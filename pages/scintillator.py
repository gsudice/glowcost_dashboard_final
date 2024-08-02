import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1('Liquid Scintillator'),
        html.Div(
            [
                html.Br(),
                'A test stand for a Liquid Scintillator is ...',
                html.Br(),
                html.Br(),
                html.Br(),
                'Available below are test stands within different timeframes.',
            ],
        )
    ],
    className='text-center',
    style={'padding':'50px 10px 25px 10px'},
)