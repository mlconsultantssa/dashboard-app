#https://www.youtube.com/watch?v=XOFrvzWFM7Y

from dash import Dash, html
import dash

dash.register_page(__name__, name = 'Clients', path='/clients')

def layout():
    return html.Div(
        className = "app-div",
        children = [
            html.H1('huhi'),
            html.Hr()
        ]
    )