'''Dash app'''

from dash import Dash, html
from src import components, layouts
from src.common import FilterInput

# Create dash app
app = Dash(__name__, use_pages=True)
application = app.server

# Initialise custom components
vehicle_dropdown = components.VehicleDropdown('my-input')
date_picker = components.DatePicker('date-picker')
filter_store = components.FilterStore('filter-store')
map_component = components.Map('map')
column_layout = layouts.ColumnLayout('column-layout')

# Set app layout
app.layout = html.Div(children=[
    filter_store.get_component(),
    html.H1("Charizard", style={'textAlign': 'center', 'color': '#7FDBFF'}),
    column_layout.get_component([
        layouts.Column(1, [
            vehicle_dropdown.get_component(),
            date_picker.get_component()
        ]),
        layouts.Column(2, [
            map_component.get_component()
        ])
    ])
])

# Set custom callbacks
vehicle_dropdown.set_callback(app)
input_tuples = [
    FilterInput('number_plate', vehicle_dropdown.id),
    FilterInput('start_date', date_picker.id, 'start_date'),
    FilterInput('end_date', date_picker.id, 'end_date')
]
filter_store.set_callback(app, input_tuples, map_component.id)

if __name__ == '__main__':
    app.run_server(port=8050,debug=True)
