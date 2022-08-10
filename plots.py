from matplotlib import pyplot as plt
import numpy as np
from get_coords import get_coords


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


def plot_cities(ds, city):

    coords = get_coords(city)

    # Get data for coords and plot
    coords = (ds.ts.sel(lon = coords[0], lat = coords[1], method = 'nearest')-273.15).plot(x="time")
    labels = city
    plt.legend(labels,loc='lower right')
    plt.title(f'SSP5_8.5 temperature projections for {labels}')


def plot_cities_annual(ds, cities):

    coords = get_coords(cities)

    # timeseries for yearly averages
    year_annual = (ds['ts']-273.15).groupby('time.year').mean(dim='time')
    for coord in coords:
        year_annual.sel(lon = coord[0], lat = coord[1], method = 'nearest').plot.line(x="year")
    labels = cities
    plt.legend(labels,loc='lower right')
    plt.title(f'SSP5_5.8 annual trends for {cities}')


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

def get_data_for_city(ds, ncset, city, lat, lon):
    coords = get_coords(city)

    latvals = lat[:]
    lonvals = lon[:]

    # find closest coord to city
    dist_sq = (lonvals - coords[0]) ** 2 + (latvals - coords[1]) ** 2
    minindex_flattened = dist_sq.argmin()
    closet_coord = np.unravel_index(minindex_flattened, lat.shape)
    
    ts = ncset['ts'][:]

    return city_temps