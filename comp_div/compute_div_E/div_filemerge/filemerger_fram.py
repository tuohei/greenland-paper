import numpy as np
import netCDF4 as nc4
import xarray as xr
import sys
import os
from mpi4py import MPI
from scipy.interpolate import griddata
import dask.array as da
import glob
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
#### MERGE YEAR DATA #####
datadir = '/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/'
#years = np.arange(1979,2017+1,1)
##years = np.array([2004])
#nrange = range(6)
#yr_p_rank = int(len(years)/size)
#years = years[rank*yr_p_rank:(rank+1)*yr_p_rank]
#for year in years:
#    for n in nrange:
#        paths = glob.glob(f'{datadir}divE.WN6.{year}.n{n}.t*.rgrid.nc')
#        dat = xr.open_mfdataset(paths, concat_dim = 'time').sortby('time')
#        dt = dat['divE']
#        dt.to_netcdf(f'{datadir}divQ.n{n}.{year}.regrid.nc')
#        print(f'{year}, n = {n} done. Removing old files.')
#        for path in paths:
#            try:
#                os.remove(path)
#            except OSError:
#                print("Error while deleting file")
#        print(f'Files for {year} and n = {n} removed.')
#### MERGE n DATA #####
#datadir = '/cluster/work/users/the038/divQ_anom/regrid/'
#nrange = [0,1,2,3,4,5]
nrange = [1]
n = nrange[rank]
#n = 5
#yr_p_rank = int(len(years)/size)
#years = years[rank*yr_p_rank:(rank+1)*yr_p_rank]
paths = glob.glob(f'{datadir}divQ.n{n}.*.regrid.nc')
dat = xr.open_mfdataset(paths, concat_dim = 'time').sortby('time')
dt = dat['divE']
dat.to_netcdf(f'{datadir}divE.n{n}.1979-2017.rgrid.nc')
