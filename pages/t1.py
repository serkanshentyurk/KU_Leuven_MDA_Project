# Import necessary libraries 
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from app import app
from utils.descriptive.meteo import lineplot, table_head


dropdown_meteor = dcc.Dropdown(
    id='meteor_data_groups',
    options=[{"label":'All Data','value':0},
             {"label":'Grouped by Hour','value':1},
             {"label":'Grouped by Day','value':2}             ],
    value=2)

# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1('Meteorology Data')),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("Meteorology Data is recoreded every 10 minutes in 2023. It records not only temperature but other weather variables, such as:"),
            html.Ul([
                html.Li('Humidity'),
                html.Li('Dew Point'),
                html.Li('Radiation'),
                html.Li('Rain Intensity'),
                html.Li('Daily Rain Amount'),
                html.Li('Wind Speed')
            ]),
            html.P("The quality control of the data is done by the reserachers and if a datapoint passed 3 quality checks, the temperature values is listed in the column LC_TEMP_QCL3."),
            html.Br(),
            html.P("You can select All data or grouped data to see the preview of the dataframe below:"), 
            dropdown_meteor,
            html.Br(),
            html.P("The first 5 and last 5 rows are:"), 
            html.Div(id = 'meteor-output', children = []),
            html.Br(),
            html.P('Temperature, Rain Intensity, Daily Rain Amount, and Wind Speed is plotted against time.'),
            html.P('If Data - Grouped by Day is selected, you can also see the high noise events (see Export 41 Data) are also plotted. The unit of Y axis for noise events is dB (scaled).'),
            html.P('It seems to be a linear correlation between Temperature and the Noise levels. There are some peaks during March and June.'),
            dcc.Graph(id = "graph1", figure = {}),
            dcc.Graph(id = "graph2", figure = {}),
            dcc.Graph(id = "graph3", figure = {}),
            dcc.Graph(id = "graph4", figure = {}),
            dcc.Graph(id = "graph5", figure = {}),
            html.Br()
        ], width='100vw')
    ])
], style={'padding': '2rem'})

@app.callback(
    Output("meteor-output", "children"), 
    Output("graph1", "figure"), 
    Output("graph2", "figure"), 
    Output("graph3", "figure"), 
    Output("graph4", "figure"), 
    Output("graph5", "figure"), 
    Input("meteor_data_groups", "value")
)
def render_meteor_content(value):
    dashtable = table_head.create_table(value)
    fig5, fig2, fig3, fig4, fig1 = lineplot.create_line_plots(value)
    return dashtable, fig5, fig2, fig3, fig4, fig1