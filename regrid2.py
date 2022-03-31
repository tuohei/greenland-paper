import numpy as np
import netCDF4 as nc4
import xarray as xr
import sys
from scipy.interpolate import griddata
import dask.array as da
import glob
datadir = '/mnt/data/greenland/decor/div_des2021/'
datadir2 = '/mnt/data/greenland/decor/divQ/'
fname_grid = f'{datadir2}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc'
d = xr.open_dataset(fname_grid)
lats = d['LAT'].data
lons = d['LON'].data
x = d['x'].data
y = d['y'].data
#var = 'var65'
var = 'divQ'
paths = glob.glob(f'{datadir}/divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.sign2000.pos.nc')
#paths = glob.glob(f'{datadir}/{var}.WN?-?.*greenland_box*.trend.nc')
for fname in paths:
#fname = f'{datadir}/reg.divQ.WN0.LP.1979-2018.10d_rm.nc'
    spath = f'{fname[:-3]}.regrid.nc'
    d = xr.open_dataset(fname)
    lon = d['lon'].data
    lat = d['lat'].data
    divq = d[var].data
    lon,lat = np.meshgrid(lon,lat)
    a = np.array(divq)
    print(a.shape)
    p = np.array([np.ravel(lon),np.ravel(lat)]).T
    #ls = lons.shape[1]
    #lls = lons.shape[0]
    b = a[:,:]
    ipd_data = griddata(p, np.ravel(b), (lons,lats), method='linear')
    #var = 'U'
    data =xr.Dataset({var: (['y','x'],ipd_data),
                        'lat': (['y','x'],lats),
                        'lon': (['y','x'],lons)},
                        coords= {'y': (['y'],y),'x': (['x'],x)}) 
    #
    #
    data.to_netcdf(spath)
#

