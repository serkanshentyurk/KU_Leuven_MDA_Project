# Import necessary libraries 
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from pages import t1, t2, t3, t4, t5
from app import app


# Define the page layout
layout = dbc.Container([
    dcc.Tabs(id = 'tabs_descriptive', value = 'tab-1-descriptive', children = [
        dcc.Tab(label = 'Meteorology Data', value = 'tab-1-descriptive'),
        dcc.Tab(label = 'Export 40 Data', value = 'tab-2-descriptive'),
        dcc.Tab(label = 'Export 41 Data', value = 'tab-3-descriptive'),
        dcc.Tab(label = 'Export 42 Data', value = 'tab-4-descriptive'),
        dcc.Tab(label = 'Facebook Data', value = 'tab-5-descriptive')
    ]),
    html.Div(id = 'tab-content', children=[])
], style={'padding': '2rem'})

@app.callback(Output('tab-content', 'children'),
              Input('tabs_descriptive', 'value'))
def render_tab(tab):
    if tab == 'tab-1-descriptive':
        return t1.layout
    elif tab == 'tab-2-descriptive':
        return t2.layout
    elif tab == 'tab-3-descriptive':
        return t3.layout
    elif tab == 'tab-4-descriptive':
        return t4.layout
    elif tab == 'tab-5-descriptive':
        return t5.layout
    else:
        return "404 Page Error! Please choose a link"
