'''Dash app'''
from dash import Dash, html, dcc, Input, Output
import dash_leaflet as dl
from src.data_loader import load_data
from src.mapper import Mapper

app = Dash(__name__)

df = load_data()

app.layout = html.Div(children=[
    html.H1("Charizard", style={'textAlign': 'center', 'color': '#7FDBFF'}),
    html.Div([
        "Input: ",
        dcc.Input(id='my-input', value='JD79WMGP', type='text')
    ]),
    html.Br(),
    dl.Map([dl.TileLayer(), dl.LayerGroup(id="layer-group")], style={'width': '1000px', 'height': '500px'})
])

@app.callback(
    Output(component_id='layer-group', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    mapper = Mapper(df);
    markers = mapper.clean().filter_events_on_number_plate(input_value).generate_points().generate_color().generate_markers()
    return markers

if __name__ == '__main__':
    app.run_server(debug=True)
