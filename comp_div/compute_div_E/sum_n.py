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
fname = 'divE.WN6.'
# Defining the wavenumber interval for slice
n_low = 0
n_high = 5
first = True
for year in years:
	paths = sorted(glob.glob(f'{datadir}{fname}{year}*'))
	for path in paths:
		print(path)
		d = xr.open_dataset(path)
		d = d.sortby(d.time)
		d = d.sel(time=~((d.time.dt.month == 2) & (d.time.dt.day == 29)))
		d = d.sel(n = slice(n_low,n_high))
		d = d.sum(dim = 'n')
		d.time.attrs['bounds'] = 'time_bnds'
		d.lon.attrs['units'] = 'degrees_east'
		d.lat.attrs['units'] = 'degress_north'
		d.lon.attrs['long_name'] = 'longitude'
		d.lat.attrs['long_name'] = 'latitude'
		d.to_netcdf(f'{path[:-14]}WN{n_low}-{n_high}{path[-11:]}')
