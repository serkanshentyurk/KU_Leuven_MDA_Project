# Import necessary libraries 
from dash import html, dcc
import dash_bootstrap_components as dbc
from datetime import date
from dash.dependencies import Input, Output
from app import app
from utils.descriptive.exp42 import filter42, gather_exp42, geoplot


datepicker1 = dcc.DatePickerSingle(
    id='parameter_date',
    min_date_allowed=date(2022, 1, 1),
    max_date_allowed=date(2022, 1, 31),
    initial_visible_month=date(2022, 1, 1),
    date=date(2022, 1, 16),
    show_outside_days=True,
    day_size=32,
    display_format='DD/MM/YYYY',
    clearable=True,
    style={'zIndex': 10},
    )

hour = dcc.Slider(id='hour', value=12, min=0, max=23, step=1,
                    marks={
                        0: '0',
                        3: '3',
                        6: '6',
                        9: '9',
                        12: '12',
                        15: '15',
                        18: '18',
                        21: '21',
                        23: '23'}
                        )


# Define the page layout
layout = dbc.Container([
    dbc.Row([
        html.Center(html.H1("Exp 42 Data")),
        html.Br(),
        html.Hr(),
        dbc.Col([
            html.P("Export 42 Data contains hourly recorded Noise data for the month January."),
            html.P("Since it only covers January, we did not include it in our research."),
            html.P('However, we decided to visualise it regardless.'),
            html.P('You can select date and time below and observe the noise levels from geoplots :)'),
            html.Br(),
            datepicker1,
            html.Br(),
            hour,
        ]), 
        dbc.Col([
            html.P("Laeq:"),
            dcc.Graph(id = 'exp42-laeq', figure = {}),
            html.Br(),
            html.P('Lamax:'),
            dcc.Graph(id = 'exp42-lamax', figure = {}),
            html.Br(),
            html.P('Lceq:'),
            dcc.Graph(id = 'exp42-lceq', figure = {}),
            html.Br(),
            html.P('LcPeak:'),
            dcc.Graph(id = 'exp42-lcpeak', figure = {})
        ])
        
    ])
], style={'padding': '2rem'})

@app.callback(
    Output('exp42-laeq', 'figure'),
    Output("exp42-lamax", "figure"), 
    Output("exp42-lceq", "figure"), 
    Output("exp42-lcpeak", "figure"), 
    Input("parameter_date", "date"),
    Input("hour", "value"))



def render_figures(date, time):

    df1 = gather_exp42.df1
    df2 = gather_exp42.df2
    df3 = gather_exp42.df3
    df4 = gather_exp42.df4
    

    df1_comb = filter42.filter_df(df1, date, time)
    df2_comb = filter42.filter_df(df2, date, time)
    df3_comb = filter42.filter_df(df3, date, time)
    df4_comb = filter42.filter_df(df4, date, time)

    fig1 = geoplot.create_fig(df1_comb)
    fig2 = geoplot.create_fig(df2_comb)
    fig3 = geoplot.create_fig(df3_comb)
    fig4 = geoplot.create_fig(df4_comb)
    return fig1, fig2, fig3, fig4
