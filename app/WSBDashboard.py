import dash
import app.WSBPrimary as WSB
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.express as px
import plotly.graph_objects as go

"""
def get_returns(df):
    #get list of daily returns from ticker dataframe
    returns = []
    for i in range(len(df.Close)-1):
        dailyreturn = ((df.Close[i+1] - df.Close[i])/df.Close[i])*100
        returns.append(dailyreturn)
    return returns
"""
# above function can be used to make a histogram

app = dash.Dash("r/WallStreetBets Frequently Mentioned Tickers")

df = pd.read_excel('C:/Users/John/Test Workbooks/Reddit Bot Data/WSB Ticker Count.xlsx')

tickerlist = list(df['Ticker'].unique())

count = list(df.Count)
ticker = list(df.Ticker)

fig = px.bar(df, x=df.Ticker, y=df.Count, color=df.Sentiment)

app.layout = html.Div([
    html.Div([
        html.H1('Top 20 most frequently mentioned stocks on WSB'),
        dcc.Graph(figure=fig),

        html.Div([
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in tickerlist],
                value=ticker[0]
            ),
            dcc.DatePickerRange(
                id='daterange',  # id to be used for callback
                start_date=dt(2020, 1, 1),  # default start date
                min_date_allowed=dt(2010, 1, 1),  # default minimum date
                end_date=dt.now()  # default ending date
            ),

            dcc.Graph(id='performance')
        ])
    ])
])


@app.callback(Output('performance', 'figure'),
              [Input('dropdown', 'value'),
               Input('daterange', 'start_date'),
               Input('daterange', 'end_date')])
def update_graph(selected_dropdown_value, start_date, end_date):
    df = web.DataReader(
        selected_dropdown_value,
        'yahoo',
        start_date,
        end_date
    )
    # above code uses pandas_datareader to get stock information from yahoo finance
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }],
        'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
    }


app.run_server()

