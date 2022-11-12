'''Store for filters'''

from dash import dcc, Input, Output, State

from src.data_loader import load_data
from src.mapper import Mapper

initial_data = {
    'number_plate': '',
    'start_data': '',
    'end_date': ''
}

class FilterStore:
    '''Filter store'''
    def __init__(self, id):
        self.id = id

    def get_component(self):
        '''Returns component'''
        return dcc.Store(id=self.id, data=initial_data)

    def set_callback(self, app, input_tuples, output_id):
        '''Sets callback'''
        @app.callback(
        Output(self.id, 'data'),
        State(self.id, 'data'),
        [Input(input_tuple.component_id, input_tuple.component_property) for input_tuple in input_tuples],
        )
        def update_store(data, *inputs):
            data = data or initial_data

            for i, value in enumerate(input_tuples):
                data[value.name] = inputs[i] or ''

            return data


        @app.callback(
        Output(output_id, 'children'),
        Input(self.id, 'data')
        )
        def update_map(input_value):
            mapper = Mapper(load_data()).clean()

            if input_value['number_plate'] != '':
                mapper.filter_events_on_number_plate(input_value['number_plate'])

            if input_value['start_date'] != '':
                mapper.filter_events_on_start_date(input_value['start_date'])

            if input_value['end_date'] != '':
                mapper.filter_events_on_end_date(input_value['end_date'])

            mapper.generate_points().generate_color()

            return mapper.get_markers()
