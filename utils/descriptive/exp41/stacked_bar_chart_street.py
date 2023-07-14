import plotly.graph_objects as go
from utils.descriptive.exp41 import preprocess41

def create_stacked_bar_chart(street):
    if street == 0:
        df_E = preprocess41.df_E
    else: 
        df_E = preprocess41.df_E[preprocess41.df_E['description'] == street]
    # Group the data by hour and noise_event_laeq_primary_detected_class
    grouped_df = df_E.groupby(['hour', 'noise_event_laeq_primary_detected_class']).size().unstack()

    # Create a list of colors for the different classes
    colors = ['rgb(31, 119, 180)', 'rgb(255, 127, 14)', 'rgb(44, 160, 44)', 'rgb(214, 39, 40)', 'rgb(148, 103, 189)', 'rgb(140, 86, 75)']

    # Create a list to store the traces for each class
    traces = []

    # Iterate over each class
    for i, column in enumerate(grouped_df.columns):
        # Create a bar trace for the current class
        trace = go.Bar(
            x=grouped_df.index,
            y=grouped_df[column],
            name=column,
            marker=dict(color=colors[i])
        )
        traces.append(trace)

    # Create the stacked bar chart layout
    layout = go.Layout(
        title=f"Counts Distribution of Noise Events by Hour - {street}",
        xaxis=dict(title="Hour"),
        yaxis=dict(title="Count"),
        barmode="stack"
    )

    # Create the figure with the traces and layout
    stacked_bar_chart = go.Figure(data=traces, layout=layout)
    
    return stacked_bar_chart
