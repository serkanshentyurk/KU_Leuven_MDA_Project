from utils.descriptive.exp40 import preprocess40
import plotly.graph_objects as go

def create_heatmap(street):
# Define the desired order of weekdays
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_N_filtered = preprocess40.df_N[preprocess40.df_N['description'] == street]

    # Calculate the average laf50_per_hour and laf01_per_hour values for each weekday and hour combination
    heatmap_data_laf50 = df_N_filtered.groupby(['weekday', 'hour'])['laf50_per_hour'].mean().unstack()
    heatmap_data_laf01 = df_N_filtered.groupby(['weekday', 'hour'])['laf01_per_hour'].mean().unstack()

    # Create the heatmap figure for laf50_per_hour
    fig_laf50 = go.Figure(data=go.Heatmap(
        z=heatmap_data_laf50.values,
        x=heatmap_data_laf50.columns,
        y=weekday_order,
        colorscale='YlGnBu',
        colorbar=dict(title='Average LAF50')
    ))
    fig_laf50.update_layout(
        title=f'Average LAF50 per Hour and Weekday - {street}',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Weekday')
    )

    fig_laf01 = go.Figure(data=go.Heatmap(
        z=heatmap_data_laf01.values,
        x=heatmap_data_laf01.columns,
        y=weekday_order,
        colorscale='YlGnBu',
        colorbar=dict(title='Average LAF01')
    ))
    fig_laf01.update_layout(
        title=f'Average LAF01 per Hour and Weekday - {street}',
        xaxis=dict(title='Hour'),
        yaxis=dict(title='Weekday')
    )
    return fig_laf50, fig_laf01