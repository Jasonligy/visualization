import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import dash
import plotly
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
from re import sub
from decimal import Decimal
import plotly.figure_factory as ff
from jupyter_dash import JupyterDash


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = pd.read_csv('preprocessed.csv')
df = df[df.availability_365 < 1000] # remove outlier
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
# app = JupyterDash(__name__)
construct_year_list = df[df['age'].notna()]['age'].sort_values().unique()

# 前台畫面設定
# Dash-前台：設定Dash的版面(app.layout)
app.layout = html.Div([

    # 互動式圖表放置處，此處有命名id為graph-with-slider
    # 這個id很重要，要讓後台辨識用的
    dcc.Graph(id='graph-with-slider'),
    # 設定一個slider，讓使用者能夠拖曳年份
    # 後台依據此slider目前選擇的年份繪製對應的圖表資訊
    dcc.Slider(
        # slider的id，後台辨識用的
        id='year-slider',        
        # 使用者能夠拖曳slider最小值
        min=df['age'].min(),
        # 使用者能夠拖曳slider最大值
        max=df['age'].max(),
        # slider的默認值
        value = df.age.min(),
        # value=[df['construction_year'].min(), df['construction_year'].median()],
        # slider的選項名稱
        marks = {str(year): str(year) for year in construct_year_list.astype(int)},
        step=1.0
    ),html.Br(),
    # html.Div([
    # dcc.Graph(id ='type-selection' ),
    dcc.RadioItems(
        id = 'yaxis-type',
        options=[{'label': i, 'value': i} for i in ['price', 'availability_365','service_fee']],
        value='price',
        labelStyle={'display': 'inline-block'},#,className="pretty_container four columns",
        style={"padding-left": "34%"}
    )        
    # ])

])

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
    Input('yaxis-type','value')
)
def update_figure(selected_year,yaxis_type):
    
    fig = go.Figure()
    # print(selected_year)
    # filtered_df0 = df[df.construction_year > selected_year[0]]
    # filtered_df1 = df[df.construction_year < selected_year[1]]
    # filtered_df = pd.concat([filtered_df0,filtered_df1])
    filtered_df = df[df.age == float(selected_year)]
    # filtered_df = df[df.construction_year == selected_year[1]]
    # 選取前台使用者選取的年份
    # filtered_df0 = df[df.construction_year == selected_year[0]] # defeault min
    # filtered_df1 = df[df.construction_year == selected_year[1]] # default median
    # filtered_df = df.loc[(df.construction_year > selected_year[0]) & (df.construction_year < selected_year[1])] # by year
    # filtered_df = df[df.construction_year == int(selected_year)]
    
    # 繪製圖表，此處繪製散佈圖，X軸為人均GDP，Y軸為預期壽命
    # x
    borough_all = df[df['neighbourhood_group'].notna()]['neighbourhood_group'].unique().tolist()
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
                box_visible = True,
                meanline_visible = True,
                points = 'all'
                
            ))
    # fig = go.violin(filtered_df, x="gdpPercap", y="lifeExp",box_visible = True)

    # 降低圖片動畫速度
    # fig.update_layout(transition_duration=500)
    fig.update_layout(
        title_text='Borough', # title of plot
        xaxis_title_text='Borough district', # xaxis label
        yaxis_title_text= selected_type, # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
)


    # 輸出圖表，圖表放置在callback函數指定的Output id位置
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(mode='inline', port=8051)
