#https://www.youtube.com/watch?v=XOFrvzWFM7Y


from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
from .components import client_dropdown, mapper, date_picker
from src.data_loader import load_data

from datetime import date

from dash import Dash, html, dcc 

from datetime import date
dash.register_page(__name__, name = 'Clients', path='/clients')

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    client_dropdown.render(id='client-dropdown')
                ),
                dbc.Col(
                    date_picker.render(id='date-picker-client')
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    mapper.render(id='mapper-client')
                )
            ]
        )
    ]
)


#https://dash.plotly.com/basic-callbacks
@callback(
    Output(component_id='mapper-client', component_property='children'),
    Input(component_id='date-picker-client', component_property='start_date'),
    Input(component_id='date-picker-client', component_property='end_date'),
    Input(component_id='client-dropdown',component_property='value')
)
def update_map(start_date, end_date, clients):
    mapper_ = mapper.Mapper(load_data()).clean()
    print(start_date, end_date, clients)

    if clients != None:
         mapper_.filter_events_on_clients(clients)

    if start_date != None:
        mapper_.filter_events_on_start_date(start_date)

    if end_date != None:
        mapper_.filter_events_on_end_date(end_date)

    mapper_.generate_points().generate_color()

    return mapper_.get_markers()

