from dash import html, dcc 

def render(id):
    licence_plates = []

    return html.Div(
        children = [
            html.H6('Choose licence plate'),
            dcc.Dropdown(
                id = id,
                options=[{'label': licence_plate, 'value': licence_plate} 
                    for licence_plate in licence_plates],
                value = None,
                multi=True
            ),
            html.Div(id = '{id}-initial-loader')
        ]
    )
