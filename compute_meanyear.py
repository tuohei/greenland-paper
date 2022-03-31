#!/usr/bin/env python
import numpy as np
import netCDF4 as nc4
import glob
import xarray as xr
import pandas as pd

## GLOBALS

# datadir = '/media/climate/climatefiles/the038/data/divD_greenland/'
datadir = "/mnt/data/greenland/massflux/"
varname = "UM"
fname = f"{datadir}south_west.Ucorr.1979-2018.daily.nc"
# fname = f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.nc'
d = xr.open_dataset(fname)
d = d.sel(time=~((d.time.dt.month == 2) & (d.time.dt.day == 29)))
# print(d.groupby('time.dayofyear').mean('time'))
# Start and end years
startyr = 1979
endyr = 2018
# numyrs = endyr - startyr + 1
years = np.arange(startyr, endyr + 1, 1)
ndata = len(years)
div = 0
for year in years:
    data = d.sel(time=d.time.dt.year == year)
    div += data[varname].data
div /= ndata
# data[varname].data = div
# print(data)
# flen = 11
## Extra data points
# ed = int((flen -1)/2)
# temp_data = xr.concat([data[-ed:,:,:],data,data[:ed,:,:]],'time')
# data = temp_data.rolling(center = True, time = flen).mean().dropna('time')
# data.name = varname
# data.to_netcdf(f'{datadir}{fname}divD.W4-5.1979-2018.greenland_box.smoothed.yearmean.nc')


# ndays_yr = 365
# years = np.arange(startyr,endyr +1,1)
# months = ['01','02','03','04','05','06','07','08','09','10','11','12']
## Paths for data directories
# datadir = '/media/climate/climatefiles/the038/data/divD_greenland/'
# varname = 'divD'
# n_low = 4
# n_high = 5
# fname = f'divD.WN{n_low}-{n_high}.'
# first = True
# for year in years:
#    paths = sorted(glob.glob(f'{datadir}{fname}{year}*.smoothed.nc'))
#    print(f'computing {year}')
#    d = xr.open_mfdataset(paths, concat_dim = 'time')
#    d = d.sortby(d.time)
#    d = d.sel(time=~((d.time.dt.month == 2) & (d.time.dt.day == 29)))
#    if first:
#        first = False
#        smb = np.array(d[varname].data)
#    else:
#        smb += np.array(d[varname].data)
data = xr.DataArray(div, coords=[data.time, data.y, data.x], dims=["time", "x", "y"])
data.name = varname
# Length of running mean
flen = 11
# Extra data points
ed = int((flen - 1) / 2)
temp_data = xr.concat([data[-ed:, :, :], data, data[:ed, :, :]], "time")
data = temp_data.rolling(center=True, time=flen).mean().dropna("time")
data.name = varname
data.to_netcdf(f"{fname[:-3]}.yearmean.nc")
