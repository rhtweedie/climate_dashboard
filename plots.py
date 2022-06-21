from matplotlib import pyplot as plt
import numpy as np
from geopy.geocoders import Nominatim



def plot_monthly_trends(ds, datevar):
    '''plot monthly trends'''

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 3, figsize=(19, 15))
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    list_months=['January','February','March','April','May','June','July','August','September','October','November','December']

    for i in range(3):
        ax=ax1[i]
        (ds.ts.isel(time=i+40*12)-ds.ts.isel(time=i)).plot(ax=ax, vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i])

    for i in range(3):
        ax=ax2[i]
        (ds.ts.isel(time=i+3+40*12)-ds.ts.isel(time=i+3)).plot(ax = ax2[i], vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+3])

    for i in range(3):
        ax=ax3[i]
        (ds.ts.isel(time=i+6+40*12)-ds.ts.isel(time=i+6)).plot(ax = ax, vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+6])

    for i in range(3):
        ax=ax4[i]
        (ds.ts.isel(time=i+9+40*12)-ds.ts.isel(time=i+9)).plot(ax = ax4[i], vmin=-3, vmax=3, extend='both', zorder=-3)
        ax.set_title(list_months[i+9])

    fig.suptitle('Monthly trends: '+str(datevar[0])+' to '+str(datevar[-1]))


def get_coords(cities):
    '''Get coordinates for selected cities'''

    #https://github.com/geopy/geopy
    #https://developers.google.com/maps/documentation/geocoding/overview
    geolocator = Nominatim(user_agent="Google Geocoding API (V3)")
    location = geolocator.geocode("London")
    print(location.address)
    print(geolocator.geocode("London").longitude, geolocator.geocode("London").latitude)

    coords = []

    for city in cities:
        # Get coords of cities
        (lon, lat) = geolocator.geocode(city).longitude,geolocator.geocode(city).latitude
        coords = coords.append((lon, lat))
    return coords


def plot_cities(ds, cities):

    coords = get_coords(cities)

    # Get data for coords and plot
    for coord in coords:
        (ds.ts.sel(lon = coord[0], lat = coord[1], method = 'nearest')-273.15).plot(x="time")
    labels = cities
    plt.legend(labels,loc='lower right')
    plt.title(f'SSP5_8.5 temperature projections for {labels}')


def subset_data(datevar, lat, lon):
    # Get indices of time, lat and lon over the area
    years = np.array([idx.year for idx in datevar])

    idx_lat_region  = (lat>=-90) * (lat<=90.0)
    idx_lon_region  = (lon>=0) * (lon<=360)
    idx_tim_region = (years>=2015) * (years<=2099)
    # lat: -90 - 90
    # lon: 0 - 360
    # time: 2015 - 2099

    lat_region = lat[idx_lat_region]
    lon_region = lon[idx_lon_region]
    dates_region  = datevar[idx_tim_region]

    return lat_region, lon_region, dates_region
