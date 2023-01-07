import dash_bootstrap_components as dbc
from dash import html

def render(id):
    #clients = list(load_data()['camera_id'].unique())
    clients = ['one-space-11', 'vumacam-14', 'itrack-21', 'navic-5', '-20', '-9', 'alpha-security-group-12', '-7', '-10', 'watcher-22', '-17', 'nimbus-24', 'cloudsell-25', '-8', 'maxi-security-18' ]

    return html.Div(
            dbc.Container(
                [
                    html.Div(
                        [
                    html.Div(html.P("Estimated number of cameras", className="lead")),
                    html.Div(html.P(dbc.Button("Learn more", color="primary"), className="lead"))
                        ],
                    className="hstack gap-3"),

                    html.Hr(className="my-2"),
                    html.P(
                        id=id,
                        children = "100",
                        className="display-3"
                    ),

                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )