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
df_violin = pd.read_csv('preprocessed.csv')
violin = df_violin[df_violin.availability_365 < 1000] # remove outlier
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
construct_year_list = violin[violin['age'].notna()]['age'].sort_values().unique() # Sort age and make a list, drop na

app.layout = html.Div([
    html.P("Age of propety"), # slider
    dcc.Slider(
        id='year-slider',        
        min=violin['age'].min(),
        max=violin['age'].max(),
        value = violin.age.min(),
        marks = {str(year): str(year) for year in construct_year_list.astype(int)},
        step=1.0
    ),
    dcc.Graph(id='graph-with-slider'),
    dcc.RadioItems(
        id = 'yaxis-type',
        options=[{'label': i, 'value': i} for i in ['price', 'availability_365','service_fee']],
        value='price',
        labelStyle={'display': 'inline-block'},
    )        
])



violin_figure = app.layout
@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'),
    Input('yaxis-type','value')
)
def update_figure(selected_year,yaxis_type):
    """
    # Violin plot for the chart
    # Input
    Value_YearSlider: str -> float
    Value_Yaxis: str (options)

    """
    
    fig = go.Figure()
    filtered_df = violin[violin.age == float(selected_year)]
    # x
    borough_all = violin[violin['neighbourhood_group'].notna()]['neighbourhood_group'].unique().tolist()
    # y - could be price, popularity, service fee
    selected_type = yaxis_type 
    
    
    for place in borough_all:
        # inconsistency naming
        if place == 'brookln':
            pass
        elif place == 'manhatan':
            pass
        else:
            fig.add_trace(go.Violin(
                x=filtered_df['neighbourhood_group'][filtered_df["neighbourhood_group"] == place], 
                y=filtered_df[selected_type][filtered_df["neighbourhood_group"] == place],
                name=place,
                box_visible = True,
                meanline_visible = True
                
            ))


    fig.update_layout(
        xaxis_title_text='Borough district', # xaxis label
        yaxis_title_text= selected_type, # yaxis label
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)