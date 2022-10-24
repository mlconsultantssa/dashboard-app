from dash import html

class ColumnLayout:
    '''Column container'''
    def __init__(self, id):
        self.id = id

    def get_component(self, columns):
        '''Returns component'''
        total_column_divisions= sum(column.width for column in columns)

        return html.Div(
            style={'display': 'flex'},
            children=[html.Div(
                style={'width': f'{(100/total_column_divisions) * column.width}%', 'padding': '20px'},
                children=column.components
            ) for column in columns]
        )
