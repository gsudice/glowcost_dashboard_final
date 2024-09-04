"""Main Dash App for Rainfall Analysis"""
from dash import Dash, html
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
        dbc.Row(
            [
                pylayout.HTML_TITLE,
                dbc.Row(
                    [
                        dbc.Col(className='col-extra-largeview'), # Without this empty col, the alignment setting won't work for large screen
                        dbc.Col(
                            pylayout.HTML_NAVBAR, 
                            className='col-navbar', 
                            align='end',
                        ),
                        dbc.Col(className='col-extra'), # Without this empty col, the alignment setting won't work for reduced screen size
                    ],
                    justify='end',
                    align='end',
                    className="g-0 row-navbar",
                    id='',
                ),

                dbc.Row(
                    [
                        dbc.Col(width={'size':2}),
                        dbc.Col(
                            [
                                Svg(
                                    [
                                        'assets/bg-header-wave.svg',
                                    ],
                                    width='1200',
                                    fill='#F1F2F4',
                                    height='30',
                                    viewBox='0 0 1200 30',
                                    preserveAspectRatio='none',
                                ),
                                # html.Img(
                                #     src='assets/bg-header-wave.svg',
                                #     style={
                                #         'fill':'white',
                                #         'color':'white',
                                #         # 'width':'100%','height':'110%'
                                #     },
                                # ),
                            ],
                            width={'size':6},
                        ),
                        dbc.Col(width={'size':2}),
                    ],
                    id='row-navbar-wave',
                    className="g-0",
                ),
            ],
            id='row-navbar-styling-container',
            className="g-0",
            style={
                'padding':'0px 100px 0px 100px',
                "background-image": "url('assets/bg1.png')",
                "background-repeat":'no-repeat',
                "background-color": '#332348'
            }
        ),
        html.Div(
            [
                dash.page_container,
            ],
            className='div-multipage-content',
            style={'padding':'0px 100px 0px 100px'},
        ),
        pylayout.HTML_FOOTER,
    ],
    fluid=True,
    className="dbc",
    style={
        'min-height':'100vh',
        "padding": "0px 0px 0px 0px", 
        'margin':"-16px 0px 0px 0px" # Quick fix: Need to figure out why random space 
        # between page and browser on top
    },
)

if __name__ == "__main__":
    # app.run_server(host='0.0.0.0')
    app.run_server(debug=DEBUG)