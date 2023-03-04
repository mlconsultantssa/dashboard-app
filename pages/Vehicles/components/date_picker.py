from dash import dcc 
from . import ids

def render():
    return dcc.DatePickerRange(id=ids.DATE_PICKER, style={'padding': '20px 0px', 'zIndex': 20})
    