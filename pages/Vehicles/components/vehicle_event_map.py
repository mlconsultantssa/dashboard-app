from dash import dcc
import dash_leaflet as dl
from . import ids

def render():
    return dcc.Loading(
        parent_className='loading_wrapper',
        children=[
            dl.Map(
                [dl.TileLayer(), dl.LayerGroup(id=ids.MAP_GROUP_LAYER)],
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
        children=[
            dl.Popup(row['size'])

        ],
        id={
            'type': 'circle-marker',
            'index': f"{row['latitude']}_{row['longitude']}"
            },
        center=[row['latitude'],
        row['longitude']],
        radius=row['size_normalised'] * 50,
        color=row['color'], fillColor=row['color'],
        fillOpacity=0.8) for i, row in data.iterrows()
    ]