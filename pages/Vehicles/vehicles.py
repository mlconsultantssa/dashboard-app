
from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
from .components import licence_plate_dropdown, date_picker, mapper
dash.register_page(__name__, name = "Vehicles", path='/vehicles')

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    licence_plate_dropdown.render()
                ),
                dbc.Col(
                    date_picker.render()
                )
            ]
        ),
        dbc.Row(
            [
                mapper.render()
            ]
        )
    ]
)

