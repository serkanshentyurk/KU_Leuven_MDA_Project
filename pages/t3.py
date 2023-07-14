# Import necessary libraries 
from dash import html, dash_table, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
from app import app
from utils.descriptive.exp41 import stacked_bar_chart_street, pie_chart_day_night_street

dropdown_exp41 = dcc.Dropdown(
    id='exp41_data_groups',
    options=[{"label":'All Locations','value': 0},
             {"label":'Naamsestraat 35  Maxim','value': 'Naamsestraat 35'},
             {"label":'Naamsestraat 57 Xior','value': 'Naamsestraat 57'},
             {"label":'Naamsestraat 62 Taste','value': 'Naamsestraat 62'},
             {"label":'Calvariekapel KU Leuven','value': 'Calvariekapel KU Leuven'},
             {"label":'Parkstraat 2 La Filosovia','value': 'Parkstraat 2'},
             {"label":'Naamsestraat 81','value': 'Naamsestraat 81'},
             {"label":'Vrijthof','value': 'Vrijthof'},
             ],
    value = 'Naamsestraat 35')


# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Exp 41 Data")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("Please select a location to see the details:"),
            dropdown_exp41,
            html.Br(),
            dcc.Graph(id = 'exp41-stacked-bar-street', figure = {}),
            html.P('This stacked bar graph simply shows us the number of sound events detected during the day. In general, we see that the most detected sound event is the car, followed by shouting. We see that yelling occurs most often between 11:00 p.m. and 4:00 a.m., mainly around 1:00 a.m. In the pie charts, we see even more clearly that there is a difference between the types of sound events detected at night and during the day.'),
            html.Br(),
            dcc.Graph(id = 'exp41-pie-chart-street', figure = {})
        ])
    ])
], style={'padding': '2rem'})

@app.callback(
    Output('exp41-pie-chart-street', 'figure'),
    Output("exp41-stacked-bar-street", "figure"), 
    [Input("exp41_data_groups", "value")]
)
def render_bar_chart(value):
    bar_chart = stacked_bar_chart_street.create_stacked_bar_chart(value)
    pie_street = pie_chart_day_night_street.create_pie_chart_day_night(value)
    return pie_street, bar_chart
