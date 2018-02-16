import dash
from dash.dependencies import Input, Output, Event
import dash_core_components as dcc
import dash_html_components as html

import plotly
import plotly.graph_objs as go

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.test_database
tests = db.tests


app = dash.Dash(__name__, static_folder='static')

# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
app.css.append_css({"external_url": "static/styles.css"})

app.layout = html.Div([
    html.H3('SUPER COOL FRAUD DETECTION DASHBOARD', style={'textAlign': 'center'}),
    html.Div([
        html.Div([
        ], className='title'),
        html.Div([
            dcc.Graph(id='fraud-graph', config={'displayModeBar': False}),
        ], className='twelve columns wind-speed'),
    ]),
    html.Div(id='fraud-table', style={'margin': '20px'}),
    dcc.Interval(id='fraud-update', interval=1000, n_intervals=0),
])

@app.callback(Output('fraud-graph', 'figure'),
              [Input('fraud-update', 'n_intervals')])
def gen_fraud(n):
    probs = []
    frauds = []
    for i, x in enumerate(tests.find().sort([('$natural', -1)]).limit(100)):
        if x['prob'] > 0.5:
            frauds.append({'prob': x['prob'], 'pos': i})
        probs.append(x['prob'])

    trace = go.Scatter(
        y=probs,
        line=go.Line(
            color='#42C4F7'
        ),
        hoverinfo='skip',
        mode='lines'
    )

    layout = go.Layout(
        height=450,
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            showline=False,
            zeroline=False,
            fixedrange=True,
            # tickvals=[0, 50, 100, 150, 200],
            # ticktext=['200', '150', '100', '50', '0'],
            # title='Time'
        ),
        yaxis=dict(
            range=[0, 1],
            showline=False,
            # fixedrange=True,
            zeroline=False,
            # nticks=max(6, round(df['Speed'].iloc[-1]/10))
        ),
        margin=go.Margin(
            t=45,
            l=50,
            r=50
        ),
        annotations=[dict(
            x=fraud['pos'],
            y=fraud['prob'],
            xref='x',
            yref='y',
            text='FRAUD DETECTED!',
            showarrow=True,
            arrowhead=5,
            # arrowcolor='red',
            font=dict(
                family='Courier New, monospace',
                size=14,
                color='red'
            ),
            ax=0,
            ay=-40) for fraud in frauds if frauds]
    )


    return go.Figure(data=[trace], layout=layout)



@app.callback(Output('fraud-table', 'children'),
              [Input('fraud-update', 'n_intervals')])
def table(n):
    # data = tests.find().sort([('$natural', -1)]).limit(100)
    # frauds = [[x['amount'], x['nameDest'], x['nameOrig'], x['oldbalanceOrg'], x['newbalanceOrig']]
    #           for x in data if x['prob'] > 0.5]
    columns = ['Amount', 'To Account ID', 'From Account ID', 'Old Balance', 'New Balance']

    data = [x for x in tests.find().sort([('$natural', -1)]).limit(100)]
    frauds = [[x['amount'], x['nameDest'], x['nameOrig'], x['oldbalanceOrg'], x['newbalanceOrig']]
              for x in data if x['prob'] > 0.5]

    print('cool!' if data[0]['prob'] > 0.5 else 'nope')

    if data[0]['prob'] > 0.5:
        background = 'red'
    else:
        background = '#42C4F7'

    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in columns], style={'background': background})] +

        [html.Tr([
            html.Td(val) for val in vals
        ]) for vals in frauds]

        , style={'width': '100%'}
    )




# {'step': '661',
#  'type': 'TRANSFER',
#  'amount': '16828.95', 
#  'nameOrig': 'C189499013',
#  'oldbalanceOrg': '20797.0',
#  'newbalanceOrig': '3968.05',
#  'nameDest': 'C1935516174', 
#  'oldbalanceDest': '59408.18',
#  'newbalanceDest': '76237.13',
#  'isFraud': '0',
#  'isFlaggedFraud': '0'}

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
