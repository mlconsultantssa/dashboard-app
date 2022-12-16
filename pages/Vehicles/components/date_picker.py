from dash import dcc 

def render(id):
    return dcc.DatePickerRange(id = id, style={'padding': '20px 0px', 'zIndex': 20})
    