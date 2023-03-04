
from dash import html, callback, Output, Input, ctx, State, MATCH, ALL, no_update, dcc, DiskcacheManager
import dash
import dash_bootstrap_components as dbc
import plotly.express as px

from .components import licence_plate_dropdown, date_picker, ids, vehicle_event_map
from package.db.queries import load_distinct_vehicles, VehicleEventQueryBuilder, load_vehicle_histogram_data, load_daily_vehicle_histogram_data, load_all_events
from package.data_processor import VehicleEventDataProcessor

import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

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
        ),
        html.Div('histrogram', id='histrogram'),
        html.Div('daily-histogram', id='daily-histogram'),
        html.Div('events-list', id='events_list'),
    ]
)

@callback(
    Output(ids.LICENCE_PLATE_DROPDOWN, 'options'),
    Input(ids.LICENCE_PLATE_DROPDOWN + '-initial-loader', 'children'),
    background=True,
    manager=background_callback_manager
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

@callback(
    [
        Output('histrogram', 'children'),
        Output('daily-histogram', 'children'),
        Output('events_list', 'children'),
    ],
    Input({'type': 'circle-marker', 'index': ALL}, 'n_clicks'),
    Input(component_id=ids.DATE_PICKER, component_property='start_date'),
    Input(component_id=ids.DATE_PICKER, component_property='end_date'),
    Input(component_id=ids.LICENCE_PLATE_DROPDOWN, component_property='value')
)
def update_histogram(clicks, start_date, end_date, number_plates):
    trigger = ctx.triggered_id
    if trigger and 'type' in trigger and trigger['type'] == 'circle-marker' and clicks != [None] * len(clicks):
        coords = trigger['index'].split('_')
        data = load_vehicle_histogram_data(coords[0], coords[1])
        fig = px.histogram(data, x='day', y='size')
        fig.update_layout(bargap=0.2)
        fig.update_traces(xbins_size=86400000)

        data_daily = load_daily_vehicle_histogram_data(coords[0], coords[1])
        fig_daily = px.histogram(data_daily, x='hour', y='size')
        fig_daily.update_layout(bargap=0.2)

        data_list = load_all_events(coords[0], coords[1], start_date, end_date, number_plates)

        return dcc.Graph(figure=fig), dcc.Graph(figure=fig_daily), [html.H3(f'Events: {len(data_list)}'), html.Ul(children=[html.Li(f'Lat:{event[0]} Long:{event[1]} NP:{event[2]}') for event in data_list])]

    return no_update