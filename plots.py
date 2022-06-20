from matplotlib import pyplot as plt
import cartopy.crs as ccrs
from math import floor, ceil


def all_data_plate_carree(lon, lat, ts, title):
    ''' Plot data and coastlines on Plate Carree projection'''
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()
    ax.coastlines()
    ax.contourf(lon, lat, ts[0], vmin=250, vmax=290, zorder=-3)
    ax.set_title(title)

def all_data_rotated_pole(lon, lat, ts, title):
    '''Plot data and coastlines on Rotated Pole projection'''
    projection = ccrs.RotatedPole(pole_longitude=-177.5, pole_latitude=37.5)
    ax = plt.axes(projection=projection)
    ax.set_global()
    ax.coastlines()
    ax.contourf(lon,lat,ts[0],vmin=250,vmax=290, transform=ccrs.PlateCarree(), zorder = -3)
    ax.set_title('Global Temperature - Rotated Pole Projection')


def multiple_projections(projections, ds):
    '''Plot data on multiple other projections. Projections as list.
    [ccrs.Robinson() / ccrs.InterruptedGoodeHomolosine() / ccrs.Mercator() / ccrs.Orthographic() / ccrs.PlateCarree()]'''

    ts_test = ds.ts.sel(time='2015-01-16', method='nearest')

    # plot data
    for proj in projections:
        plt.figure()
        ax = plt.axes(projection=proj)
        ax.coastlines()
        ax.gridlines()
        ts_test.plot(ax=ax, transform=ccrs.PlateCarree(),
                vmin=250, vmax=290, cbar_kwargs={'shrink': 0.4}, zorder=-1)
        ax.set_title(f'{type(proj)}')

def diff_between_dates(ds, datevar):
    '''Plot data from the first and last months in dataset (01/2015 and 12/2099 respectively), and the difference between these'''

    date_years=[datevar[0],datevar[-1]]

    for year in date_years:
        ts_test = ds.ts.sel(time=year, method='nearest')
        fig = plt.figure(figsize=(9,6))
        ax = plt.axes(projection=ccrs.Mercator())
        ax.coastlines()
        ax.gridlines()
        ts_test.plot(ax=ax, transform=ccrs.PlateCarree(),
                vmin=250, vmax=290, cbar_kwargs={'shrink': 0.4}, zorder=-3)

    ts_test_2 = ds.ts.sel(time=date_years[1], method='nearest')
    ts_test_1 = ds.ts.sel(time=date_years[0], method='nearest')
    fig = plt.figure(figsize=(9,6))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.coastlines()
    ax.gridlines()
    ax.set_title('difference')
    (ts_test_2-ts_test_1).plot(ax=ax, transform=ccrs.PlateCarree(),
            vmin=-3, vmax=3, cbar_kwargs={'shrink': 0.4}, zorder=-3)
    plt.title('difference: '+str(datevar[0])+' vs '+str(datevar[-1]))


def plot_monthly_trends(ds, datevar):
    '''plot monthly trends'''

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 3, figsize=(19, 15))
    fig.subplots_adjust(hspace=0.3, wspace=0.1)
    list_months=['January','February','March','April','May','June','July','August','September','October','November','December']

    for i in range(3):
        ax=ax1[i]
        (ds.ts.isel(time=i+40*12)-ds.ts.isel(time=i)).plot(ax=ax,vmin=-3,vmax=3,extend='both', zorder=-3)
        ax.set_title(list_months[i])

    for i in range(3):
        ax=ax2[i]
        (ds.ts.isel(time=i+3+40*12)-ds.ts.isel(time=i+3)).plot(ax=ax2[i],vmin=-3,vmax=3,extend='both', zorder=-3)
        ax.set_title(list_months[i+3])

    for i in range(3):
        ax=ax3[i]
        (ds.ts.isel(time=i+6+40*12)-ds.ts.isel(time=i+6)).plot(ax=ax,vmin=-3,vmax=3,extend='both', zorder=-3)
        ax.set_title(list_months[i+6])

    for i in range(3):
        ax=ax4[i]
        (ds.ts.isel(time=i+9+40*12)-ds.ts.isel(time=i+9)).plot(ax=ax4[i],vmin=-3,vmax=3,extend='both', zorder=-3)
        ax.set_title(list_months[i+9])

    fig.suptitle('Monthly trends: '+str(datevar[0])+' to '+str(datevar[-1]))


def plot_average_diff(ds_y):
    '''plot difference between average data for 2015 and 2099'''
    fig = plt.figure(figsize=(9,6))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.coastlines()
    ax.gridlines()
    (ds_y.ts.sel(year=2099)-ds_y.ts.sel(year=2015)).plot(ax=ax, zorder=-1, transform=ccrs.PlateCarree(), vmin=-3,vmax=3,extend='both', cbar_kwargs={'shrink': 0.4})
    plt.title('difference: 2015 vs 2099')


    # Compare these temperature differences with the average 2015-2099 value and the standard deviation.

    # Using standard arrays:


    #Mean
    ts_avg = np.mean(ts, axis=0)
    # calculate mean for all years and months
    ts_avg.shape

    #Standard deviation
    ts_std=np.std(ts, axis=0)
    ts_std.shape

    #Visualising mean and standard deviation on global scale
    minu = floor(np.min(ts_avg))
    maxu = ceil(np.max(ts_avg))

    # plot average 2015-2099 values and standard deviation
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4))
    fig.subplots_adjust(hspace=0.1, wspace=0.1)

    im1=ax1.pcolormesh(lon,lat,ts_avg,vmin=270,vmax=290)
    fig.colorbar(im1,ax=ax1)
    ax1.set_title('Temperature average 2015-2099')

    im2=ax2.pcolormesh(lon,lat,ts_std,vmin=0,vmax=10)
    fig.colorbar(im2,ax=ax2)
    ax2.set_title('Temperature standard deviation 2015-2099')
