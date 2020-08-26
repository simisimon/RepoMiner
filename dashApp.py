import dash_html_components as html
import dash_core_components as dcc
import dash


def create_dashApp(name, server, fig, identifier):
    app = dash.Dash(name=name, server=server, url_base_pathname='/'+identifier+'/')
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])


