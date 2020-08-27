import dash_html_components as html
import dash_core_components as dcc
import dash


def create_dashApp(name, server, charts, identifier):
    app = dash.Dash(name=name, server=server, url_base_pathname='/'+identifier+'/')
    app.layout = html.Div([
        html.Div([
            dcc.Graph(figure=charts[0])
        ]),
        html.Div([
            dcc.Graph(figure=charts[1])
        ])
    ])


