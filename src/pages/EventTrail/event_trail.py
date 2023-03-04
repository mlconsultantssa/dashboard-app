
from dash import html, callback, Output, Input, ctx, State, MATCH, ALL, no_update, dcc, DiskcacheManager, callback_context
import dash
import dash_bootstrap_components as dbc
import datetime

import diskcache
cache = diskcache.Cache("./cache")
background_callback_manager = DiskcacheManager(cache)

from .components import licence_plate_dropdown, date_picker, ids, event_trail_map
from package.db.queries import load_distinct_vehicles, load_event_trail_data
from package.data_processor import fix_bad_coordinates
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

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
        dbc.Row(
            [
                dbc.Col(
                    event_trail_map.render(ids.MAP_GROUP_LAYER),
                    width=8
                ), 
                dbc.Col(
                    dcc.Slider(0, 10, step=1, id=ids.SLIDER, vertical=True, tooltip={"always_visible": True}),
                    width=4
                )
                
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

@callback(
    [Output(ids.SLIDER, 'max'),
    Output(ids.SLIDER, 'marks'),],
    [Input(component_id=ids.DATE_PICKER, component_property='date'),
    Input(component_id=ids.LICENCE_PLATE_DROPDOWN, component_property='value')]
)
def update_slider(date, number_plate):
    if (number_plate and date):

        data = fix_bad_coordinates(load_event_trail_data(number_plate, date))
        #dates = data.index()
        logger.debug(f'event trail data {data}')
        dates = list(data["created_at"])
        markers = {}
        for i in range(len(data)):
            markers[i] = {'label': dates[i][:], 'style': {'writing-mode': 'horizontal-rl', 'text-orientation': 'upright', 'margin-top': '1000px', "white-space":"nowrap"}}
        
        #print(f'event trail data {list(data["created_at"])}')
        return len(data) - 1, markers
    
# @callback(
#     Input(ids.SLIDER, 'value'),
#     output=dict(
#             radius=Output({'type': ids.CIRCLE_MARKER, 'index': ALL}, 'radius')
#         )
#     )
# def update_circle_marker_radius(value):
#     outputs = len(callback_context.outputs_grouping['radius'])
#     result_radius = [10 for _ in range(outputs)]
#     if(value):
#         result_radius[value] = 20
#     print(result_radius)
#     return {'radius': result_radius}

# @callback(
#     Input(ids.SLIDER, 'value'),
#     output=dict(
#             color=Output({'type': ids.CIRCLE_MARKER, 'index': ALL}, 'color')
#         )
#     )
# def update_circle_marker(value):
#     outputs = len(callback_context.outputs_grouping['color'])
#     result_color = ["blue" for _ in range(outputs)]
#     print(result_color)
#     print(value)
#     if(value):
#         result_color[value] = "red"
#     print(result_color)
#     return {'color': result_color}

    
@callback(
    [Output({'type': ids.CIRCLE_MARKER, 'index': ALL}, 'radius'),
    Output({'type': ids.CIRCLE_MARKER, 'index': ALL}, 'color')],
    [Input(ids.SLIDER, 'value')])
def update_circle_marker_radius(value):
    outputs = len(callback_context.outputs_grouping[0])
    result_radius = [10 for _ in range(outputs)]
    if(value):
        result_radius[value] = 20

    result_color = ["blue" for _ in range(outputs)]
    if(value):
        result_color[value] = "red"
    return result_radius, result_color



