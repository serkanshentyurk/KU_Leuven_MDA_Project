import pandas as pd
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

# Extract the numbers from 'Event.attendance'
df_events[['Interested', 'Attended']] = df_events['Event.attendance'].str.split(' · ', n=1, expand=True)
df_events['Interested'] = df_events['Interested'].str.replace(' geïnteresseerd', '').str.replace(',', '.')
df_events['Attended'] = df_events['Attended'].str.replace(' zijn gegaan', '').str.replace(',', '.')

# Extract numeric values only and convert column to numeric
df_events['Interested'] = pd.to_numeric(df_events['Interested'].str.findall(r'\d+\.\d+|\d+').apply(lambda x: x[0] if x else None))
df_events['Attended'] = pd.to_numeric(df_events['Attended'].str.findall(r'\d+\.\d+|\d+').apply(lambda x: x[0] if x else None))

# Create a 'Weekday' column
df_events['Weekday'] = df_events.index.weekday

# List of weekdays
weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
colors = ['red', 'green', 'blue', 'orange', 'purple', 'yellow', 'cyan']

# Create a separate plot for each weekday
fig = go.Figure()

for i in range(7):

    fig.add_trace(go.Scatter(x=df_events[df_events['Weekday'] == i].index,
                             y=df_events[df_events['Weekday'] == i]['Attended'],
                             mode='markers',
                              marker=dict(color=colors[i]),  # Set color based on index
                             name=weekdays[i]))
    fig.update_layout(title='Attended Number over the Year',
                      xaxis_title='Date',
                      yaxis_title='Count')
