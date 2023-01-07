
from dash import html, callback, Output, Input, State
import dash
import dash_bootstrap_components as dbc

from .components import licence_plate_dropdown, date_picker, ids, vehicle_event_map, filter_store
from src.db.queries import load_distinct_vehicles, VehicleEventQueryBuilder
from src.data_processor import VehicleEventDataProcessor

dash.register_page(__name__, name = "Vehicles", path='/vehicles')

layout = html.Div(
    [
        filter_store.render(),
        dbc.Row(
            [
                dbc.Col(
                    licence_plate_dropdown.render()
                ),
                dbc.Col(
                    date_picker.render()
                )
            ]
        ),
        dbc.Row(
            [
                vehicle_event_map.render()
            ]
        )
    ]
)

@callback(
    Output(ids.LICENCE_PLATE_DROPDOWN, 'options'),
    Input(ids.LICENCE_PLATE_DROPDOWN + '-initial-loader', 'children')
)
def initial_load(_):
    vehicles = load_distinct_vehicles()
    return vehicles

@callback(
    Output(ids.FILTER_STORE, 'data'),
    State(ids.FILTER_STORE, 'data'),
    Input(ids.LICENCE_PLATE_DROPDOWN, 'value'),
    Input(ids.DATE_PICKER, 'start_date'),
    Input(ids.DATE_PICKER, 'end_date'),
)
def update_store(data,
    licence_plate_dropdown_input_value,
    date_picker_input_start_date,
    date_picker_input_end_date):

    data['number_plate'] = licence_plate_dropdown_input_value or ''
    data['start_date'] = date_picker_input_start_date or ''
    data['end_date'] = date_picker_input_end_date or ''

    return data

@callback(
    Output(ids.MAP_GROUP_LAYER, 'children'),
    Input(ids.FILTER_STORE, 'data')
    )
def update_map(input_value):
    vehicle_event_query_builder = VehicleEventQueryBuilder()

    if input_value['number_plate'] != '':
        print(input_value['number_plate'])
        vehicle_event_query_builder.filter_events_on_number_plate(input_value['number_plate'])

    if input_value['start_date'] != '':
        vehicle_event_query_builder.filter_events_on_start_date(input_value['start_date'])

    if input_value['end_date'] != '':
        vehicle_event_query_builder.filter_events_on_end_date(input_value['end_date'])

    camera_events = vehicle_event_query_builder.execute()
    vehicle_event_data_processor = VehicleEventDataProcessor(camera_events)

    vehicle_event_data_processor.fix_bad_coordinates().generate_points()
    return vehicle_event_map.generate_markers(vehicle_event_data_processor.events)
