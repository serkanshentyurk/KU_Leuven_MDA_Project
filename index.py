# Import necessary libraries 
from dash import Dash, html, dcc, Input, Output, State, callback
from dash.dependencies import Input, Output
# Connect to main app.py file
from app import app
# Connect to your app pages
from pages import Q1, A1, home

# Connect the navbar to the index
from Components import navbar
# Define the navbar
nav = navbar.Navbar()

# Define the index page layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    nav, 
    html.Div(id='page-content', children=[]),
 
])

# Create the callback to handle mutlipage inputs
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/predictions':
        return Q1.layout
    elif pathname == '/visuals':
        return A1.layout

    elif pathname == '/home':
        return home.layout
    elif pathname == '/':
        return home.layout
    else: # if redirected to unknown link
        return "404 Page Error! Please choose a link"

if __name__ == '__main__':
    app.run_server(debug=True)
