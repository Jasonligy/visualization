from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot


from dash import html
import plotly.express as px
from dash.dependencies import Input, Output


from Airbnb.column import target_graph,data
from dash import html,dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
class Histogramplot(html.Div):
    def __init__(self, name, feature_x, feature_y, df):
        self.html_id = name.lower().replace(" ", "-")
        self.df = df
        self.feature_x = feature_x
        self.feature_y = feature_y

        # Equivalent to `html.Div([...])`
        super().__init__(
            className="graph_card",
            children=[
                dcc.Graph(figure=target_graph('Private room'))
            ],
        )

    def update(self, value):
        self.fig = go.Figure()
        self.fig.update_layout(dcc.Graph(figure=target_graph(value)),bargap=0,width=600,bargroupgap=1.0)
        return  dcc.Graph(figure=target_graph(value))


if __name__ == '__main__':



    data_his=data()
    # Instantiate custom views
    histogram=Histogramplot(" Histogram", 'petal_length', 'petal_width', data_his)

    app.layout = html.Div(
        id="app-container",
        children=[

            html.Div(id='dropdown',
                
                
                children=[dcc.Dropdown(['Entire home', 'Private room', 'Shared room','Hotel room'], 'Entire home', id='demo-dropdown'),
                html.Div(id='dd-output-container')],
            )
      ],
    )
    @app.callback(
        Output('dd-output-container', 'children'),
        Input('demo-dropdown', 'value')
    )
    def update_output(value):

        return histogram.update(value)


    app.run_server(debug=False, dev_tools_ui=False)