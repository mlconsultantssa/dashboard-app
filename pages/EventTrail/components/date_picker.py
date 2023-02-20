from dash import dcc 
from . import ids

def render(id):
    return dcc.DatePickerSingle(id=id, style={'padding': '20px 0px', 'zIndex': 20})
    