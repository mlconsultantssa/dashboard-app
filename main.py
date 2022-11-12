from dash import Dash, html

from layout import create_layout

def main() -> None:
    app = Dash(__name__, use_pages=True)
    app.title = "metagrated"
    app.layout = create_layout(app)
    app.run_server(port=8050,debug=True)


if __name__=="__main__":
    main()