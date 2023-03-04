import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/', name='Home') # '/' is home page


layout = html.Div(
    [
        html.H1('Welcome to the APP'),
        html.H4('This app provides dashboard for analyzing metagrateds LRP data')
    ]
)