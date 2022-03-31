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


datadir = '/cluster/work/users/the038/divQ_anom/divQ/divergence/'
paths1 = sorted(glob.glob(f'{datadir}divQ.WN1-3.????.??.smoothed.nc'))
lon1 = -90
lon2 = 0
lat1 = 55
lat2 = 85
for path in paths1:
   ofile = f'{path[:-3]}.greenland_box.nc'
   cdo.sellonlatbox(f'{lon1},{lon2},{lat1},{lat2}',input = path, output = ofile)

paths1 = sorted(glob.glob(f'{datadir}divQ.WN4-5.????.??.smoothed.nc'))
for path in paths1:
   ofile = f'{path[:-3]}.greenland_box.nc'
   cdo.sellonlatbox(f'{lon1},{lon2},{lat1},{lat2}',input = path, output = ofile)


