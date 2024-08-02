import dash
from dash import html
from os.path import exists
import dash_bootstrap_components as dbc

dash.register_page(__name__)

# Extract links
content = {}
if exists('./app_data/links.txt'):
    f = open('./app_data/links.txt')
    while True:
        key = f.readline()
        l = f.readline()

        if not key:
            break

        content[key] = l
    f.close()
if len(content) == 0:
    content = {'No available links at this time':''}

# World data centers
content2 = {}
if exists('./app_data/wdc.txt'):
    f = open('./app_data/wdc.txt')
    while True:
        key = f.readline()
        l = f.readline()

        if not key:
            break

        content2[key] = l
    f.close()
if len(content2) == 0:
    content2 = {'No available links at this time':''}

# Returns html.A link container
def generate_link(key_l, txt_l):
    return html.A(key_l, href=txt_l, target='_blank')

# Set up layout
layout = html.Div(
    [   
        html.Div(
            [
                
                html.H1('Cosmic Ray Data Links'),
                html.Br(),
                dbc.Row([generate_link(key_l, content[key_l]) for key_l in content]),
            ],
            style={'padding':'0px 0px 25px 0px'},
        ),
        html.Div(
            [
                html.H1('World Data Centers'),
                html.Br(),
                dbc.Row([generate_link(key_l, content2[key_l]) for key_l in content2]),
            ],
            style={'padding':'25px 0px 0px 0px'},
        ),
    ],
    className='text-center',
    style={'padding':'50px 10px 25px 10px'},
)