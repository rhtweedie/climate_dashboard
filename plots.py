from matplotlib import pyplot as plt

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
