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
paths1 = sorted(glob.glob(f'{datadir}divE.W0-3.????.??.nc'))
paths2 = sorted(glob.glob(f'{datadir}divE.WN1-3.????.??.nc'))
for path1,path2 in zip(paths1,paths2):
   ofile = f'{path1[:-15]}0{path1[-11:]}'
   d1 = xr.open_dataset(path1)
   d2 = xr.open_dataset(path2)
   d = d1.divE - d2.divE
   d.to_netcdf(ofile)


