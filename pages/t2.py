# Import necessary libraries 
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from app import app
from utils.descriptive.exp40 import plot_time_series, heatmaps, summary

dropdown_exp40 = dcc.Dropdown(
    id='exp40_data_groups',
    options=[{"label":'Naamsestraat 35  Maxim','value': 'Naamsestraat 35'},
             {"label":'Naamsestraat 57 Xior','value': 'Naamsestraat 57'},
             {"label":'Naamsestraat 62 Taste','value': 'Naamsestraat 62'},
             {"label":'Naamsestraat 76','value': 'Naamsestraat 76'},
             {"label":'Calvariekapel KU Leuven','value': 'Calvariekapel KU Leuven'},
             {"label":'Parkstraat 2 La Filosovia','value': 'Parkstraat 2'},
             {"label":'Naamsestraat 81','value': 'Naamsestraat 81'},
             {"label":'Vrijthof','value': 'Vrijthof'},
             ],
    value='Naamsestraat 35')

# Define the page layout

layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Exp 40 Data")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.Br(),
            html.P("Please select a location to see the details:"),
            dropdown_exp40,
            html.Br(),
            html.Br(),
            html.P('This graph shows us the hourly evolution of the median noise values over time, as well as the 25th and 75th percentiles for each location. We can observe the general trend over time. In addition, we see that there is some daily variation in the median noise levels. Moreover, we can identify the loudest and quietest months.'),
            dcc.Graph(id = "histogram_exp40", figure = {}),
            html.Br(),
            html.P('However, we would like more detailed information to deepen our understanding of which days and hours of the week are the loudest.'),
            dcc.Graph(id = 'heatmap-50', figure = {}),
            html.P('This heatmap shows the average median noise values for different weekdays and hours. For example, we can see that on weekends there is less noise on average in the morning and Friday nights are louder than other nights.'),
            html.Br(),
            html.P('In the summary statistics below, we get a better idea of which weekdays are the noisiest. We also make the distinction between daytime and nighttime. By night we mean the hours between 10 p.m. and 6 a.m.'),
            html.Hr(),
            html.Div(id = 'exp40-summary-output', children =[]),   
            html.Br(),         
            html.P('This table shows the average laf50_per_hour values for the whole day, the daytime, and the nighttime. Highlighted are the weekdays considered to be the loudest on average.'),
            html.P('Although the night has on average lower median noise values, they are still relatively high, especially for Thursday and Friday. WHO recommends decibels lower than 40 at night and lower than 55 at day. We see that this first target in particular is often not met. It is important to note that we are working here with average median noise values. This means that on average in an hour on a Friday night, dBs lower than or equal to 50 are observed only half of the time!'),
            html.Br(),
            html.P('In the next step, we can look at specific detected noise events associated with this problematic nighttime noise. ')
        ])
    ])
], style={'padding': '2rem'})

@app.callback(
    Output('exp40-summary-output', 'children'),
    Output('heatmap-50', 'figure'),
    Output("histogram_exp40", "figure"),
    Input("exp40_data_groups", 'value'))
def render_histogram(value):
    figure_time = plot_time_series.plot_time_series(value)
    heatmap50, heatmap01 = heatmaps.create_heatmap(value)
    summary_table = summary.create_summary_table(value)
    return summary_table, heatmap50, figure_time
