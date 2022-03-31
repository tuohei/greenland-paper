import numpy as np
import netCDF4 as nc4
import xarray as xr
import sys
from scipy.interpolate import griddata
import glob
fstart = 'totrad.1979-2019.anom.10d_rm.nc'
#datadir = '/cluster/work/users/the038/divD_anom/divD/divergence/anomalies/'
datadir = '/cluster/work/users/the038/radiation/'
spath = f'{datadir}totrad/'
years = np.arange(1979,2018 +1, 1)
fname_grid = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc'
d = xr.open_dataset(fname_grid)
lats = d['LAT'].data
lons = d['LON'].data
x = d['x'].data
y = d['y'].data
fname = f'{datadir}{fstart}'
d = xr.open_dataset(fname)
lon = d['lon'].data
lat = d['lat'].data
lon,lat = np.meshgrid(lon,lat)
p = np.array([np.ravel(lon),np.ravel(lat)]).T
ls = lons.shape[1]
lls = lons.shape[0]

for year in years:
    dat = d.sel(time = (d.time.dt.year == year))
    time = dat.time
    divq = np.array(dat['SLH'].data)
    ndays = divq.shape[0]
    i_data = np.empty((len(time),len(y),len(x)))
    for day in range(ndays):
        b = divq[day,:,:]
        ipd_data = griddata(p, np.ravel(b), (lons,lats), method='linear')
        i_data[day,:,:] = ipd_data
    data = xr.Dataset({'LWS': (['time','y','x'],i_data),
                    'lat': (['y','x'],lats),
                    'lon': (['y','x'],lons)},
                    coords= {'y': (['y'],y),'x': (['x'],x),'time': time}) 
    data.to_netcdf(f'{spath}/{fstart[:-3]}.{year}.regrid.nc')
    print(f'{year} complete')
