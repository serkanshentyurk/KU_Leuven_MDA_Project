# Import necessary libraries 
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from utils.night_noise import figure_map
from utils import landing_images
import pandas as pd

data = {'Dataset': ['Meteorology Data', 'Export 40 Data', 'Export 41 Data', 'Export 42 Data', 'Facebook Data'],
        'Main Variable Interest': ['LC_TEMP_QCL3 (Quality-controlled Temperature)',
                                   'laf50_per_hour (median hourly noise values)', 
                                   'noise_event_laeq_primary_detected_class (class of noise event)',
                                   'Nan',
                                   'Events, locations, attendance']}


df = pd.DataFrame(data)

table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])


# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Br(),
        html.Center(html.H1('Noise Pollution in Leuven')),
        html.Br(),
        html.Hr(),
        html.Div([
            html.Img(src=landing_images.image1, style={'height':'80%','width':'70%'}),
        ], style={'textAlign': 'center'}),
        html.Br(),
        html.Div([
            html.Img(src=landing_images.image2, style={'height':'90%','width':'90%'}),
        ], style={'textAlign': 'center'}),
        html.Hr(),
        html.Br(),
        html.P("Noise pollution is something every big city has to deal with. Similarly for the city of Leuven, press reports regularly appear about the nighttime noise that Leuven residents complain about. Often the cause of this noise is attributed to nightlife and students who reside in the city."),
        html.Br(),
        html.P('Not surprisingly, Leuven has already set up several measures and projects to keep nighttime noise levels within certain limits, for example through nudging techniques such as dimmed lighting, signs on the road, and much more.'),
        html.Br(),
        html.P('In this project, we want to bring more insight into the noise pollution experienced by the residents in Leuven, with a particular focus on nighttime noise pollution. In doing so, we have two research objectives:'),        
        html.Div(html.Ol(
            [
            html.Li('By means of explorative visualizations, bring insight into the distribution of noise nuisance and contributing factors, such as events and weather conditions over time and location.'),
            html.Li('Building a model using machine learning techniques that can predict nighttime noise levels.'),
            ]
        ), style={'padding': '3rem'}),
        html.P('We make use of the data we obtained for different locations in the Naamsestraat. These locations are indicated in the map below.'),
        dcc.Graph(figure=figure_map.figure_map),


        html.P("We use the following data in this project:"),
        # put table here

        table,
        html.Br(),
        html.Br(),


        dbc.Col([
            html.Hr(),
            html.P("We are Team Burundi:"),
                html.Ul(
                    [
                    html.Li('Alhamd Faisal'),
                    html.Li('Mira Luna Leenders'),
                    html.Li('Robbe Ghysen'),
                    html.Li('Saar Fieuws'),
                    html.Li('Serkan Shentyurk')
                    ]
                )
        ]),
        dbc.Col([
                html.Div([html.Img(src=landing_images.image3, style={'height':'40%','width':'40%'})], style = {'padding': '1rem'})
        ])
        ])

], style={'padding': '2rem'})