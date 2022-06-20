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
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import xarray as xr
from retrieve_data import retrieve_data
from math import floor, ceil
from plots import all_data_plate_carree, all_data_rotated_pole, multiple_projections, diff_between_dates, plot_monthly_trends, plot_average_diff
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


all_data_plate_carree(lon, lat, ts, "Global Temperature: Plate Carree")
all_data_rotated_pole(lon, lat, ts, "Global Temperature: Rotated Pole")
multiple_projections([ccrs.Robinson(), ccrs.InterruptedGoodeHomolosine()], ds)
diff_between_dates(ds, datevar)
plot_monthly_trends(ds, datevar)
plot_average_diff(ds_y)




# Using xarray functionalities:



# plot average 2015-2099 values and standard deviation

ds_avg = ds.ts.mean(dim='time')

fig = plt.figure(figsize=(16, 4))
fig.subplots_adjust(hspace=0.1, wspace=0.1)

ax1 = fig.add_subplot(121, projection = ccrs.Mercator())
ds.ts.mean(dim='time').plot.contourf(ax = ax1, transform = ccrs.PlateCarree(), vmin = 270, vmax = 290, extend='both', cbar_kwargs = {'shrink': 0.8})
ax1.add_feature(cfeature.COASTLINE)
ax1.gridlines()
ax1.set_title('Temperature average 2015-2099')

ax2 = fig.add_subplot(122, projection = ccrs.Mercator())
ds.ts.std(dim='time').plot.contourf(ax = ax2, transform = ccrs.PlateCarree(),vmin = 0, vmax = 10, extend = 'both', cbar_kwargs = {'shrink': 0.8})
ax2.add_feature(cfeature.COASTLINE)
ax2.gridlines()
ax2.set_title('Temperature standard deviation 2015-2099')



# Plotting trend maps with significance using hatchingg

# Putting the data in the right format for the cal_trend function:
start_year=2015-2015
num_years=85
start_month=0
num_months=12

ts_ym=ts.reshape(num_years,num_months,144,192)

nx=ts_ym.shape[2]
ny=ts_ym.shape[3]
ts_trend, ts_trend_ym, ts_sig_a, ts_sig_a_ym, ts_r_a, ts_r_a_ym, ts_int_a, int_a_ym = cal_trend(start_year, num_years, start_month, num_months, nx, ny, ts_ym)


# Faster way to calculate trends but does not provide significance (i.e. p-value):

nt, nlat, nlon = ts.shape
ngrd = nlon*nlat

#Linear trend calculation
ts_grd  = ts.reshape((nt, ngrd), order='F')
x       = np.linspace(1,nt,nt)
ts_rate = np.empty((ngrd,1))
ts_rate[:,:] = np.nan

for i in range(ngrd):
    y = ts_grd[:,i]
    if(not np.ma.is_masked(y)):
        z = np.polyfit(x, y, 1)
        ts_rate[i,0] = z[0]*120.0

ts_rate = ts_rate.reshape((nlat,nlon), order='F')


# Plot the trends directly from the newly created numpy.array:
fig = plt.figure(figsize=(9,6))

ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()
ax.coastlines()
ax.gridlines()
plt.pcolormesh(lon,lat,ts_rate,vmin=-1,vmax=1, zorder=-1)
plt.colorbar(ax=ax,shrink=0.4)
plt.title('Temperature trend (K/decade) for 2015-2099')


# Or we can create an xarray with the new calculated trends and plot with xarray functionalities:

#calculated with polyfit
data=ts_rate
ds_trend1 = xr.DataArray(data, coords=[ds.lat,ds.lon], dims=["longitude","latitude"])
fig = plt.figure(figsize=(9,6))
ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()
ax.gridlines()
(ds_trend1).plot(ax=ax, transform=ccrs.PlateCarree(), vmin=-1,vmax=1,extend='both', cbar_kwargs={'shrink': 0.4}, zorder=-1)
plt.title('Temperature trend (K/decade) for 2015-2099 - polyfit')


#Calculated with linregress
data=ts_trend
ds_trend = xr.DataArray(data, coords=[ds.lat,ds.lon], dims=["longitude","latitude"])
fig = plt.figure(figsize=(9,6))
ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()
ax.gridlines()
(10.*ds_trend).plot(ax=ax, transform=ccrs.PlateCarree(), vmin=-1,vmax=1,extend='both', cbar_kwargs={'shrink': 0.4}, zorder=-1)
plt.title('Temperature trend (K/decade) for 2015-2099 - linear regression')


#Massive difference in the results?gsize=(9,6))
ax = plt.axes(projection=ccrs.Mercator())
ax.coastlines()
ax.gridlines()
(10.*ds_trend-ds_trend1).plot(ax=ax, transform=ccrs.PlateCarree(),extend='both', cbar_kwargs={'shrink': 0.4}, zorder=-1)
plt.title('Difference between polyfit and linear regression methods')


# The two methods used to calculate trends in the data provide very similar results, with temperature change varying by up to only 0.02K.

# We now plot trends with their significance and mask irrelevant regions.

# For yearly trends:


# create color scheme and colorbar
biasContDist=0.1
rgrColorTable=np.array(['#4457c9','#4f67d4','#6988ea','#84a6f9','#9ebdff','#b7d0fd','#cfdcf3','#ffffff','#f1d7c8','#f9c5ab','#f7aa8c','#f28d72','#df6553','#c93137','#bc052b'])
iContNr=len(rgrColorTable)
iMinMax=12.*biasContDist/2.+biasContDist/2.
clevsTD=np.arange(-iMinMax,iMinMax+0.0001,biasContDist)

# plot data
data=ts_trend
ds_trend = xr.DataArray(data, coords=[ds.lat,ds.lon], dims=["longitude","latitude"])
fig = plt.figure(figsize=(24,18))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.gridlines()
cs=plt.contourf(lon,lat,ts_sig_a, hatches=['','///'],levels=[0,90,100], zorder=1, alpha=0)# ,transform=cartopy.crs.PlateCarree())
plt.contourf(lon,lat,10.*ds_trend,colors=rgrColorTable, extend='both',levels=clevsTD, zorder=0)

plt.title('Temperature trend (K/decade) for 2015-2099 ')
plt.colorbar(ax=ax,shrink=0.4)


# And for individual months:

# plot data for given month
list_months=['January','February','March','April','May','June','July','August','September','October','November','December']
month=8 #8 = September
data=ts_trend_ym[month]
ds_trend = xr.DataArray(data, coords=[ds.lat,ds.lon], dims=["longitude","latitude"])
fig = plt.figure(figsize=(22,15))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines()
ax.gridlines()
# cs=plt.contourf(lon,lat,ts_sig_a_ym[month], hatches=['xxx',''],levels=[0,90,100], zorder=1, alpha=0)# ,transform=cartopy.crs.PlateCarree()) #hatches not significant
cs=plt.contourf(lon,lat,ts_sig_a_ym[month], hatches=['','///'],levels=[0,90,100], zorder=1, alpha=0)# ,transform=cartopy.crs.PlateCarree()) #hatches significant
plt.contourf(lon,lat,10.*ds_trend,colors=rgrColorTable, extend='both',levels=clevsTD, zorder=0)
plt.title(list_months[month]+' temperature trend (K/decade) for 2015-2099 ')
plt.colorbar(ax=ax,shrink=0.4)


### 7) Selecting a sub-part of your data

# Subset and plot data for the sea around Iceland. This area was chosen as it is the only area of the world that is predicted by the model to become slightly cooler over the examined time period.


# Get indices of time, lat and lon over the area
years = np.array([idx.year for idx in datevar])

idx_lat_region  = (lat>=-90) * (lat<=90.0)
idx_lon_region  = (lon>=0) * (lon<=360)
idx_tim_region = (years>=2015) * (years<=2099)
# time: 2015-2099

lat_region = lat[idx_lat_region]
lon_region = lon[idx_lon_region]
dates_region  = datevar[idx_tim_region]



# Mask the original arrays (ts) and create a new smaller array (ts_region):

ts_region = ts[idx_tim_region, :, :][:, idx_lat_region, :][:, :, idx_lon_region]
print(ts_region.shape)
print(dates_region.shape)


# plot subsetted region

fig = plt.figure(figsize=(9,6))
ax = plt.axes(projection=ccrs.PlateCarree())
#ax = plt.axes(projection=ccrs.Mercator())
ax.set_global()
ax.coastlines()
plt.pcolormesh(lon_region,lat_region,ts_region[480],zorder=-1)#,vmin=-1,vmax=1)
# plt.contourf(lons,lats,t2m_rate, extend='both',vmin=-1,vmax=1)
lat1, lon1, lat2, lon2 = 80, -40, 40, 20
ax.set_extent([lon1, lon2, lat1, lat2], crs=ccrs.PlateCarree())
plt.colorbar(ax=ax,shrink=0.4)
plt.title('Surface Temperature of North Atlantic/Arctic Ocean around Iceland (K)')


### 8) Analysing timeseries near selected cities, localities etc

# Get coordinates for selected cities:

#https://github.com/geopy/geopy
#https://developers.google.com/maps/documentation/geocoding/overview
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Google Geocoding API (V3)")
location = geolocator.geocode("London")
print(location.address)
print(geolocator.geocode("London").longitude,geolocator.geocode("London").latitude)


# Get coords of cities
location_1 = "Jerusalem"
location_2 = "Cincinnati"
location_3 = "Stockholm"
lon1,lat1=geolocator.geocode(location_1).longitude,geolocator.geocode(location_1).latitude
lon2,lat2=geolocator.geocode(location_2).longitude,geolocator.geocode(location_2).latitude
lon3,lat3=geolocator.geocode(location_3).longitude,geolocator.geocode(location_3).latitude


# Get data for coords and plot
(ds.ts.sel(lon=lon1, lat=lat1, method = 'nearest')-273.15).plot(x="time")
(ds.ts.sel(lon=lon2, lat=lat2, method = 'nearest')-273.15).plot(x="time")
(ds.ts.sel(lon=lon3, lat=lat3, method = 'nearest')-273.15).plot(x="time")
labels = [location_1,location_2,location_3]
plt.legend(labels,loc='lower right')
plt.title('Compare SSP5_8.5 temperature record for ' + labels[0] +', '+ labels[1]+ ', and ' +labels[2])


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


# Timeseries for yearly averages:


# timeseries for yearly averages
year_annual = (ds['ts']-273.15).groupby('time.year').mean(dim='time')
year_annual.sel(lon=lon1, lat=lat1, method = 'nearest').plot.line(x="year")
year_annual.sel(lon=lon2, lat=lat2, method = 'nearest').plot.line(x="year")
year_annual.sel(lon=lon3, lat=lat3, method = 'nearest').plot.line(x="year")
labels = [location_1,location_2,location_3]
plt.legend(labels,loc='lower right')
plt.title('Yearly trends for ' + labels[0] +', '+ labels[1]+ ', and ' +labels[2])


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
