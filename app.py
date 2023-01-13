from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
<<<<<<< HEAD

from dash import html
import plotly.express as px
from dash.dependencies import Input, Output

=======
from Airbnb.test import target_graph,data
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
        self.fig.update_layout(dcc.Graph(figure=target_graph(value)))
        return  dcc.Graph(figure=target_graph(value))
>>>>>>> c098af2... 'dropdown'

if __name__ == '__main__':
    # Create data
    df = px.data.iris()
<<<<<<< HEAD

    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)

=======
    data_his=data()
    # Instantiate custom views
    scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)
    scatterplot2 = Scatterplot("Scatterplot 2", 'petal_length', 'petal_width', df)
    histogram=Histogramplot(" Histogram", 'petal_length', 'petal_width', data_his)
    # dropdown=make_dropdown_menu()
>>>>>>> c098af2... 'dropdown'
    app.layout = html.Div(
        id="app-container",
        children=[
            # Left column
            html.Div(
                id="left-column",
                className="three columns",
                children=make_menu_layout()
            ),

            # Right column
            html.Div(
                id="right-column",
                className="nine columns",
                children=[
                    scatterplot1,
                    scatterplot2
                ],
            ),
<<<<<<< HEAD
=======
            # html.Div(
            #     id='room-type',
            #     className='roomtype graph',
            #     children=make_dropdown_menu()
            # )
            html.Div(id='dropdown',
                
                
                children=[dcc.Dropdown(['Entire home', 'Private room', 'Shared room','Hotel room'], 'Entire home', id='demo-dropdown'),
                html.Div(id='dd-output-container')],
            )

>>>>>>> c098af2... 'dropdown'
        ],
    )

    # Define interactions
    @app.callback(
        Output(scatterplot1.html_id, "figure"), [
        Input("select-color-scatter-1", "value"),
        Input(scatterplot2.html_id, 'selectedData')
    ])
    def update_scatter_1(selected_color, selected_data):
        return scatterplot1.update(selected_color, selected_data)

    @app.callback(
        Output(scatterplot2.html_id, "figure"), [
        Input("select-color-scatter-2", "value"),
        Input(scatterplot1.html_id, 'selectedData')
    ])
    def update_scatter_2(selected_color, selected_data):
        return scatterplot2.update(selected_color, selected_data)
<<<<<<< HEAD

=======
    @app.callback(
        Output('dd-output-container', 'children'),
        Input('demo-dropdown', 'value')
    )
    def update_output(value):
        print('test')
        return histogram.update(value)
>>>>>>> c098af2... 'dropdown'

    app.run_server(debug=False, dev_tools_ui=False)