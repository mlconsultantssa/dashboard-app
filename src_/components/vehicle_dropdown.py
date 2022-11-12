'''Vehicle dropdown component'''

from dash import dcc, Input, Output, html

from src.data_loader import load_distinct_vehicles

class VehicleDropdown:
    '''Vehicle dropdown'''
    def __init__(self, id):
        self.id = id

    def get_component(self):
        '''Returns component'''
        return html.Div([
            dcc.Loading(
                parent_className='loading_wrapper',
                children=(dcc.Dropdown([], '', id=self.id)),
                style={'zIndex': 10}
            ),
            html.Div(id=self.id + '-initial-loader')
        ], style={'max-width': '288px'})

    def set_callback(self, app):
        '''Sets callback'''

        @app.callback(
            Output(self.id, 'options'),
            Input(self.id + '-initial-loader', 'children')
        )
        def initial_load(_):
            vehicles = load_distinct_vehicles()
            return vehicles
