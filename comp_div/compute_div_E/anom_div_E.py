import numpy as np
import netCDF4 as nc4
import glob
import xarray as xr
import pandas as pd

## GLOBALS

# Start and end years
startyr = 1979
endyr = 2018
numyrs = endyr - startyr + 1
years = np.arange(startyr,endyr+1,1)
ndays_yr = 365
years = np.arange(startyr,endyr +1,1)
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
# Paths for data directories
datadir = '/cluster/work/users/the038/Edivdat/divergence/'
varname = 'divE'
n_low = 4
n_high = 5
fname = f'divE.WN{n_low}-{n_high}.'
first = True
for year in years:
    paths = sorted(glob.glob(f'{datadir}{fname}{year}*.smoothed.nc'))
    print(f'computing {year}')
    d = xr.open_mfdataset(paths, concat_dim = 'time')
    d = d.sortby(d.time)
    d = d.sel(time=~((d.time.dt.month == 2) & (d.time.dt.day == 29)))
    if first:
        first = False
        smb = np.array(d[varname].data)
    else:
        smb += np.array(d[varname].data)
data = xr.DataArray(smb/numyrs,coords = [d.time,d.lat,d.lon],dims = ['time','lat','lon'])
data.name = varname
# Length of running mean
flen = 11
# Extra data points
ed = int((flen -1)/2)
temp_data = xr.concat([data[-ed:,:,:],data,data[:ed,:,:]],'time')
data = temp_data.rolling(center = True, time = flen).mean().dropna('time')
data.name = varname
data.to_netcdf(f'{datadir}{fname}smoothed.yearmean.nc')

