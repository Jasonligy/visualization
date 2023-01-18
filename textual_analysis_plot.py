import pandas as pd
import numpy as np
import pandas as pd
import nltk
import re
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc

airbnb = pd.read_csv('./Airbnb/preprocessed.csv',low_memory=False)
airbnb.columns=[col.lower().replace(" ","_") for col in airbnb.columns]

def get_word_freq(top_n:int=20, style:dict=None) -> dcc.Graph:

    text = ''
    for sentence in airbnb.house_rules.values:
        text += (' ' + str(sentence))

    lower_text = text.lower()
    words = re.sub("[^A-Za-z]"," ",lower_text).split() #remove punctuation, then split by space.
    len(words)

    # nltk.download("stopwords")
    custom_sw = [
        'nan', 'keep', 
        'room', 'building', 'apartment', 'home', 'house',
        'must', 'us', 'may', 'let', 'would', 
        ]
    sw = nltk.corpus.stopwords.words('english') + custom_sw

    words_ne=[]
    for word in words:
        if word not in sw:
            words_ne.append(word)

    counts = Counter(words_ne)
    df = pd.DataFrame.from_dict(counts, orient='index').reset_index()
    df.columns = ['word', 'count']
    df = df.sort_values(by=['count'], ascending=False)

    y= list(df.iloc[:top_n,:]['word'].values)
    x= list(df.iloc[:top_n,:]['count'].values)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y= y,
        x= x,
        name='High Frequency Words',
        orientation='h',
        marker=dict(
            color='rgba(39, 159, 243, 0.8)',
            line=dict(color='rgba(37, 118, 175, 0.9)', width=2)
        )
    ))

    fig.update_layout(
        barmode='stack', yaxis={'categoryorder':'total ascending'},
        title={
            'text': "Top-"+str(top_n)+" High Frequency Words in House Rules",
            'xanchor': 'center',
            'x': 0.5
        },
        xaxis_title="Word Frequency",
        # yaxis_title="Y Axis Title",
    )

    # annotations = [].append(dict(xref='x1', yref='y1',
    #                         y=xd, x=yd + 3,
    #                         text=str(),
    #                         font=dict(family='Arial', size=12,
    #                                   color='rgb(50, 171, 96)'),
    #                         showarrow=False))

    return dcc.Graph(figure=fig, style= style)



def get_cancellation_policy(style: dict = None) -> dcc.Graph:

    cancellation_count = airbnb['cancellation_policy'].value_counts()
    colors = ['lightcyan', 'royalblue', 'darkblue']

    fig = go.Figure(
        data=[go.Pie(
            labels= cancellation_count.index, 
            values= cancellation_count.values, 
            hole=.4, pull=[0.03, 0.03, 0.03],
        ) ] 
        )
    fig.update_layout(
        title={
            'text': "The Make-up of Cancellation Policy Types",
            'xanchor': 'center',
            'x': 0.5,
            
        },
    )
    fig.update_traces(
        textfont_size=20,
        marker=dict(colors=colors, line=dict(color='#888888', width=2))
    )

    return dcc.Graph(figure=fig, style=style)
