from dash import dcc
import dash_leaflet as dl

class Map:
    '''Map'''
    def __init__(self, id):
        self.id = id

    def get_component(self):
        '''Returns component'''
        return dcc.Loading(
        parent_className='loading_wrapper',
        children=[
            dl.Map(
                [dl.TileLayer(), dl.LayerGroup(id=self.id)],
                center=[-30, 25], zoom=5,
                style={'width': '100%', 'height': '500px'}
            )
        ],
        style={'zIndex': 10}
    )
