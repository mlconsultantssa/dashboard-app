
from dash import html, callback, Output, Input, ctx, State, MATCH, ALL, no_update, dcc, DiskcacheManager
import dash
import dash_bootstrap_components as dbc

import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

from .components import licence_plate_dropdown, date_picker, ids, event_trail_map
from src.db.queries import load_distinct_vehicles, load_event_trail_data
from src.data_processor import fix_bad_coordinates

dash.register_page(__name__, name = "EventTrail", path='/eventtrail')

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    licence_plate_dropdown.render(ids.LICENCE_PLATE_DROPDOWN)
                ),
                dbc.Col(
                    date_picker.render(ids.DATE_PICKER)
                )
            ]
        ),
        dbc.Row([
            dcc.Slider(0, 20)
        ]),
        dbc.Row(
            [
                event_trail_map.render(ids.MAP_GROUP_LAYER)
            ]
        ),
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
    Input(component_id=ids.DATE_PICKER, component_property='date'),
    Input(component_id=ids.LICENCE_PLATE_DROPDOWN, component_property='value')
    )
def update_map(date, number_plate):
    if (number_plate and date):
        data = fix_bad_coordinates(load_event_trail_data(number_plate, date))
        return event_trail_map.generate_markers(data)
