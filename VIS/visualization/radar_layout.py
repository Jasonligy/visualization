from dash import Dash, dcc, html, Input, Output
import pandas as pd
from radar_plot import radar_fig

''' Map
airbnb = get_data()
token = 'pk.eyJ1IjoieHdhbmc3IiwiYSI6ImNsY3VsenV3ZzB2eXEzcHMxaTB0c3I5dzgifQ.B3HVHAdHrqlClPA2O9XVUg'
us_cities = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/us-cities-top-1k.csv")'''


app = Dash(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


'''
LAYOUT for radar map
'''

app.layout = html.Div([
    html.Div([
        # multiselect dropdown 
        dcc.Dropdown(
        ['Overall', 'Manhattan', 'Brooklyn', 'Queens', 'Staten Island', 'Bronx'],
        multi=True,
        id='radar-neighborhood-select',
        value = ['Overall']
        ),
        # radiobutton
        dcc.RadioItems(
            ['Mean', 'Median'],
            'Median',
            id='radar-method',
            inline=True
        ),
    ]),
    # radar graph
    dcc.Graph(id='radar-plot', figure=radar_fig(neighbours=['Manhattan'])),
])
radar = app.layout

# callback that updates the radar plot
@app.callback(
    Output(component_id='radar-plot', component_property='figure'),
    Input(component_id='radar-neighborhood-select', component_property='value'),
    Input(component_id='radar-method', component_property='value')
)
def update_radar(neighborhood_select, method):
    if neighborhood_select:
        return radar_fig(neighbours=neighborhood_select, method=method)
    else:
        return radar_fig(neighbours=["Overall"], method=method)
    
if __name__ == '__main__':
    app.run_server(debug=True)


