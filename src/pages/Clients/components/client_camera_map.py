from dash import dcc
import dash_leaflet as dl

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
    # https://www.youtube.com/watch?v=OVggxyO81CQ
    return [
        dl.CircleMarker(center=[row['latitude'],
        row['longitude']],
        radius=row['size_normalised'] * 20,
        color=row['color'], fillColor=row['color'],
        fillOpacity=0.8) for i, row in data.iterrows()
    ]
