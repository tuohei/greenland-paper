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
#datadir = '/run/media/the038/external/data/era5/res0.5x0.5/divergence/'
datadir = '/cluster/work/users/the038/Edivdat/divergence/'
varname = 'divE'
n_low = 4
n_high = 5
fname = f'divE.WN{n_low}-{n_high}.'
fname2 = f'divE.WN{n_low}-{n_high}.smoothed.yearmean'
# Defining the southernmost latitude of the dataset
first = True
mm = xr.open_dataset(f'{datadir}{fname2}.nc')

for year in years:
    paths = sorted(glob.glob(f'{datadir}{fname}{year}*.smoothed.nc'))
    # print(paths)
    print(f'computing {year}')
    d = xr.open_mfdataset(paths, concat_dim = 'time')
    d = d.sortby(d.time)
    d = d.sel(time=~((d.time.dt.month == 2) & (d.time.dt.day == 29)))
    d[varname].data -= mm[varname].data
    d.to_netcdf(f'{datadir}anomalies/{fname}{year}.anom.nc')
    # data = xr.DataArray(smb/numyrs,coords = [d.time,d.y,d.x],dims = ['time','y','x'])
# print(d)
# print(smb.shape)
# data.name = varname
# data.to_netcdf(f'{datadir}{fname}_yearmean.nc')
