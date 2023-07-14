from utils.descriptive.exp40 import preprocess40

import pandas as pd
import plotly.graph_objs as go
from datetime import datetime

def plot_time_series(street):
    # Filter the data for 'Naamsestraat 35' and create a new DataFrame
    filtered_df = preprocess40.df_N[preprocess40.df_N['description'] == street].copy()

    # Convert 'result_timestamp' column to datetime data type
    filtered_df['result_timestamp'] = pd.to_datetime(filtered_df['result_timestamp'], dayfirst= True)

    # Set 'result_timestamp' as the index
    filtered_df.set_index('result_timestamp', inplace=True)

    # Sort the DataFrame by 'result_timestamp'
    filtered_df.sort_index(inplace=True)

    # Calculate hourly and daily averages for laf50, laf25, and laf75
    hourly_laf50 = filtered_df['laf50_per_hour']
    hourly_laf25 = filtered_df['laf25_per_hour']
    hourly_laf75 = filtered_df['laf75_per_hour']
    filtered_df_50 = filtered_df['laf50_per_hour']
    daily_avg = filtered_df_50.resample('D').mean()
    monthly_avg = filtered_df_50.resample('M').mean() # Calculate monthly average

    # Identify the loudest and least loud months
    loudest_month = monthly_avg.idxmax().strftime('%B')  # Get the month with the highest average
    least_loud_month = monthly_avg.idxmin().strftime('%B')  # Get the month with the lowest average

    # Create a trace for hourly laf50 values
    trace_hourly_laf50 = go.Scatter(
        x=hourly_laf50.index,
        y=hourly_laf50,
        mode='lines',
        name='Hourly LAF50',
        line=dict(color='rgba(135, 206, 250, 1)')
    )

    # Create a trace for hourly average laf25 values
    trace_hourly_laf25 = go.Scatter(
        x=hourly_laf25.index,
        y=hourly_laf25,
        mode='lines',
        name='Hourly LAF25',
        line=dict(color='rgba(0, 0, 255, 0.3)', width=1.5)
    )

    # Create a trace for hourly average laf75 values
    trace_hourly_laf75 = go.Scatter(
        x=hourly_laf75.index,
        y=hourly_laf75,
        mode='lines',
        name='Hourly LAF75',
        line=dict(color='rgba(255, 165, 0, 0.3)', width=1.5)
    )

    # Create a trace for daily average values
    trace_daily = go.Scatter(
        x=daily_avg.index,
        y=daily_avg,
        mode='markers',
        name='Daily Average',
        marker=dict(symbol='circle', size=4, color='blue')
    )

    # Create a trace for monthly average values
    trace_monthly_avg = go.Scatter(
        x=monthly_avg.index,
        y=monthly_avg,
        mode='lines',
        name='Monthly Average',
        line=dict(color='rgba(0, 0, 255, 0.8)', width=2)  # Change the color and line width
    )

    # Add annotations for loudest and least loud months
    annotations = [
        dict(
            x=monthly_avg.idxmax(),
            y=monthly_avg.max(),
            xref='x',
            yref='y',
            text=f"Loudest: {loudest_month}",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=-40
        ),
        dict(
            x=monthly_avg.idxmin(),
            y=monthly_avg.min(),
            xref='x',
            yref='y',
            text=f"Least Loud: {least_loud_month}",
            showarrow=True,
            arrowhead=7,
            ax=0,
            ay=40
        )
    ]

    # Create the plot layout with white background and annotations
    layout = go.Layout(
        title=f'Time Series of Sound Levels - {street}',
        yaxis=dict(title='dB(A)'),
        showlegend=True,
        plot_bgcolor='white',
        annotations=annotations
    )

    # Create the figure and add the traces
    figure_time_series = go.Figure(data=[trace_hourly_laf25, trace_hourly_laf75, trace_hourly_laf50, trace_daily, trace_monthly_avg], layout=layout)
    return figure_time_series