# ANA 430 Final Project 

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Function to get data from CoinGecko API
def get_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': False
    }
    r = requests.get(url, params=params)
    data = r.json()
    df = pd.json_normalize(data)
    df = df[['id', 'symbol', 'name', 'market_cap', 'current_price', 'price_change_percentage_24h']]
    df.columns = ['ID', 'Symbol', 'Name', 'Market_Cap', 'Current_Price', '24h_Change']
    return df

# Load and clean data
final_df = get_crypto_data()
print(final_df.head())

# Layout for Dash app
app.layout = html.Div([
    html.H1("Top 100 Cryptocurrencies Dashboard"),

    html.H2("Choose a Metric to Display on the Bar Chart"),
    dcc.Dropdown(
        id='bar-metric',
        options=[
            {'label': 'Market Cap', 'value': 'Market_Cap'},
            {'label': 'Current Price (USD)', 'value': 'Current_Price'},
            {'label': '24h Price Change (%)', 'value': '24h_Change'}
        ],
        value='Market_Cap'
    ),

    dcc.Graph(id='bar-chart'),

    html.Hr(),

    html.H2("Compare Metrics Using a Scatter Plot"),

    html.Label("X-Axis"),
    dcc.Dropdown(
        id='xaxis',
        options=[
            {'label': 'Market Cap', 'value': 'Market_Cap'},
            {'label': 'Current Price (USD)', 'value': 'Current_Price'},
            {'label': '24h Price Change (%)', 'value': '24h_Change'}
        ],
        value='Market_Cap'
    ),

    html.Label("Y-Axis"),
    dcc.Dropdown(
        id='yaxis',
        options=[
            {'label': 'Market Cap', 'value': 'Market_Cap'},
            {'label': 'Current Price (USD)', 'value': 'Current_Price'},
            {'label': '24h Price Change (%)', 'value': '24h_Change'}
        ],
        value='Current_Price'
    ),

    dcc.Graph(id='scatter-plot'),

    html.Hr(),

    html.H2("Adjust Graph Display"),
    html.Label("Graph Height (px):"),
    dcc.Slider(
        id='graph-height',
        min=300,
        max=800,
        step=50,
        value=500,
        marks={i: f"{i}px" for i in range(300, 851, 100)}
    )
])

# Callback to update bar chart
@app.callback(
    Output('bar-chart', 'figure'),
    Input('bar-metric', 'value')
)
def update_bar(metric):
    fig = px.bar(
        final_df.head(20),
        x='Name',
        y=metric,
        title=f"Top 20 Cryptocurrencies by {metric.replace('_', ' ')}",
        labels={metric: metric.replace('_', ' ')}
    )
    return fig

# Callback to update scatter plot
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('xaxis', 'value'),
     Input('yaxis', 'value'),
     Input('graph-height', 'value')]
)
def update_scatter(x, y, height):
    fig = px.scatter(
        final_df,
        x=x,
        y=y,
        hover_name='Name',
        title=f"{x.replace('_', ' ')} vs {y.replace('_', ' ')}",
        height=height
    )
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
