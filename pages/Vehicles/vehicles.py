
from dash import Dash, html
import dash
from .components import licence_plate_dropdown
dash.register_page(__name__)


def layout():
    return html.Div(
        className = "app-div",
        children = [
            html.H1('Metagrated dashboard'),
            html.Hr(),
            html.Div(
                children = [
                    licence_plate_dropdown.render()
                ]
            )
        ]
    )
