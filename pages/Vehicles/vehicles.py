from dash import html, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
from src.common.data_loader import load_data
from .components import licence_plate_dropdown, mapper, date_picker

dash.register_page(__name__, name = "Vehicles", path='/vehicles')

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    licence_plate_dropdown.render(id='licence-plate-dropdown')
                ),
                dbc.Col(
                    date_picker.render(id='date-picker')
                )
            ]
        ),
        dbc.Row(
            [
                mapper.render(id='mapper')
            ]
        )
    ]
)

@callback(
    Output(component_id='mapper', component_property='children'),
    Input(component_id='date-picker', component_property='start_date'),
    Input(component_id='date-picker', component_property='end_date'),
    Input(component_id='licence-plate-dropdown',component_property='value')
)
def update_map(start_date, end_date, licence_plates):
    mapper_ = mapper.Mapper(load_data()).clean()
    print(start_date, end_date, licence_plates)

    if licence_plates is not None:
        mapper_.filter_events_on_number_plates(licence_plates)

    if start_date is not None:
        mapper_.filter_events_on_start_date(start_date)

    if end_date is not None:
        mapper_.filter_events_on_end_date(end_date)

    mapper_.generate_points().generate_color()

    return mapper_.get_markers()

@callback(
    Output(component_id='licence-plate-dropdown')
)
    