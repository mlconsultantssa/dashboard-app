#https://www.youtube.com/watch?v=XOFrvzWFM7Y


from dash import html, callback, Output, Input, dcc
import dash
import dash_bootstrap_components as dbc
from .components import client_camera_map, client_dropdown, date_picker, camera_number_estimate, client_nan_graph
from src.db.queries import ClientCameraQueryBuilder
from src.data_processor import ClientCameraDataProcessor

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
                    client_camera_map.render(id='mapper-client')
                ),
                dbc.Col([
                    dbc.Row(camera_number_estimate.render(id='client_cam_count')),
                    dbc.Row(client_nan_graph.render(id='client_nan_graph'))
            ])
            ]
        )
    ]
)



@callback(
    Output(component_id='mapper-client', component_property='children'),
    Input(component_id='date-picker-client', component_property='start_date'),
    Input(component_id='date-picker-client', component_property='end_date'),
    Input(component_id='client-dropdown',component_property='value')
)
def update_map(start_date, end_date, clients):
    client_camera_query_builder = ClientCameraQueryBuilder()

    if clients:
        clients = [i[-2:].replace('-', '') for i in clients]
        client_camera_query_builder.filter_events_on_clients(clients)

    if start_date:
        client_camera_query_builder.filter_events_on_start_date(start_date)

    if end_date:
        client_camera_query_builder.filter_events_on_end_date(end_date)

    camera_events = client_camera_query_builder.execute()
    client_camer_data_processor = ClientCameraDataProcessor(camera_events)

    client_camer_data_processor.fix_bad_coordinates().generate_points()
    return client_camera_map.generate_markers(client_camer_data_processor.events)

@callback(
    Output(component_id='client_cam_count', component_property='children'),
    Input(component_id='date-picker-client', component_property='start_date'),
    Input(component_id='date-picker-client', component_property='end_date'),
    Input(component_id='client-dropdown',component_property='value')
)
def update_map(start_date, end_date, clients):
    client_camera_query_builder = ClientCameraQueryBuilder()

    if clients:
        clients = [i[-2:].replace('-', '') for i in clients]
        client_camera_query_builder.filter_events_on_clients(clients)

    if start_date:
        client_camera_query_builder.filter_events_on_start_date(start_date)

    if end_date:
        client_camera_query_builder.filter_events_on_end_date(end_date)

    camera_events = client_camera_query_builder.execute()
    client_camer_data_processor = ClientCameraDataProcessor(camera_events)

    count = len(client_camer_data_processor.fix_bad_coordinates().events)
    return count

