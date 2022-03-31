import numpy as np
import netCDF4 as nc4
import glob
from cdo import Cdo
from mpi4py import MPI
import xarray as xr
import pandas as pd
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()

cdo = Cdo()
## GLOBALS

# Start and end years
startyr = 1979
endyr = 2018

months = ['01','02','03','04','05','06','07','08','09','10','11','12']
month = months[rank%len(months)]
years = np.repeat(np.arange(startyr,endyr+1,1),len(months))
year = years[rank]
print(f'rank {rank} computes {year}.{month}')
#
#year = 1999
# Paths for data directories
datadir = '/cluster/work/users/the038/divQ_anom/divQ/divergence/'
n_low = 0
n_high = 3
fname = f'divQ.W{n_low}-{n_high}.'
# Defining the southernmost latitude of the datas
path = f'{datadir}{fname}{year}.{month}.nc'
ofile = f'{path[:-3]}.smoothed.nc'
cdo.smooth(input = path,output = ofile)

