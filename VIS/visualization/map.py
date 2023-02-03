from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
from sklearn import preprocessing





token = 'pk.eyJ1IjoiZ29sZGVkaXRpb24yMTIiLCJhIjoiY2tld3dvMGxmMGJsbjM1bXV5cXNjam84cSJ9.32Xt4hp12-2Fa3Rk2XFLgQ'
airbnb = pd.read_csv('preprocessed.csv')

#feature selection and data normalization
features = ["nei_price", "age", "availability_365",'lat','long']
min_max_scalar = preprocessing.MinMaxScaler(feature_range=(0,1))
map_data = airbnb[features]
map_data['price_distribution'] = min_max_scalar.fit_transform(map_data['nei_price'].values.reshape(-1,1))
map_data['age_distribution'] = min_max_scalar.fit_transform(map_data['age'].values.reshape(-1,1))
map_data['availability_distribution'] = min_max_scalar.fit_transform(map_data['availability_365'].values.reshape(-1,1))


app = Dash(__name__)

# map layout
app.layout = html.Div([
    dcc.RadioItems(
        id='candidate', 
        options=["price_distribution", "age_distribution", "availability_distribution"],
        value="price_distribution",
        inline=True
    ),
    dcc.Graph(id="map"),
])

map_figure = app.layout

@app.callback(
    Output("map", "figure"), 
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = map_data 
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color=candidate,
            range_color=[0,1],
            color_continuous_scale=px.colors.sequential.amp
                            )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)






