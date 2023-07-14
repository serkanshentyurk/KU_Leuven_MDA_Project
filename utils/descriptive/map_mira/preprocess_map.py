from utils.descriptive.exp40 import preprocess40
from utils.descriptive.meteo import preprocess_meteo
from utils.fb_events import preprocess_fb
import pandas as pd
from geopy.geocoders import Nominatim

df_40 = preprocess40.df_N
df_final = preprocess_meteo.df_final
df_groupby_hour = preprocess_meteo.df_groupby_hour
df_events = preprocess_fb.df_events_filtered

df_noise_meteo = df_groupby_hour.merge(df_40, left_on=['Month','Day','Hour'],
                                       right_on=['month','day','hour'],
                                       how='right')

#Merge meteo, noise and facebook data
df_noise_meteo_fb = df_noise_meteo.merge(df_events, left_on=['Month','Day'],
                                       right_on=['Month','Day'],
                                       how='left')

df_noise_meteo_fb['datetime'] = pd.to_datetime(df_noise_meteo_fb[['Year', 'Month', 'Day', 'Hour']])
df_noise_meteo_fb = df_noise_meteo_fb.drop(['Year', 'Month','Day','month','day','Event.date'], axis=1)

df_noise_meteo_fb.dropna(subset=['Event.location'], inplace=True)

unique_values = df_noise_meteo_fb['Event.location'].unique()
value_counts = df_noise_meteo_fb['Event.location'].value_counts()

df_location_events = pd.DataFrame({'Location': unique_values, 'Count': value_counts})

geolocator = Nominatim(user_agent="my_geocoder")

# Create empty lists to store the coordinates
latitudes = []
longitudes = []

# Iterate over the unique locations
for location in df_location_events['Location']:
    try:
        # Use geopy to geocode the location
        location_data = geolocator.geocode(location)
        if location_data is not None:
            # Append the latitude and longitude to the respective lists
            latitudes.append(location_data.latitude)
            longitudes.append(location_data.longitude)
        else:
            latitudes.append(None)
            longitudes.append(None)
    except:
        latitudes.append(None)
        longitudes.append(None)

# Add the latitude and longitude lists to the DataFrame
df_location_events['Latitude'] = latitudes
df_location_events['Longitude'] = longitudes

df_location_events.dropna(subset=['Latitude'], inplace=True)

