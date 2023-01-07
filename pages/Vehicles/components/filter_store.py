from dash import dcc
from . import ids

def render():
    initial_data = {
        'number_plate': '',
        'start_data': '',
        'end_date': ''
    }

    return dcc.Store(id=ids.FILTER_STORE, data=initial_data)
