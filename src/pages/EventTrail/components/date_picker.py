from dash import dcc 
from . import ids
from datetime import date

def render(id):
    return dcc.DatePickerSingle(id=id, style={'padding': '20px 0px', 'zIndex': 20}, date=date(2022, 9, 1))