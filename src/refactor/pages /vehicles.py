from dash import Dash, html
import dash

dash.register_page(__name__)

def layout(app: Dash) -> html.Div:
    return html.Div(
        className = "app-div",
        children = [
            html.H1(app.title),
            html.Hr()
        ]
    )