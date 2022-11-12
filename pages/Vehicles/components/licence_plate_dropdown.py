from dash import Dash, html, dcc 
from . import ids

def render():
    licence_plates = ['dsdd', 'jkhjjds']
    return html.Div(
        children = [
            html.H6('Choose licence plate'),
            dcc.Dropdown(
                id = ids.LICENCE_PLATE_DROPDOWN,
                options=[{'label': licence_plate, 'value': licence_plate} for licence_plate in licence_plates],
                value = licence_plates,
                multi=True
            )
        ]
    )

