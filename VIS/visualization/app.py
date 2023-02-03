






import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from sklearn import preprocessing
from violin import violin_figure
from map import map_figure
from matrix import matrix_figure
from textual_analysis_layout import freq_fig
from bar_chart import bar_fig,histogram
from radar_layout import radar
from radar_plot import radar_fig





app = Dash(__name__)

server = app.server
########### data of matrix####################
matrix = pd.read_csv('preprocessed.csv')
attribute = ['neighbourhood_group','room_type','age','nei_price','service_fee','minimum_nights','availability_365']
filtered_data = matrix[attribute].dropna()

##########dataframe of violin########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df_violin = pd.read_csv('./preprocessed.csv')
violin = df_violin[df_violin.availability_365 < 1000]  # remove outlier - as calcuated - out of 3rd standard deviation
construct_year_list = violin[violin['age'].notna()
                             ]['age'].sort_values().unique()


##########  dataframe of map ########

token = 'pk.eyJ1IjoiZ29sZGVkaXRpb24yMTIiLCJhIjoiY2tld3dvMGxmMGJsbjM1bXV5cXNjam84cSJ9.32Xt4hp12-2Fa3Rk2XFLgQ'
airbnb = pd.read_csv('preprocessed.csv')
#feature selection and data normalization
features = ["nei_price", "age", "availability_365",'lat','long']
min_max_scalar = preprocessing.MinMaxScaler(feature_range=(0,1))
map_data = airbnb[features]
map_data['price_distribution'] = min_max_scalar.fit_transform(map_data['nei_price'].values.reshape(-1,1))
map_data['age_distribution'] = min_max_scalar.fit_transform(map_data['age'].values.reshape(-1,1))
#compute the mean and standard variance and filter the data in terms of mean and variance
mean_ava = map_data['availability_365'].mean()
sd = map_data['availability_365'].std()
map_data = map_data[(map_data['availability_365'] <= mean_ava+(3*sd))]
map_data['availability_distribution'] = min_max_scalar.fit_transform(map_data['availability_365'].values.reshape(-1,1))

##################### data of word freq###################
word_freq = pd.read_csv('preprocessed.csv',low_memory=False)
word_freq.columns=[col.lower().replace(" ","_") for col in word_freq.columns]

#



##################layout#########################

app.layout = html.Div([
    html.Div([html.Div([html.Div([html.Img(className="logo", src="https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg"
                                           ), html.Div(["New York Airbnb Analysis"], className="navbar-title")], className="navbar-container")], className="navbar-flex")], className="navbar"),
    # map
    # first row
    html.Div([
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Geographic Analysis"),
                html.Div(className="description",
                         children="Analyze the distribution of different attributes based on geographic information in the New York area")
            ], className="title-container"),
            html.Div([map_figure], className="plot")
        ], className="child"),
    ], className="row"),

    # second row
    html.Div([
        # histogram
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Property Quantity Analysis"),
                html.Div(className="description",
                         children="Comparison of the amount of property over the different neighborhoods with respect to the different room type")
            ], className="title-container"),
            html.Div([bar_fig], className="plot"),        
        ], className="child"),

        # violin 
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Distribution Anaysis"),
                html.Div(className="description",
                         children="Analyze the distribution of various attributes with the respect to the  different neighbourhoods in New York")
            ], className="title-container"),
            html.Div([violin_figure], className="plot"),   
        ], className="child"),

        # radar
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Region Analysis"),
                html.Div(className="description",
                         children="Attributes of Properties with the respect to the New York City Boroughs")
            ], className="title-container"),
            html.Div([radar], className="plot"),   
        ], className="child"),
        
        

    ], className="row"),

    # third row
    html.Div([
        # histogram
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Findings on Textual Data"),
                html.Div(className="description",
                         children="The words frequency counting in houseing rule and cancellation policy")
            ], className="title-container"),
            html.Div([freq_fig], className="plot")       
        ], className="child"),

        # matrix
        html.Div([

            html.Div([
                html.Div(className="title",
                         children="Correlation among the features"),
                html.Div(className="description",
                         children=" Analysis the correlation among part of important features ")
            ], className="title-container"),
            html.Div([matrix_figure], className="plot")
        ], className="child"),     

    ], className="row"),
],
    className="parent"
)

# ---------------------------------------------------------------


############### figure of map###########################
@app.callback(
    Output("map", "figure"),
    Input("candidate", "value"))
def display_choropleth(candidate):
    df = map_data  
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color=candidate,
                            range_color=[0, 1],
                            color_continuous_scale=px.colors.cyclical.IceFire
                            )
    fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(margin=dict(b=0, t=0, l=0, r=0))

    return fig


##################figure of histogram#############################
@app.callback(
    Output('dd-output-container', 'children'),
    Input('demo-dropdown', 'value')
)
def update_output(value):
    return histogram.update(value)




#####################violin######################


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('yaxis-type', 'value')
)
def update_figure(selected_year, yaxis_type):
    """
    # use the go.Violin()
    - Input: selected_uear : float
    - Input: yaxis_type: str
    ## Output: fig
    """

    fig = go.Figure()
    filtered_df = violin[violin.age == float(selected_year)]

    # x - make boroughs into list
    borough_all = violin[violin['neighbourhood_group'].notna(
    )]['neighbourhood_group'].unique().tolist()
    # y
    selected_type = yaxis_type

    for place in borough_all:
        # filter incosistency naming
        if place == 'brookln':
            pass
        elif place == 'manhatan':
            pass
        else:
            # plotting
            fig.add_trace(go.Violin(
                x=filtered_df['neighbourhood_group'][filtered_df["neighbourhood_group"] == place],
                y=filtered_df[selected_type][filtered_df["neighbourhood_group"] == place],
                name=place,
                box_visible=True,
                meanline_visible=True

            ))
    fig.update_layout(
        title_text='Borough',  # title of plot
        xaxis_title_text='Borough district',  # xaxis label
        yaxis_title_text=selected_type,  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )

    return fig

#################### radar######################
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


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
