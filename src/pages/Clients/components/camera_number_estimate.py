import dash_bootstrap_components as dbc
from dash import html

def render(id):

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
                        children = "",
                        className="display-3"
                    ),

                ],
                fluid=True,
                className="py-3",
            ),
            className="p-3 bg-light rounded-3",
        )