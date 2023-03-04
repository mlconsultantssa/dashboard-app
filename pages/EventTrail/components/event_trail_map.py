from dash import dcc
import dash_leaflet as dl
from . import ids

def render(id):
    return dcc.Loading(
        parent_className='loading_wrapper',
        children=[
            dl.Map(
                [dl.TileLayer(), dl.LayerGroup(id=id)],
                center=[-30, 25], zoom=5,
                style={'width': '100%', 'height': '500px'}
            )
        ],
        style={'zIndex': 10}
    )

def generate_markers(data):
    # Create markers from data frame.
    return [
        dl.CircleMarker(
        id={
            'type': ids.CIRCLE_MARKER,
            'index': row['created_at']
            },
        center=[row['latitude'],
            row['longitude']],
        fillColor="blue",
        fillOpacity=0.8) for i, row in data.iterrows()
    ]