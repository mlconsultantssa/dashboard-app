from dash import Dash, html, dcc 
from package.data_loader import load_data

def render(id):
    clients = ['one-space-11', 'vumacam-14', 'itrack-21', 'navic-5', '-20', '-9', 'alpha-security-group-12', '-7', '-10', 'watcher-22', '-17', 'nimbus-24', 'cloudsell-25', '-8', 'maxi-security-18' ]

    return html.Div(
        children = [
            html.H6('Choose client'),
            dcc.Dropdown(
                id = id,
                options=[{'label': client, 'value': client} for client in clients],
                value = None,
                multi=True
            )
        ]
    )