from jbi100_app.main import app
from jbi100_app.views.menu import make_menu_layout
from jbi100_app.views.scatterplot import Scatterplot
import pandas as pd
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
from jbi100_app.views.viob import vioB
import dash_core_components as dcc
import plotly.graph_objects as go

# Create data
df = pd.read('Airbnb_2')
# borough_all list
borough_all = df[df['neighbourhood_group'].notna(
)]['neighbourhood_group'].unique().tolist()
y_features = ['price', 'construction_year', 'availability_365']
# Instantiate custom views
# scatterplot1 = Scatterplot("Scatterplot 1", 'sepal_length', 'sepal_width', df)

app.layout = html.Div(
    [
        html.Div(id="output-clientside"),
        html.Div(
        [
            html.H1("Select Data with RangeSlider", style={
                    "text-align": "center", "color": "blue"}),
            html.P("Select borough districts for comparison", className="control_label", style={"font-weight": "bold", "text-align": "center"}),
        ]),
        html.Div(
        [
            html.H1("Select Data with RangeSlider", style={
                    "text-align": "center", "color": "blue"}),
            html.P("Select borough districts for comparison", className="control_label", style={"font-weight": "bold", "text-align": "center"}),
        ],
        )
        html.Div(
        [
            dcc.RadioItems(
                id='xaxis-column',  # input id
                options=[{'label': i, 'value': i} for i in borough_all],
                value='Box',
                # ,className="pretty_container four columns",
                labelStyle={'display': 'inline-block'},
                style={"padding-left": "34%"}
            ),
        ],)
        html.Div(
        [
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in y_features],
                value=y_features[0]
            ),
        ],)
            dcc.Graph(id="graph-with-rangeslider"),
            dcc.RangeSlider(
                id='my-range-slider',
                min=df.construction_year.min(),
                max=df.construction_year.max(),
                step=1.0,
                # 滑动条下每个年份数字，改成字符型数据
                marks={str(year): str(year)
                        for year in df["construction_year"].unique()},
                value=[2015, 2022]  # 范围和初始值
                ),
        # html.Div(id='output-container-range-slider')
    ],)

    # Define interactions
@ app.callback(
    Output("graph-with-rangeslider", "figure"),  # 输出与输入，和上面的名称一一对应
#     Output('output-container-range-slider', 'children'),
    [Input("year-rangeslider", "value")]  # input yea
    [Input("xaxis-column","value")]
    [Input("yaxis-column","value")]
)
def update_figure(selected_year, borough_list, y_feat):
    # fill in the indicate year
    year_start = df[df.year == selected_year[0]]
    year_end = df[df.year == selected_year[1]]
    point_style = 'all'
    # if y feature is construction year, then need to update year range
    if y_feat == 'construction_year':
        year_ = year_start
        _year = year_end
        df_plot = df.loc[(df.construction_year > year_) & (
            df.construction_year < _year)]
    else:
        df_plot = df
    
    for place in borough_list:
        if place == 'brookln':
            pass
        elif place == 'manhatan':
            pass
        else:
            fig = go.Figure()
            fig.add_trace(go.Violin(
                x = df_plot['neighbourhood_group'][df_plot['neighbourhood_group'] == place],
                y = df_plot[y_feat][df_plot['neighbourhood_group']==place],
                name = place,
                box_vivsible = True,
                meanline_visible = True,
                points = point_style
            ))
    fig.update_layout(
        title_text='Borough', # title of plot
        xaxis_title_text='Borough district', # xaxis label
        yaxis_title_text=y_feat, # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=False, dev_tools_ui=False)
