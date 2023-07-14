import plotly.express as px
# from utils.descriptive.map_mira import preprocess_map
import pandas as pd
from utils import paths

def create_map():
    # df_location_events = preprocess_map.df_location_events
    df_location_events = pd.read_csv(paths.path_map)

    # Set Mapbox access token
    px.set_mapbox_access_token("your-access-token-here")

    # Create the bubble mapbox figure
    fig = px.scatter_mapbox(
        df_location_events,
        lat='Latitude',
        lon='Longitude',
        color='Count',
        size='Count',
        size_max=50,
        zoom=10,
        center=dict(lat=50.874949, lon=4.700150),
        mapbox_style='open-street-map',
        color_continuous_scale='Viridis',
        opacity=0.7,
        hover_data={'Count': True, 'Location': True}
    )

    return fig

map_figure = create_map()