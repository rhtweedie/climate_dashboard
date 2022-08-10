#%%

from plots import plot_cities, plot_cities_annual
from retrieve_data import retrieve_data
import netCDF4 as netcdf
import numpy as np
import cftime
import xarray as xr


# define constant variables
TEMP_RES = 'monthly'
EXPERIMENT = 'ssp5_8_5'
VARIABLE = 'surface_temperature'
MODEL = 'hadgem3_gc31_ll'
DATE = '2015-01-01/2099-12-31'
DATA_FN = 'hadgem3_gc31_ll_ssp5_8_5_data.nc'


# retrieve data
ncset = netcdf.Dataset(DATA_FN, mode='r')

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


# load data
ds = xr.open_dataset(DATA_FN)
lat = ds.lat
lon = ds.lon
ds_y = ds.groupby('time.year').mean(dim='time')

# %%
cities = ["London"]
plot_cities(ds, cities)

# %%
