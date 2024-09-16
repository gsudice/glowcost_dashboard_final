"""Main Dash App for Rainfall Analysis"""
from dash import Dash, Input, Output, State
import dash
import dash_bootstrap_components as dbc
from dash_svg import Svg, G, Path
# from pyconfig import appConfig
import pylayout

# Dash app config
APP_TITLE = 'Global CosmicRay Network for Space Weather Monitoring and STEM Outreach'
UPDATE_TITLE = 'Updating...'
DEBUG = 'TRUE'
THEME = 'LITERA' # Web app theme selection

# App initiation
app = Dash(
    APP_TITLE,
    use_pages=True,
    external_stylesheets=[getattr(dbc.themes, THEME)],
    title=APP_TITLE,
    update_title=UPDATE_TITLE,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
    suppress_callback_exceptions=True,
)
server = app.server


# Layout creation based on container with various divs for sections of webpage
# This one loads all pages and keeps consistent header and navbar
app.layout = dbc.Container(
    [
        dash.page_container,
        pylayout.HTML_FOOTER,
    ],
    fluid=True,
    className="dbc",
    style={
        'background-color':'#f3f3f3',
        'min-height':'100vh',
        'width':'100%',
        'max-width':'100%',
        "padding": "0px 0px 0px 0px", 
        'margin':"-16px 0px 0px 0px" # Quick fix: Need to figure out why random space 
        # between page and browser on top
    },
    id='container-base-app'
)

''' 
Callback for displaying toogle options when navbar is small due to small screen format

'''
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    # app.run_server(host='0.0.0.0')
    app.run_server(debug=DEBUG)