def geocode_location(location):
    try:
        location = geolocator.geocode(f'{location}')
        return location.latitude, location.longitude
    except:
        return None, None