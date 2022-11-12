from dash import Dash, html
import dash

dash.register_page(__name__)

def layout():
    return html.Div(
        className = "app-div",
        children = [
            html.H1('huhi'),
            html.Hr()
        ]
    )