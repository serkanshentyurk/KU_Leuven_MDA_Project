# Import necessary libraries 
from dash import html, dcc
import dash_bootstrap_components as dbc
from app import app
from utils.descriptive.fb import scatter, heatmap
from utils.descriptive.map_mira import create_map


fig_heatmap = heatmap.fig
fig_scatter = scatter.fig
fig_map = create_map.map_figure


# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Facebook Data")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("We believe that the events hosted in Leuven might lead to high Noise Levels. Thus, we scraped Events from Facebook that happened in 2022."), 
            html.Br(),
            dcc.Graph(id = 'graph1', figure = fig_map),
            html.P("We suspected whether the day of the week affect the noise levels. The heatmap shows the number of events per weekdays for all year. As it is seen, the number of events in Thursday and Friday is higher than other days, especailly Friday, Saturday, and Sunday."),
            html.Br(),
            html.P('We - the international ones - explain the lack of events in Friday by the phenomenon called BESGOH, a.k.a. Belgian Students Going Back to Their Homes :)'), 
            dcc.Graph(id = "graph2", figure = fig_heatmap),
            html.Br(),
            html.P('You can see the number of people attended to the events throughout the year. The colours represent the weekdays.'),
            dcc.Graph(id = "graph3", figure = fig_scatter),
            html.Br()
        ], width='100vw')
    ])
], style={'padding': '2rem'})