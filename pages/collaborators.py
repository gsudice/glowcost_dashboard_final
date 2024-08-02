import dash
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.H1('Collaborators'),
        html.Div('Special thanks to all the contributors making this research project possible, including: ')
    ],
    className='text-center',
    style={'padding':'50px 10px 25px 10px'},
)