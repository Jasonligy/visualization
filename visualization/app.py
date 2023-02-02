






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




app = Dash(__name__)

server = app.server
########### data of matrix####################
matrix = pd.read_csv('preprocessed.csv')
attribute = ['neighbourhood_group', 'room_type', 'age',
             'nei_price', 'service_fee', 'minimum_nights', 'availability_365']
filtered_data = matrix[attribute].dropna()

##########dataframe of violin########
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df_violin = pd.read_csv('preprocessed.csv')
violin = df_violin[df_violin.availability_365 < 1000]  # remove outlier
construct_year_list = violin[violin['age'].notna()
                             ]['age'].sort_values().unique()


##########  dataframe of map ########

token = 'pk.eyJ1IjoiZ29sZGVkaXRpb24yMTIiLCJhIjoiY2tld3dvMGxmMGJsbjM1bXV5cXNjam84cSJ9.32Xt4hp12-2Fa3Rk2XFLgQ'
airbnb = pd.read_csv('preprocessed.csv')
features = ["nei_price", "age", "availability_365", 'lat', 'long']
min_max_scalar = preprocessing.MinMaxScaler(feature_range=(0, 1))
map_data = airbnb[features]
# for avaiablity
mean_ava = map_data['availability_365'].mean()
sd = map_data['availability_365'].std()
map_data = map_data[(map_data['availability_365'] <= mean_ava+(3*sd))] # fitler outlier row

map_data['availability_distribution'] = min_max_scalar.fit_transform(
    map_data['availability_365'].values.reshape(-1, 1))
map_data['price_distribution'] = min_max_scalar.fit_transform(
    map_data['nei_price'].values.reshape(-1, 1))
map_data['age_distribution'] = min_max_scalar.fit_transform(
    map_data['age'].values.reshape(-1, 1))


##################### data of word freq###################
word_freq = pd.read_csv('preprocessed.csv',low_memory=False)
word_freq.columns=[col.lower().replace(" ","_") for col in word_freq.columns]



##################layout#########################

app.layout = html.Div([
    html.Div([html.Div([html.Div([html.Img(className="logo", src="https://tailwindui.com/img/logos/workflow-mark-indigo-500.svg"
                                           ), html.Div(["New York Airbnb Analysis"], className="navbar-title")], className="navbar-container")], className="navbar-flex")], className="navbar"),
    # map
    html.Div([
        html.Div([
            html.Div([
                html.Div(className="title",
                         children="Location Analysis"),
                html.Div(className="description",
                         children="Analyze the distribution of various attributes in different locations in New York")
            ], className="title-container"),
            html.Div([map_figure], className="plot")
        ], className="child"),
    ], className="row"),

    html.Div([
        html.Div([
            # barchart
            html.Div([
                html.Div(className="title",
                         children="Comparsion of the number of the property"),
                html.Div(className="description",
                         children="Statistics on the number of different housing types under different regions")
            ], className="title-container"),
            html.Div([bar_fig], className="plot"),
            html.Br(),
            # freq_fig
            html.Div([
                html.Div(className="title",
                         children="Findings on Textual Data"),
                html.Div(className="description",
                         children="The words frequency counting in houseing rule and cancellation policy")
            ], className="title-container"),
            html.Div([freq_fig], className="plot")
        ], className="child"),

        # down right part
        html.Div([
            # vilion
            html.Div([
                html.Div(className="title",
                         children="Distribution of the attributes in NYC boroughs"),
                html.Div(className="description",
                         children="Density and distribution of differnt attributes for each neighberhood_group")
            ], className="title-container"),
            html.Div([violin_figure], className="plot"),

            html.Br(),
            # matrix
            html.Div([
                html.Div(className="title",
                         children="Objects distribution"),
                html.Div(className="description",
                         children=" Count all the items and display them in a histogram and pie chart. ")
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
    df = map_data  # replace with your own data source
    fig = px.scatter_mapbox(df, lat='lat', lon='long', color=candidate,
                            range_color=[0, 1],
                            color_continuous_scale=px.colors.cyclical.IceFire
                            )
    # fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
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


# Dash-後台
# callback函數：
# 輸入(Input)為前台畫面id='year-slider'的值，即使用者現在選取Slider的年份
# 輸出(Output)為圖表放置到前台畫面id='graph-with-slider'的位置
# 當Input有更動時，此函數即會執行，並將運作完的結果返回到Output
# 在這個範例中，當使用者調整Slider的年份，後台察覺前台有變化，
# 即會執行update_figure函數，依選取年份繪製出的圖形後，
# 輸出到前台畫面的圖片放置處


@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('yaxis-type', 'value')
)
def update_figure(selected_year, yaxis_type):

    fig = go.Figure()
    # print(selected_year)
    # filtered_df0 = df[df.construction_year > selected_year[0]]
    # filtered_df1 = df[df.construction_year < selected_year[1]]
    # filtered_df = pd.concat([filtered_df0,filtered_df1])
    filtered_df = violin[violin.age == float(selected_year)]
    # filtered_df = df[df.construction_year == selected_year[1]]
    # 選取前台使用者選取的年份
    # filtered_df0 = df[df.construction_year == selected_year[0]] # defeault min
    # filtered_df1 = df[df.construction_year == selected_year[1]] # default median
    # filtered_df = df.loc[(df.construction_year > selected_year[0]) & (df.construction_year < selected_year[1])] # by year
    # filtered_df = df[df.construction_year == int(selected_year)]

    # 繪製圖表，此處繪製散佈圖，X軸為人均GDP，Y軸為預期壽命
    # x
    borough_all = violin[violin['neighbourhood_group'].notna(
    )]['neighbourhood_group'].unique().tolist()
    # y
    selected_type = yaxis_type

    for place in borough_all:
        if place == 'brookln':
            pass
        elif place == 'manhatan':
            pass
        else:
            fig.add_trace(go.Violin(
                # filtered_df,
                x=filtered_df['neighbourhood_group'][filtered_df["neighbourhood_group"] == place],
                y=filtered_df[selected_type][filtered_df["neighbourhood_group"] == place],
                name=place,
                box_visible=True,
                meanline_visible=True,
                points='all'

            ))
    # fig = go.violin(filtered_df, x="gdpPercap", y="lifeExp",box_visible = True)

    # 降低圖片動畫速度
    # fig.update_layout(transition_duration=500)
    fig.update_layout(
        title_text='Borough',  # title of plot
        xaxis_title_text='Borough district',  # xaxis label
        yaxis_title_text=selected_type,  # yaxis label
        bargap=0.2,  # gap between bars of adjacent location coordinates
        bargroupgap=0.1  # gap between bars of the same location coordinates
    )

    # 輸出圖表，圖表放置在callback函數指定的Output id位置
    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
