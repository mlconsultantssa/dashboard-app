from dash import html, dcc 
from . import ids

def render(id):
    licence_plates = 'JD79WMGP'
    return html.Div(
        children = [
            html.H6('Choose licence plate'),
            dcc.Loading(
                parent_className='loading_wrapper',
                children=(
                    dcc.Dropdown(
                        id = id,
                        options=[],
                        value = licence_plates
                    )
                ),
                style={'zIndex': 10}
            ),
            html.Div(id=ids.LICENCE_PLATE_DROPDOWN + '-initial-loader')
        ]
    )
