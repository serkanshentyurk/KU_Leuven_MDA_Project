# Import necessary libraries 
from dash import html, dcc, Output, State, Input
import dash_bootstrap_components as dbc
from utils.fb_events import fb_events_table, fb_events_images, fb_events_model, plot_prediction
from datetime import date
from app import app
import plotly.graph_objects as go

# Parameters for predictions

# month-day selection
datepicker1 = dcc.DatePickerSingle(
    id='parameter_date',
    min_date_allowed=date(2023, 1, 1),
    max_date_allowed=date(2023, 12, 31),
    initial_visible_month=date(2023, 1, 1),
    date=date(2023, 10, 1),
    show_outside_days=True,
    day_size=32,
    display_format='DD/MM/YYYY',
    clearable=True,
    style={'zIndex': 10},
    )

# dropdown for hour selection

dropdown_hour = dcc.Dropdown(
    id='parameter_time',
    options=[{"label": '22:00','value':22},
             {"label": '23:00','value':23},
             {"label": '00:00','value':0},
             {"label": '01:00','value':1},
             {"label": '02:00','value':2},
             {"label": '03:00','value':3},
             {"label": '04:00','value':4},
             {"label": '05:00','value':5},
             ],
    value=22)

# input for temperature

temperature = dcc.Input(id='parameter_temperature', type='number', min=-20, max=40, step=1, value = 10)

# input for attendance

attendance = dcc.Input(id='parameter_attendance', type='number', min=0, max=2000, step=1, value = 10)

# slider for distance 

distance = dcc.Slider(id='parameter_distance', value=500, min=0, max=1000, step=1,
                    marks={
                        0: '0 m',
                        250: '250 m',
                        500: '500 m',
                        750: '750 m',
                        1000: '1000 m'}
                        ) # meters

# dropdown for rain_density
dropdown_rain_density = dcc.Dropdown(
    id='parameter_rain_density',
    options=[{"label": 'No Rain','value':0},
             {"label": 'Light ','value':0.02},
             {"label": 'Moderate','value':0.05},
             {"label": 'Heavy','value':0.2},
             {"label": 'Violant','value':1}
             ],
    value=0)
# dropdown for rain_amount

dropdown_rain_amount = dcc.Dropdown(
    id='parameter_rain_amount',
    options=[{"label": 'No Rain','value':0},
             {"label": 'Light ','value':0.00001},
             {"label": 'Moderate','value':0.0003},
             {"label": 'Heavy','value':0.001},
             ],
    value=0)

# Prediction button 

predict_button = dbc.Button("Predict", id = "predict_button", color="primary")

parameters = dbc.Row([dbc.Col(
    html.Div([
        html.P('Select Date:'),
        datepicker1,
        html.Br(),
        html.Br(),
        html.P('Select Time'),
        dropdown_hour,
        html.Br(),
        html.P("Input Temperature"),
        temperature,
        html.Br(),
        html.Br(),
        html.P('Input the number of Attendees to the Event'),
        attendance,
        html.Br(),
        html.Br()]), width = 6),
    dbc.Col(html.Div([
        html.P("The distance of the Event to the middle of the Naamsestraat (in meters):"),
        distance,
        html.Br(),
        html.P("Expected Rain Density: (mm/m^3)"),
        dropdown_rain_density,
        html.Br(),
        html.P('Expected Rain Amount: (mm)'),
        dropdown_rain_amount,
        html.Br(),
        predict_button
            ]), width = 6
    )])

# Define the page layout
layout = dbc.Container([    
    html.Br(),
    dbc.Row([
        html.Center(html.H1("Noise Prediction Model")),
        html.Br(),
        html.Hr(),
        html.P('We used meteorology data, noise data, and Facebook Events data to model the Noise Output.'),
        html.P('We compared different algorithms and selected Light Gradient Boosting Machine since it has the lowest error and highest R2.'),
        fb_events_table.dashtable_methods,
        dbc.Col([
            html.Br(),
            html.P('Fit on median values very good, no big overfitting and residuals look evenly distributed.'),
            html.Img(src=fb_events_images.res_pred_dist, style={'height':'50%','width':'90%'}),
            html.Br(),
            html.Br(),
            html.P('For the hours we see that the later it gets, the less impact it has on the output of the predicted noise level. Also thursday seems to be the most influential day.'),
            html.Img(src=fb_events_images.other_plot, style={'height':'40%','width':'90%'})
        ]),
        dbc.Col([
            html.Br(),
            html.P('Temperature, attendance numbers and distance of event to measurement location seem to be the most important factores, followed by the two rain factors and the number of events that day. The other factors do not have much impact on the outcome.'),
            html.Img(src=fb_events_images.feature_importance, style={'height':'90%','width':'100%'})
            ]),
        html.Div([
        html.Br(),
        html.Br(),        
        html.P('You can predict the sound level by chosing parameters below then clicking Predict button.'),
        parameters,
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
            html.P(''),
            html.Div(id = 'prediction-output', children = [])
            ], width = 5),
        dbc.Col([
            dcc.Graph(id = 'prediction-plot', figure = go.Figure())]
        , width= 5)])],
        style = {'padding': '1rem'})
        ])
], style={'padding': '2rem'})

@app.callback(
    Output("prediction-output", "children"),
    Output("prediction-plot", 'figure'),
    Input("predict_button", 'n_clicks'),
    State("parameter_date", "date"),
    State("parameter_time", "value"),
    State("parameter_temperature", "value"),
    State("parameter_attendance", "value"),
    State("parameter_distance", "value"),
    State("parameter_rain_density", "value"),
    State("parameter_rain_amount", "value")
)

def render_predict(n_click, datee, time, temp, n, dist, rain_dens, rain_amount):
    d = date.fromisoformat(datee)
    day = d.day
    month = d.month
    if n_click:
        result = fb_events_model.predict_noise(month, day, time, temp, dist/1000, n, rain_dens, rain_amount)
        out1 = 'The expected average noise level for following parameters:'
        out2 = f'    Date: {d}'
        out3 = f'    Time: {time}:00' 
        out3 = f'    Temperatue: {temp} C'
        out4 = f'    Distance to the Naamsestraat: {dist} m'
        out4_2 = 'Selected Rain Density and Amount'
        out5 = 'The predicted noise levels are:'
        out6 = f'    50th Percentile: {result[0]}'
        out7 = f'    75th Percentile: {result[1]}'
        out8 = f'    99th Percentile: {result[2]}'
        out9 = f'    99.5th Percentile: {result[3]}'
        out10 = 'The boxplot for the prediction is shown below. Note that, we do not predict 0th and 25th percentile noise levels but they are plotted (assuming Gaussian distrubiton) for technical reasons.'

        out = html.P([out1, html.Br(), 
                      html.Ul([
                          html.Li(out2),
                          html.Li(out3),
                          html.Li(out4),
                          html.Li(out4_2)
                      ]),
                      html.Br(), out5, html.Br(),
                      html.Ul([
                          html.Li(out6),
                          html.Li(out7),
                          html.Li(out8),
                          html.Li(out9)
                      ]),
                      html.Br(), out10, html.Br()])

        figure = plot_prediction.create_boxplot(result)
        return out, figure
    else:
        return '', go.Figure()
    