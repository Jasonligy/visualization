
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dcc



def get_data():
    '''
    Preprocess data and returns our desired dataframe
    '''
    airbnb = pd.read_csv('./preprocessed.csv',low_memory=False)
    airbnb.columns=[col.lower().replace(" ","_") for col in airbnb.columns]
    attribute = ['neighbourhood', 'neighbourhood_group','room_type','age','nei_price','service_fee','minimum_nights','availability_365']
    df = airbnb[attribute].dropna()
    df['availability_365'] < 365
    df = df[df['availability_365'] <= 365]
    df = df[df['minimum_nights'] < 2000]
    df = df[df['neighbourhood_group'] != 'brookln']
    return df

def median(x):
    '''
    median function, returns the median of the columns

    @param x: pandas dataframe
    '''
    return (x-x.min())/(x.max()-x.min)

def get_radar_score(neighbour:str, df, categories, method:str='Median'):
    '''
    from given dataframes build its radar score that can be passed to radar

    @param neighbour: list of neighbour
    @param df: dataframe
    @param categories: the category of columns
    @param method: choose between median or average method
    '''

    # drop NA
    overall_df = df[categories].dropna()
    # set minimum values less than 0 to 0
    overall_df[overall_df<0]=0

    ## Normalization using min-max
    # if neighbour=='Overall':  
    #     normalized_df=(overall_df-overall_df.min())/(overall_df.max()-overall_df.min())    
    # else:
    #     neighbour_df = df[df['neighbourhood_group']==neighbour]
    #     neighbour_df = neighbour_df[categories].dropna()
    #     normalized_df=(neighbour_df-neighbour_df.min())/(overall_df.max()-overall_df.min())

    # Normalization using standard deviation
    if neighbour=='Overall':
        normalized_df=(overall_df-overall_df.mean())/overall_df.std()  
    else:
        neighbour_df = df[df['neighbourhood_group']==neighbour]
        neighbour_df = neighbour_df[categories].dropna()
        normalized_df=(neighbour_df-overall_df.mean())/overall_df.std()
    if method=='Median':
        return normalized_df[categories].median()
    elif method=='Mean':
        return normalized_df[categories].mean()


df = get_data()
neighbours = df['neighbourhood_group'].unique()
categories = ['age','nei_price','service_fee','minimum_nights','availability_365']
categories_name = ['Overall', 'Age','Neighborhood Price','Service Fee','Minimum Nights','Availability in 365 days']
cate_dict = dict(zip(['overall']+categories, categories_name)) 


def radar_fig(neighbours: list=neighbours, method: str='Median') -> dcc.Graph:
  '''
  Returns the radar fig that can be put into our dcc graph.
  '''

  fig = go.Figure()
  neighbours = neighbours
  for neighbour in neighbours:
    fig.add_trace(go.Scatterpolar(
          r=get_radar_score(neighbour=neighbour, df=get_data(), categories=categories, method=method),
          theta=categories,
          fill='toself',
          name=neighbour,
    ))

  fig.update_layout(
    # define radar plot layout
    polar=dict(
      radialaxis=dict(
        visible=True,
        range=[-0.5, 0.5],
        tick0= '0',
        dtick= '0.2',
        tickangle = 0,
        tickfont = dict(color='#8ca4ad', size=7),
      )),
    showlegend=True,
    title={
            'text': "Attributes of Properties in New York City Boroughs",
            'xanchor': 'center',
            'x': 0.5,      
        },
  )

  return fig

