from dash import Dash, html, dcc 
from src.data_loader import load_data

def render(id):
    licence_plates = list(load_data()['number_plate'])
    #licence_plates = ['NPN22382', 'FNK478GP']

    return html.Div(
        children = [
            html.H6('Choose licence plate'),
            dcc.Dropdown(
                id = id,
                options=[{'label': licence_plate, 'value': licence_plate} for licence_plate in licence_plates],
                value = None,
                multi=True
            )
        ]
    )

