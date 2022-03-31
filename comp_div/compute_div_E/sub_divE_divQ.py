import numpy as np
import netCDF4 as nc4
import glob
from cdo import Cdo
import xarray as xr
#comm = MPI.COMM_WORLD
#size = comm.Get_size()
#rank = comm.Get_rank()

cdo = Cdo()
#cdo.debug = True
## GLOBALS

# Start and end years


datadir = '/cluster/work/users/the038/Edivdat/divergence/'
datadir2 = '/cluster/work/users/the038/divQ_anom/divQ/divergence/'
paths1 = sorted(glob.glob(f'{datadir}divE.W0-4-5.????.??.greenland_box.nc'))
paths2 = sorted(glob.glob(f'{datadir2}divQ.W0-4-5.????.??.greenland_box.nc'))
for path1,path2 in zip(paths1,paths2):
    ofile = f'{path1[:-33]}D.W0-4-5{path1[-25:]}'
    print(ofile)
    d1 = xr.open_dataset(path1)
    d2 = xr.open_dataset(path2)
    d = d1.divE - d2.divQ
    d.name = 'divD'
    d.to_netcdf(ofile)


