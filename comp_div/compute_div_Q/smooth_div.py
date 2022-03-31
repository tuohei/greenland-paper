import numpy as np
import netCDF4 as nc4
import glob
from cdo import Cdo
import xarray as xr
import pandas as pd
cdo = Cdo()
## GLOBALS

# Start and end years
startyr = 1999
endyr = 2018
numyrs = endyr - startyr + 1
years = np.arange(startyr,endyr+1,1)
ndays_yr = 365
years = np.arange(startyr,endyr +1,1)
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
# Paths for data directories
datadir = '/cluster/work/users/the038/divQ_anom/divQ/divergence/'
varname = 'divQ'
n_low = 0
n_high = 3
fname = f'divQ.W{n_low}-{n_high}.'
# Defining the southernmost latitude of the dataset
first = True
for year in years:
    print(f'Computing year {year}.')
    paths = sorted(glob.glob(f'{datadir}{fname}{year}*.greenland_box.nc'))
    for path in paths:
        ofile = f'{path[:-3]}.smoothed.nc'
        cdo.smooth(input = path,output = ofile)

