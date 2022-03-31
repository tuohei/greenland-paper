import numpy as np
import netCDF4 as nc4
import xarray as xr
import sys
from mpi4py import MPI
from scipy.interpolate import griddata
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

fstart = 'divE.WN6..'
datadir = '/cluster/work/users/the038/Edivdat/divergence/anomalies/'
spath = '/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/'
years = np.arange(1982,2017+1,1)
#years = np.array([2004])
yr_p_rank = int(len(years)/size)
fname_grid = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc'
d = xr.open_dataset(fname_grid)
lats = d['LAT'].data
lons = d['LON'].data
x = d['x'].data
y = d['y'].data
years = years[rank*yr_p_rank:(rank+1)*yr_p_rank]
for year in years:
    fname = datadir + fstart + str(year) + '.anom.nc'
    d = xr.open_dataset(fname)
    lon = d['lon'].data
    lat = d['lat'].data
    divq = d['divE'].data
    nwaves = divq.shape[0]
    ndays = divq.shape[1]
    lon,lat = np.meshgrid(lon,lat)
    a = np.array(divq)
    p = np.array([np.ravel(lon),np.ravel(lat)]).T
    ls = lons.shape[1]
    lls = lons.shape[0]
    #print('here')
    for day in range(ndays):
        for wave in range(nwaves):
            b = a[wave,day,:,:]
            ipd_data = griddata(p, np.ravel(b), (lons,lats), method='linear')
            data = xr.Dataset({'divE': (['y','x'],ipd_data),
                            'lat': (['y','x'],lats),
                            'lon': (['y','x'],lons)},
                            coords= {'y': (['y'],y),'x': (['x'],x),'time': d.time[day]}) 
            #print('here2')#x = xr.DataArray(ipd_data,coords=[('lat',lats),('lon',lons)])


            #x.name = 'divQ'
            data.to_netcdf(f'{spath}{fstart[:-1]}{year}.n{wave}.t{day}.regrid.nc')


    print(f'{year} complete')
