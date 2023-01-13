
from dash import html, callback, Output, Input
import dash
import dash_bootstrap_components as dbc

from .components import licence_plate_dropdown, date_picker, ids, vehicle_event_map
from src.db.queries import load_distinct_vehicles, VehicleEventQueryBuilder
from src.data_processor import VehicleEventDataProcessor

dash.register_page(__name__, name = "Vehicles", path='/vehicles')

layout = html.Div(
    [
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
    Output(ids.MAP_GROUP_LAYER, 'children'),
    Input(component_id=ids.DATE_PICKER, component_property='start_date'),
    Input(component_id=ids.DATE_PICKER, component_property='end_date'),
    Input(component_id=ids.LICENCE_PLATE_DROPDOWN, component_property='value')
    )
def update_map(start_date, end_date, number_plates):
    vehicle_event_query_builder = VehicleEventQueryBuilder()

    if number_plates:
        vehicle_event_query_builder.filter_events_on_number_plate(number_plates)

    if start_date:
        vehicle_event_query_builder.filter_events_on_start_date(start_date)

    if end_date:
        vehicle_event_query_builder.filter_events_on_end_date(end_date)

    camera_events = vehicle_event_query_builder.execute()
    vehicle_event_data_processor = VehicleEventDataProcessor(camera_events)

    vehicle_event_data_processor.fix_bad_coordinates().generate_points()
    return vehicle_event_map.generate_markers(vehicle_event_data_processor.events)
