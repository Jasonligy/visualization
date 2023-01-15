from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

token = 'pk.eyJ1IjoiZ29sZGVkaXRpb24yMTIiLCJhIjoiY2tld3dvMGxmMGJsbjM1bXV5cXNjam84cSJ9.32Xt4hp12-2Fa3Rk2XFLgQ'
airbnb = pd.read_csv('preprocessed.csv')
features = ["nei_price", "construction_year", "availability_365",'lat','long']
map_data = airbnb[features]


app = Dash(__name__)

app.layout = html.Div([
    html.H4('Polotical candidate voting pool analysis'),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate', 
        options=["nei_price", "construction_year", "availability_365"],
        value="nei_price",
        inline=True
    ),
    dcc.Graph(id="graph"),
])



@app.callback(
    Output("graph", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = map_data # replace with your own data source
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color=candidate,
            range_color=(400, 700),
            color_continuous_scale=px.colors.cyclical.IceFire
                            )
    # fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)














# def update_output(on):
#         return(
#             html.Div([
#                 html.Label(['Choose the range'],
#                            style={'font-weight': 'bold'}),
#                 html.P(),
#                 dcc.RangeSlider(
#                     id='select-range',
#                     marks={
#                         1: '0',
#                         2: '100',
#                         3: '200',
#                         4: '300',
#                         5: '400',
#                         6: '500',
#                         7: '600',
#                         8: '700',
#                         9: '800',
#                         10: '900',
#                         11: '1000',
#                         12: '1100',


#                     },
#                     step=1,                # number of steps between values
#                     min=1,
#                     max=12,
#                     value=[1, 12],     # default value initially chosen
#                     dots=True,             # True, False - insert dots, only when step>1
#                     allowCross=False,      # True,False - Manage handle crossover
#                     disabled=False,        # True,False - disable handle
#                     pushable=2,            # any number, or True with multiple handles
#                     updatemode='mouseup',  # 'mouseup', 'drag' - update value method
#                     included=True,         # True, False - highlight handle
#                     vertical=False,        # True, False - vertical, horizontal slider
#                     # hight of slider (pixels) when vertical=True
#                     verticalHeight=900,
#                     className='None',
#                     tooltip={'always_visible': False,  # show current slider values
#                              'placement': 'bottom'},
#                 ),
#                 html.Div(id='output_container', children=[]),
#                 dcc.Graph(id='map-graph', figure={})
#             ], id="map-slider-container"))


# @app.callback(
#     [Output(component_id='output_container', component_property='children'),
#      Output(component_id='map-graph', component_property='figure')],
# )
# def update_graph(option_slctd):
#     container = "The year chosen by user was: {}".format(option_slctd)
#     dff = df_map.copy()
#     dff = dff[(dff['Month'] >= option_slctd[0]) &
#               (dff['Month'] <= option_slctd[1])]

#     # Plotly Express
#     fig = px.choropleth_mapbox(dff, locations='Local_Authority_(Highway)', featureidkey='properties.lad19cd', geojson=uk_districts, color='size', opacity=0.8, mapbox_style="carto-positron", hover_data=['size'],
#                                color_continuous_scale=px.colors.sequential.YlOrRd, range_color=(
#         0, 300),

#         zoom=4, center={"lat": 55, "lon": 0}
#     )
#     fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

#     return container, fig

