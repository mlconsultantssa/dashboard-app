from dash import Dash, html, dcc 
from src.data_loader import load_data

def render(id):
    clients = list(load_data()['camera_id'].unique())
    #licence_plates = ['NPN22382', 'FNK478GP']

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