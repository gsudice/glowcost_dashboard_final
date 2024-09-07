import dash
from dash import html
import pylayout

dash.register_page(__name__)

layout = html.Div(
    [   
        pylayout.HTML_HEADER2,
        html.H1('Collaborators'),
        html.Div('Special thanks to all the contributors making this research project possible, including: ')
    ],
    className='text-center',
    style={'padding':'50px 10px 25px 10px'},
)