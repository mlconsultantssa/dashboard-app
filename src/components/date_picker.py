from dash import dcc

class DatePicker:
    '''Date picker'''
    def __init__(self, id):
        self.id = id

    def get_component(self):
        '''Returns component'''
        return dcc.DatePickerRange(id=self.id, style={'padding': '20px 0px', 'zIndex': 20})
