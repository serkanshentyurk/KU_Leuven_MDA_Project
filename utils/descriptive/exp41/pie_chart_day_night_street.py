
import pandas as pd
import plotly.graph_objects as go
from utils.descriptive.exp41 import preprocess41
from plotly.subplots import make_subplots

def create_pie_chart_day_night(street):
    if street == 0:
        df_E = preprocess41.df_E
    else:
        df_E = preprocess41.df_E[preprocess41.df_E['description'] == street]
    # Categorize hours as daytime or nighttime
    def categorize_time(hour):
        if hour >= 22 or hour < 6:
            return 'Nighttime'
        else:
            return 'Daytime'

    # Apply the categorization function to create 'Time_of_day' column
    df_E['Time_of_day'] = df_E['hour'].apply(categorize_time)

    # Calculate the sums for nighttime and daytime
    nighttime_sums = df_E[df_E['Time_of_day'] == 'Nighttime'].groupby('noise_event_laeq_primary_detected_class')['noise_event_laeq_primary_detected_class'].count()
    daytime_sums = df_E[df_E['Time_of_day'] == 'Daytime'].groupby('noise_event_laeq_primary_detected_class')['noise_event_laeq_primary_detected_class'].count()

    # Create the data for the pie charts
    nighttime_labels = nighttime_sums.index.tolist()
    nighttime_sizes = nighttime_sums.values.tolist()
    daytime_labels = daytime_sums.index.tolist()
    daytime_sizes = daytime_sums.values.tolist()

    # Define color palette for both charts
    color_palette = [{'Transport road - Passenger car': 'rgb(255, 127, 14)',
        'Transport road - Siren': 'rgb(44, 160, 44)',
        'Human voice - Shouting': 'rgb(214, 39, 40)',
        'Music non-amplified': 'rgb(148, 103, 189)',
        'Human voice - Singing': 'rgb(140, 86, 75)',
        'Nature elements - Wind': 'rgb(31, 119, 180)'}]

    fig = make_subplots(rows=1, cols=2, subplot_titles=['Nighttime Distribution', 'Daytime Distribution'], specs=[[{'type': 'domain'}, {'type': 'domain'}]])

    fig.add_trace(go.Pie(
        labels=nighttime_labels,
        values=nighttime_sizes,
        marker=dict(colors=color_palette[:len(nighttime_labels)]),
        textinfo="none"),
        row=1, col=1)

    fig.add_trace(go.Pie(
        labels=daytime_labels,
        values=daytime_sizes,
        marker=dict(colors=color_palette[:len(daytime_labels)]),
        textinfo="none"),
        row=1, col=2)

    fig.update_layout(
        height=500,
        width=1000)

    return fig