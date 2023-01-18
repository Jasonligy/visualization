import pandas as pd
import numpy as np
import pandas as pd
import nltk
import re
from collections import Counter
import plotly.express as px
import plotly.graph_objects as go

def get_word_freq():

    airbnb = pd.read_csv('./Airbnb/preprocessed.csv',low_memory=False)
    airbnb.columns=[col.lower().replace(" ","_") for col in airbnb.columns]

    text = ''
    for sentence in airbnb.house_rules.values:
        text += (' ' + str(sentence))

    lower_text = text.lower()
    words = re.sub("[^A-Za-z]"," ",lower_text).split() #remove punctuation, then split by space.
    len(words)

    nltk.download("stopwords")
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

    # basic bar
    # fig = px.bar(
    #     df.iloc[:20,:], 
    #     x='word', y='count',
    #     text_auto='.2s', hover_data=['word'], orientation='h'
    #     )

    # fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

    y= list(df.iloc[:20,:]['word'].values)
    x= list(df.iloc[:20,:]['count'].values)

    # 
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
            'text': "High Frequency Words",
            'xanchor': 'center',
            'x': 0.5
        },
        xaxis_title="Word Count",
        # yaxis_title="Y Axis Title",
    )

    # annotations = [].append(dict(xref='x1', yref='y1',
    #                         y=xd, x=yd + 3,
    #                         text=str(),
    #                         font=dict(family='Arial', size=12,
    #                                   color='rgb(50, 171, 96)'),
    #                         showarrow=False))


    return fig

# fig = get_word_freq()
# fig.show()