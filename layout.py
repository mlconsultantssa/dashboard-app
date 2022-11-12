from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import dash


def create_layout(app: Dash) -> html.Div:
    print(dash.page_registry.values())
    return html.Div([
	html.H1('Multi-page app with Dash Pages'),

    html.Div(
        [
            html.Div(
                dcc.Link(
                    f"{page['name']} - {page['path']}", href=page["relative_path"]
                )
            )
            for page in dash.page_registry.values()
        ]
    ),

	dash.page_container
])
