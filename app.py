#https://towardsdatascience.com/beginners-guide-to-building-a-multi-page-dashboard-using-dash-5d06dbfc7599

from dash import Dash, html
import dash
import dash_bootstrap_components as dbc

dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Home", href="/"),
        dbc.DropdownMenuItem("Vehicles", href="/vehicles"),
        dbc.DropdownMenuItem("Clients", href="/clients"),
    ],
    nav = True,
    in_navbar = True,
    label = "Menu",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def create_layout(app: Dash) -> html.Div:
    return html.Div([
	html.H1('Metagrated'),
    html.Hr(),
    html.Div(
        [
            dropdown,
            html.Hr()
        ]
    ),

	dash.page_container
])

def main() -> None:
    external_stylesheets = [dbc.themes.LUX]
    app = Dash(__name__, external_stylesheets=external_stylesheets, use_pages=True)
    app.title = "metagrated"
    app.layout = create_layout(app)

    app.run_server(port=8005,debug=True)


if __name__=="__main__":
    main()
