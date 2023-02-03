from dash import Dash, dcc, html
from textual_analysis_plot import get_word_freq, get_cancellation_policy


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

'''
LAYOUT for the word frequency component
'''

app.layout = html.Div([
    # Tab view
    dcc.Tabs([
        dcc.Tab(label='House Rules', children=[get_word_freq(top_n=15)]),
        dcc.Tab(label='Cancellation Policy', children=[get_cancellation_policy()]),
    ], style={'font-family': 'Avenir'})
])

freq_fig =  app.layout

if __name__ == '__main__':
    app.run_server(debug=True)


