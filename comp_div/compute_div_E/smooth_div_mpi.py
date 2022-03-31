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
startyr = 1988
endyr = 2018

months = ['01','02','03','04','05','06','07','08','09','10','11','12']
month = months[rank%len(months)]
years = np.repeat(np.arange(startyr,endyr+1,1),len(months))
year = years[rank]
print(f'rank {rank} computes {year}.{month}')
year = 1985
months = ['11','12']
month = months[rank]

# Paths for data directories
datadir = '/cluster/work/users/the038/Edivdat/divergence/'
n_low = 4
n_high = 5
fname = f'divE.WN{n_low}-{n_high}.'
# Defining the southernmost latitude of the datas
path = f'{datadir}{fname}{year}.{month}.nc'
ofile = f'{path[:-3]}.smoothed.nc'
cdo.smooth(input = path,output = ofile)

