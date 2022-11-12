from dash import Dash, html, dcc 
from . import ids
from datetime import date

def render():
    return dcc.DatePickerRange(ids.DATE_PICKER, initial_visible_month=date(2017, 8, 5),
        end_date=date(2017, 8, 25), style={'padding': '20px 0px', 'zIndex': 20})
    