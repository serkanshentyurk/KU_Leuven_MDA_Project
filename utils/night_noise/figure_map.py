import plotly.express as px
import pandas as pd

location_data = {
    'Naamsestraat 35': (50.877110, 4.700840),
    'Naamsestraat 57': (50.876490, 4.700700),
    'Naamsestraat 62': (50.875809, 4.700110),
    'Calvariekapel KU Leuven': (50.8745267, 4.6999168),
    'Parkstraat 2': (50.8741177, 4.7000138),
    'Kiosk Stadspark': (50.8752756, 4.7015081),
    'Naamsestraat 81': (50.8738250, 4.7001178),
    'Vrijthof': (50.8790375, 4.7011731),
    'His & Hears': (50.8752579, 4.7001115)
}

locations = pd.DataFrame(location_data.items(), columns=['Location', 'Coordinates'])
locations[['Latitude', 'Longitude']] = pd.DataFrame(locations['Coordinates'].tolist())

# Create a map + map layout 
figure_map = px.scatter_mapbox(locations, lat='Latitude', lon='Longitude',
                        size_max=40, color='Location',labels={'Location': 'Location'})

figure_map.update_layout(
    mapbox=dict(
        center=dict(lat=50.876490, lon=4.700700),
        zoom=14.7,
        style='carto-positron'
    ),
    showlegend=True
)