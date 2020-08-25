import dash_html_components as html
import dash_core_components as dcc
import dash


def create_dashApp(name, server, fig, id):
    app = dash.Dash(name=name, server=server, url_base_pathname='/'+id+'/')
    app.layout = html.Div([
        dcc.Graph(figure=fig)
    ])

