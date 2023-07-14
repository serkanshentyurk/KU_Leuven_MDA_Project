import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import paths

# Replace 'data.json' with the actual filename of your JSON file
json_file_path = paths.path_fb_data

# Read the JSON file into a DataFrame
df_events = pd.read_json(json_file_path)

months = {'jan.': '01', 'feb.': '02', 'mrt.': '03', 'apr.': '04',
           'mei': '05', 'jun.': '06', 'jul.': '07', 'aug.': '08',
           'sep.': '09', 'okt.': '10', 'nov.': '11', 'dec.': '12'}

df_events['Day'] = df_events['Event.date'].str.split(', ').str[1].str.split(' ').str[0]
df_events['Month'] = df_events['Event.date'].str.split(' ').str[2].map(months)

# Make 'Day' and 'Month' columns numeric
df_events['Day'] = pd.to_numeric(df_events['Day'])
df_events['Month'] = pd.to_numeric(df_events['Month'])

# Create a new 'Year' column
df_events['Year'] = 2022  # replace with the actual year if it's different

# Create a new 'Date' column from 'Day', 'Month', and 'Year'
df_events['Date'] = pd.to_datetime(df_events[['Year', 'Month', 'Day']])

# Set 'Date' as the index
df_events = df_events.set_index('Date')

# Count events per day
event_counts = df_events.resample('D').size()

# Prepare data for the heatmap
z = np.zeros((7, 53))  # Matrix for 7 days and 53 weeks
for i in range(len(event_counts)):
    day_of_week = event_counts.index[i].dayofweek
    week_of_year = event_counts.index[i].weekofyear
    z[day_of_week][week_of_year-1] = event_counts.iloc[i]  # -1 because weekofyear starts from 1

# List of weekdays
weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

# Create a heatmap
fig = go.Figure(data=go.Heatmap(
    z=z,
    x=list(range(1, 54)),  # Week numbers
    y=weekdays,
    colorscale='YlOrRd',
))

fig.update_layout(
    title='Number of Events per Day in 2022',
    xaxis_nticks=53,
    xaxis_title='Week of the Year',
    yaxis_title='Day of the Week',
)

