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
datadir = '/cluster/work/users/the038/Edivdat/divergence/anomalies/regrid/'
nrange = range(6)
paths = np.array(glob.glob(f'{datadir}divE*.regrid.nc'))

p_per_rank = int(len(paths)/size)
paths = paths[rank*p_per_rank:(rank+1)*p_per_rank]
for path in paths:
    dat = xr.open_dataset(path).astype('float32')
    dat.to_netcdf(f'{path[:-9]}rgrid.nc')
    print(f'{path} done. Removing old files.')
    try:
        os.remove(path)
    except OSError:
        print("Error while deleting file")
    print(f'Files for {path} removed.')
