from utils import paths
import pandas as pd
from utils.fb_events import distance
from geopy.geocoders import GoogleV3


df_events = pd.read_json(paths.path_fb_data)

# Extract day and month from date column
months = {'jan.': '01', 'feb.': '02', 'mrt.': '03', 'apr.': '04',
           'mei': '05', 'jun.': '06', 'jul.': '07', 'aug.': '08',
           'sep.': '09', 'okt.': '10', 'nov.': '11', 'dec.': '12'}

df_events['Day'] = df_events['Event.date'].str.split(', ').str[1].str.split(' ').str[0]
df_events['Month'] = df_events['Event.date'].str.split(' ').str[2].map(months)

# Cleaning attendance column

# dropping events with missing attendance numbers
df_events = df_events.dropna(subset=['Event.attendance'])

# Split the column by the delimiter " · " into two new columns
df_events[['Interested', 'Attended']] = df_events['Event.attendance'].str.split(' · ', n=1, expand=True)

# Remove "geïnteresseerd" and "zijn gegaan" from the strings
df_events['Interested'] = df_events['Interested'].str.replace(' geïnteresseerd', '')
df_events['Interested'] = df_events['Interested'].str.replace(' zijn geweest', '')
df_events['Attended'] = df_events['Attended'].str.replace(' zijn gegaan', '')

# Replace the comma (',') with a dot ('.') in the columns
df_events['Interested'] = df_events['Interested'].str.replace(',', '.')
df_events['Attended'] = df_events['Attended'].str.replace(',', '.')

#Check which columns contain "d."
contains_d_interested = df_events['Interested'].str.contains('d\.')
contains_d_attended = df_events['Attended'].str.contains('d\.').apply(lambda x: False if pd.isna(x) else x)

#Extract numeric values only and convert column to numeric
df_events['Interested'] = pd.to_numeric(df_events['Interested'].str.findall(r'\d+\.\d+|\d+').apply(lambda x: x[0]))
df_events['Attended']= pd.to_numeric(df_events['Attended'].str.findall(r'\d+\.\d+|\d+').apply(lambda x: x[0] if isinstance(x, list) else None))

#Multiplying value containing d. by 1000
df_events.loc[contains_d_interested, 'Interested'] *= 1000
df_events.loc[contains_d_attended, 'Attended'] *= 1000

#make day and month column numeric
df_events['Day'] = pd.to_numeric(df_events['Day'])
df_events['Month'] = pd.to_numeric(df_events['Month'])

# Adding Interested and Attended numbers to new column
df_events['Attended'].fillna(0, inplace=True)

df_events['attendance'] = df_events['Attended'] + df_events['Interested']

df_events.drop(['Attended','Interested'], axis = 1, inplace = True)

# Initialize the Google Maps Geocoding API client
geolocator = GoogleV3(api_key='AIzaSyBCy_DQ-gtOItHXqAXvaEoMmMnxiUbib7Q')

# Define the reference location coordinates of point mid Naamsestraat
ref_lat = 50.874949  # Latitude of the reference location
ref_lon = 4.700150  # Longitude of the reference location


# Function to geocode a location name and return its coordinates
def geocode_location(location):
    try:
        location = geolocator.geocode(f'{location}')
        return location.latitude, location.longitude
    except:
        return None, None

# Geocode each location in the DataFrame and calculate the distance to the reference location
df_events['latitude'], df_events['longitude'] = zip(*df_events['Event.location'].apply(geocode_location))
df_events['Distance'] = df_events.apply(lambda row: distance.calculate_distance(ref_lat, ref_lon, row['latitude'], row['longitude']), axis=1)

# Drop irrelevant columns
df_events.drop(['Event.title', 'Event.attendance', 'longitude', 'latitude'], axis=1, inplace=True)

# Only include events under 1km to measurement points and drop missing values
df_events_filtered = df_events[df_events['Distance'] <= 1]
df_events_filtered.dropna(inplace=True)

