from dash import html, dcc 
from . import ids

def render():
    licence_plates = ['JD79WMGP']
    return html.Div(
        children = [
            html.H6('Choose licence plate'),
            dcc.Loading(
                parent_className='loading_wrapper',
                children=(
                    dcc.Dropdown(
                        id = ids.LICENCE_PLATE_DROPDOWN,
                        options=[],
                        value = licence_plates,
                        multi=True
                    )
                ),
                style={'zIndex': 10}
            ),
            html.Div(id=ids.LICENCE_PLATE_DROPDOWN + '-initial-loader')
        ]
    )
