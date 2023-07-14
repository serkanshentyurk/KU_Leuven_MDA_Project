import plotly.graph_objects as go

def create_boxplot(percentiles):
    fig = go.Figure()

    fig.add_trace(go.Box(
        median = [percentiles[0]],  # Median (50th percentile)
        q1=[2*percentiles[0] - percentiles[1]],  # First quartile (25th percentile)
        q3=[percentiles[1]],  # Third quartile (75th percentile)
        lowerfence=[2*percentiles[0] - percentiles[3]],  # Bottom whisker position
        upperfence=[percentiles[3]],  # Top whisker position
        boxpoints=False,  # Do not show individual points
        marker_color='blue',
        line_color='blue'
    ))

    fig.update_layout(
        yaxis=dict(title="Noise Level"),
        showlegend=False
    )

    return fig