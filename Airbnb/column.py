import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import plotly.express as px
from dash import html,dcc
airbnb = pd.read_csv('Airbnb/preprocessed.csv')
airbnb.columns=[col.lower().replace(" ","_") for col in airbnb.columns]

def remove_dollar_sign(value):
    if pd.isna(value):
        return np.NaN
    else:
        return value
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

def preprocess(airbnb):
    airbnb["price"]=airbnb["price"].apply(lambda x: remove_dollar_sign(x))
    airbnb["service_fee"]=airbnb["service_fee"].apply(lambda x: remove_dollar_sign(x))
    airbnb.drop(columns=["id","host_id"],axis=1,inplace=True)
    airbnb.drop(columns=["country_code","country"],axis=1,inplace=True)
    airbnb.drop(columns=["house_rules","license"], axis=1, inplace=True)
    attribute = ['neighbourhood','neighbourhood_group','lat','long','room_type','construction_year','price','service_fee','minimum_nights','availability_365','number_of_reviews','instant_bookable']
    airbnb = airbnb[attribute]
    value_attribute = ['lat','long','construction_year','price','service_fee','minimum_nights','availability_365','number_of_reviews']
    for i in value_attribute:
        mean_value = airbnb[i].mean()
        airbnb[i].fillna(mean_value,inplace=True)
    airbnb = airbnb.dropna()
    options = ['Brooklyn', 'Manhattan','Queens','Staten Island','Bronx']
    
    # selecting rows based on condition
    airbnb = airbnb[airbnb['neighbourhood_group'].isin(options)]
    return airbnb
airbnb=preprocess(airbnb)
sub_1=airbnb.loc[airbnb['neighbourhood_group'] == 'Brooklyn']
price_sub1=sub_1[['price']]
#Manhattan
sub_2=airbnb.loc[airbnb['neighbourhood_group'] == 'Manhattan']
price_sub2=sub_2[['price']]
#Queens
sub_3=airbnb.loc[airbnb['neighbourhood_group'] == 'Queens']
price_sub3=sub_3[['price']]
#Staten Island
sub_4=airbnb.loc[airbnb['neighbourhood_group'] == 'Staten Island']
price_sub4=sub_4[['price']]
#Bronx
sub_5=airbnb.loc[airbnb['neighbourhood_group'] == 'Bronx']
price_sub5=sub_5[['price']]
#putting all the prices' dfs in the list
price_list_by_n=[price_sub1, price_sub2, price_sub3, price_sub4, price_sub5]

p_l_b_n_2=[]
#creating list with known values in neighbourhood_group column
nei_list=['Brooklyn', 'Manhattan', 'Queens', 'Staten Island', 'Bronx']
#creating a for loop to get statistics for price ranges and append it to our empty list
for x in price_list_by_n:
    i=x.describe(percentiles=[.25, .50, .75])
    i=i.iloc[3:]
    i.reset_index(inplace=True)
    i.rename(columns={'index':'Stats'}, inplace=True)
    p_l_b_n_2.append(i)
#changing names of the price column to the area name for easier reading of the table    
p_l_b_n_2[0].rename(columns={'price':nei_list[0]}, inplace=True)
p_l_b_n_2[1].rename(columns={'price':nei_list[1]}, inplace=True)
p_l_b_n_2[2].rename(columns={'price':nei_list[2]}, inplace=True)
p_l_b_n_2[3].rename(columns={'price':nei_list[3]}, inplace=True)
p_l_b_n_2[4].rename(columns={'price':nei_list[4]}, inplace=True)
#finilizing our dataframe for final view    
stat_df=p_l_b_n_2
stat_df=[df.set_index('Stats') for df in stat_df]
stat_df=stat_df[0].join(stat_df[1:])

sub_6=airbnb[airbnb.price < 1000]
#using violinplot to showcase density and distribtuion of prices 
viz_2=sns.violinplot(data=sub_6, x='neighbourhood_group', y='price')
viz_2.set_title('Density and distribution of prices for each neighberhood_group')

sub_7=airbnb.loc[airbnb['neighbourhood'].isin(['Williamsburg','Bedford-Stuyvesant','Harlem','Bushwick',
                 'Upper West Side','Hell\'s Kitchen','East Village','Upper East Side','Crown Heights','Midtown'])]
#using catplot to represent multiple interesting attributes together and a count
entire_room = sub_7[sub_7.room_type == 'Entire home/apt']
Private_room = sub_7[sub_7.room_type == 'Private room']
Shared_room = sub_7[sub_7.room_type == 'Shared room']
Hotel_room = sub_7[sub_7.room_type == 'Hotel room']
room_type = {'Entire home':entire_room ,'Private room':Private_room,'Shared room':Shared_room,'Hotel room':Hotel_room }
# for i in room_type:
#     viz_3=sns.catplot(x='neighbourhood', hue='neighbourhood_group', col='room_type', data=i, kind='count')
#     viz_3.set_xticklabels(rotation=90)


#used for dash
def target_graph(type):
    # viz_3=sns.catplot(x='neighbourhood', hue='neighbourhood_group', col='room_type', data=room_type[type], kind='count')
    # viz_3.set_xticklabels(rotation=90)
    fig = px.histogram(room_type[type], x="neighbourhood", color="neighbourhood_group")
    
    return fig
def data():
    return room_type
# print(Hotel_room)
# print(room_type)
target_graph('Private room')