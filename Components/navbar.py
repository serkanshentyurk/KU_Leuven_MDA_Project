# Import necessary libraries
from dash import html
import dash_bootstrap_components as dbc

# Define the navbar structure
def Navbar():

    layout = html.Div([
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Home", href="/home")),
                dbc.NavItem(dbc.NavLink("Data Explorations - Exploratory Visualisations", href="/visuals")),
                dbc.NavItem(dbc.NavLink("Noise Prediction Model", href="/predictions"))
            ] ,
            brand="MDA App",
            brand_href="/",
            color="dark",
            dark=True,
        ), 
    ])

    return layout