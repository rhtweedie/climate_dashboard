# https://www.earthinversion.com/utilities/reading-NetCDF4-data-in-python/

# %%
from fileinput import close
import netCDF4 as netcdf
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt

# %%
DATA_FN = "hadgem3_gc31_ll_ssp5_8_5_data.nc"
f = netcdf.Dataset(DATA_FN)
print(f)

# %%
temp = f.variables['ts']
lat, lon = f.variables['lat'], f.variables['lon']
time = f.variables['time']

# %%
from plots import get_coords
city = "Sydney"
coords = get_coords(city)
print(coords)

# %%
latvals = lat[:]
lonvals = lon[:]

# %%
data_fn = "hadgem3_gc31_ll_ssp5_8_5_data.nc"
ds = xr.open_dataset(data_fn)

# %%
temp_closest_coords = (ds.ts.sel(lon = coords[0], lat = coords[1], method = 'nearest') - 273.15).values
print(temp_closest_coords)
timevals = time[:]

# %%
plt.plot(timevals, temp_closest_coords)
