'''
This assignment analyses global surface temperature data from two Shared Socioeconomic Pathways scenarios,
SSP1_2.6 (best case scenario - sustainability) and SSP5_8.5 (worst case scenario - fossil-fueled development).
The Hadley Centre Global Environment Model version 3 (low resolution) (HadGEM3-GC31-MM) model is used.
This model was chosen for its low resolution, allowing analysis of a large, although less detailed, dataset.
Key analysis is performed on the SSP5-8.5 data with a brief comparison with SSP1-2.6 to conclude.
'''


# Import required libraries

from netCDF4 import Dataset as netcdf
from scipy import signal
from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import datetime
import scipy.stats as stats
import cftime
import warnings
import pandas as pd
import statsmodels.api as sm
warnings.simplefilter('ignore')
import matplotlib.dates as mdateschan
from matplotlib.dates import MonthLocator, WeekdayLocator, DateFormatter
import matplotlib.ticker as ticker
from matplotlib.pylab import rcParams
import matplotlib.dates as mdates
from matplotlib import pyplot as plt
import xarray as xr
from retrieve_data import retrieve_data
from math import floor, ceil
from plots import plot_monthly_trends, get_coords, plot_cities
from cal_trend import cal_trend




##########################################################################################################################################################################################
# Prepare data                                                                                                                                                                           #
##########################################################################################################################################################################################


# define constant variables
TEMP_RES = 'monthly'
EXPERIMENT = 'ssp5_8_5'
VARIABLE = 'surface_temperature'
MODEL = 'hadgem3_gc31_ll'
DATE = '2015-01-01/2099-12-31'


# retrieve data
data_fn = retrieve_data(TEMP_RES, EXPERIMENT, VARIABLE, MODEL, DATE)
ncset = netcdf(data_fn, mode='r')


# check which variables are in the netcdf file
print(ncset.variables)
ncset.set_auto_mask(False)


# read variables
lon = ncset['lon'][:]
lat = ncset['lat'][:]
t = ncset['time'][:]
ts = ncset['ts'][:]
nctime = ncset.variables['time'][:]
t_unit = ncset.variables['time'].units
ncset.close()

try:
    t_cal = ncset.variables['time'].calendar
    t_cal = nctime.calendar
except AttributeError:
    t_cal = u"360_day"

datevar = cftime.num2date(nctime, units=t_unit, calendar=t_cal)


# lon lat on a grid
[lon, lat] = np.meshgrid(lon, lat)

# print first and last dates, for later reference
print(datevar[0])
print(datevar[-1])

# load data
ds = xr.open_dataset(data_fn)
lat = ds.lat
lon = ds.lon
ds_y = ds.groupby('time.year').mean(dim='time')



##########################################################################################################################################################################################
# Plot data                                                                                                                                                                              #
##########################################################################################################################################################################################


plot_monthly_trends(ds, datevar)

cities = ["Jerusalem", "Cincinnati", "Stockholm"]
plot_cities(cities)


### 7) Selecting a sub-part of your data

# Subset and plot data for the sea around Iceland. This area was chosen as it is the only area of the world that is predicted by the model to become slightly cooler over the examined time period.






# Mask the original arrays (ts) and create a new smaller array (ts_region):

ts_region = ts[idx_tim_region, :, :][:, idx_lat_region, :][:, :, idx_lon_region]
print(ts_region.shape)
print(dates_region.shape)




### 8) Analysing timeseries near selected cities, localities etc





# plot temperature anomaly data for selected cities
def remove_time_mean(x):
    return x - x.mean(dim='time')

monthly_annual_anom = ds.ts.groupby('time.month').apply(remove_time_mean)
monthly_annual_anom.sel(lon=lon1, lat=lat1, method = 'nearest').plot.line(x="time")
monthly_annual_anom.sel(lon=lon2, lat=lat2, method = 'nearest').plot.line(x="time")
monthly_annual_anom.sel(lon=lon3, lat=lat3, method = 'nearest').plot.line(x="time")
labels = [location_1,location_2,location_3]
plt.legend(labels,loc='lower right')
plt.title('Compare SSP5_8.5 temperature anomaly record for ' + labels[0] +', '+ labels[1]+ ', and ' +labels[2])



# Timeseries for monthly averages:


# timeseries for a given month
month=8 #9:September
month_name = 'September'
(ds.ts.sel(lon=lon1, lat=lat1,time=ds['time.month']==month, method = 'nearest')-273.15).plot.line(x="time")
(ds.ts.sel(lon=lon2, lat=lat2,time=ds['time.month']==month, method = 'nearest')-273.15).plot.line(x="time")
(ds.ts.sel(lon=lon3, lat=lat3,time=ds['time.month']==month, method = 'nearest')-273.15).plot.line(x="time")
labels = [location_1,location_2,location_3]
plt.legend(labels,loc='lower right')
plt.title(month_name + ' trends for ' + labels[0] +', '+ labels[1]+ ', and ' +labels[2])


# Time series for a given season. Adapted from http://atedstone.github.io/rate-of-change-maps/


# timeseries for a given season
season_str='JJA' #('DJF','MAM','JJA','SON')
season_annual = ds['ts'].where(ds['ts']['time.season'] == season_str).groupby('time.year').mean(dim='time')
season_annual.sel(lon=lon1, lat=lat1, method = 'nearest').plot.line(x="year")
season_annual.sel(lon=lon2, lat=lat2, method = 'nearest').plot.line(x="year")
season_annual.sel(lon=lon3, lat=lat3, method = 'nearest').plot.line(x="year")
labels = [location_1,location_2,location_3]
plt.legend(labels,loc='lower right')
plt.title('Compare seasonal trends ('+ season_str+')')


# Compare different model scenarios

# Compare yearly trends for three cities as predicted by SSP5_8.5 and SSP1_2.6:


# plot yearly trends for three cities as predicted by SSP5_8.5 and SSP1_2.6
fig = plt.figure(figsize=(20, 6))
fig.subplots_adjust(hspace=0.1, wspace=0.1)

# set y axis limits for consistency across figure
ylimits = (5, 30)

ax1 = fig.add_subplot(121, ylim = ylimits)
year_annual126 = (ds['ts']-273.15).groupby('time.year').mean(dim='time')
year_annual126.sel(lon=lon1, lat=lat1, method = 'nearest').plot.line(ax = ax1, x="year")
year_annual126.sel(lon=lon2, lat=lat2, method = 'nearest').plot.line(ax = ax1, x="year")
year_annual126.sel(lon=lon3, lat=lat3, method = 'nearest').plot.line(ax = ax1, x="year")
labels = [location_1,location_2,location_3]
plt.title('SSP5_8.5 Yearly Trends')
plt.legend(labels,loc='lower right')

ax2 = fig.add_subplot(122, ylim = ylimits)
year_annual = (ds126['ts']-273.15).groupby('time.year').mean(dim='time')
year_annual.sel(lon=lon1, lat=lat1, method = 'nearest').plot.line(ax = ax2, x="year")
year_annual.sel(lon=lon2, lat=lat2, method = 'nearest').plot.line(ax = ax2, x="year")
year_annual.sel(lon=lon3, lat=lat3, method = 'nearest').plot.line(ax = ax2, x="year")
labels = [location_1,location_2,location_3]
plt.title('SSP1_2.6 Yearly Trends')


# Compare global predicted temperature trends for SSP5_8.5 and SSP1_2.6:

# calculate trend in SSP_2.6 data

start_year=2015-2015
num_years=85
start_month=0
num_months=12

ts126_ym=ts126.reshape(num_years,num_months,144,192)

nx126=ts126_ym.shape[2]
ny126=ts126_ym.shape[3]
ts126_trend, ts126_trend_ym, ts126_sig_a, ts126_sig_a_ym, ts126_r_a, ts126_r_a_ym, ts126_int_a, int126_a_ym = cal_trend(start_year, num_years, start_month, num_months, nx126, ny126, ts126_ym)

data126=ts126_trend
ds126_trend = xr.DataArray(data126, coords=[ds126.lat,ds126.lon], dims=["longitude","latitude"])


# plot trend in global temperature change as predicted by SSP5_8.5 and SSP1_2.6

fig = plt.figure(figsize=(20,12))
fig.subplots_adjust(hspace=0.1, wspace=0.1)

ax1 = fig.add_subplot(121, projection=ccrs.Mercator())
ax1.coastlines()
ax1.gridlines()
(10.*ds_trend).plot(ax=ax1, transform=ccrs.PlateCarree(), vmin=-1,vmax=1,extend='both', cbar_kwargs={'shrink': 0.4}, zorder=-1)
plt.title('Temperature trend (K/decade) for 2015-2099, SSP5_8.5')

ax2 = fig.add_subplot(122, projection=ccrs.Mercator())
ax2.coastlines()
ax2.gridlines()
(10.*ds126_trend).plot(ax=ax2, transform=ccrs.PlateCarree(), vmin=-1,vmax=1,extend='both', cbar_kwargs={'shrink': 0.4}, zorder=-1)
plt.title('Temperature trend (K/decade) for 2015-2099, SSP1_2.6')


######################################################################################################################################################################################################
# Summary of key findings:                                                                                                                                                           #
#                                                                                                                                                                                   #
#- SSP5_8.5 predicts a global mean temperature increase of 0.5-1K/decade between 2015 and 2099 over land areas, with a lower but still significant increase over oceans             #
#- The only area expected to see cooling over this time period is a small area over the ocean to the east of Iceland                                                                #
#- SSP1_2.6 predicts a global mean temperature increase of 0-0.25K/decade, with warming of up to 1K per decade in the Arctic                                                        #
#- Warming trends predicted by SSP5_8.5 are statistically significant                                                                                                               #
#- For the three cities analysed (Stockholm, Jerusalem and Cincinnati), SSP5_8.5 predicts a temperature increase of approximately five degrees between 2015-99,                     #
#   while SSP1_2.6 predicts minimal temperature change                                                                                                                              #
######################################################################################################################################################################################################
