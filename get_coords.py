from geopy.geocoders import Nominatim

def get_coords(city):
    '''Get coordinates for selected cities'''
    geolocator = Nominatim(user_agent="Google Geocoding API (V3)")
    coords = (geolocator.geocode(city).longitude, geolocator.geocode(city).latitude)
    return coords

