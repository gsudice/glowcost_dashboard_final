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
                html.Img(src='assets/xhe.jpg'),
                html.Br(),
                html.Br(),
                html.H1('Xiachun He'),
                'Professor',
                html.Br(),
                'Department of Physics and Astrology',
                html.Br(),
                'Georgia State University',
                html.Br(),
                '29 Peachtree Center Ave., Suite 400',
                html.Br(),
                'Atlanta, GA 30303',
                html.Br(),
                'Email: ',
                html.A("xhe@gsu.edu", href='mailto:xhe@gsu.edu', target='_blank'),
                html.Br(),
                'Phone: (404) 413-6051',
                html.Br(),
                html.Br(),
                html.H4('Nuclear Physics Group @ GSU', style={'color':'coral'}), 
            ],
            className='text-center',
            style={'padding':'50px 10vh 50px 10vh'},
        ),
    ],
    fluid=True,
    className="dbc p-0 m-0",
)

