import numpy as np
import xarray as xr
from math import pi
import pandas as pd
import sys

R = 6371e3

years = np.arange(1995,2017 + 1,1)
months = ['01','02','03','04','05','06','07','08','09','10','11','12']
dirpath = '/cluster/work/users/the038/Edivdat/'
for year in years:
    for month in months:
        vqname = f'vEtotLL.{year}.{month}.WN6.nc'
        uqname = f'uEtotLL.{year}.{month}.WN6.nc'
        fv = xr.open_dataset(dirpath + vqname)
        fu = xr.open_dataset(dirpath + uqname)
        lats = fv['lat'].data
        lons = fv['lon'].data
        vE = fv['vEtotLL'].data
        uE = fu['uEtotLL'].data
        times = pd.date_range(start = f'{month}/1/{year}',freq = '6H',periods=vE.shape[1])
        conx = np.zeros(vE.shape)
        cony = np.zeros(vE.shape)

        #Cosine of latitude
        clat = np.cos(np.deg2rad(lats))
        #Cosine of latitude multiplied by meridional transport
        vE = (vE.transpose(0,1,3,2)*clat).transpose(0,1,3,2)
        # Delta latitude
        dlat2 = 2*(lats[0]-lats[1])*pi/180

        # Computing convergence in y-direction
        # The value of each grid cell is based on the values in the adjacent cells.
        cony[:,:,1:-1,:] = (vE[:,:,:-2,:]-vE[:,:,2:,:])/dlat2
        # Computing convergence in x-direction
        conx[:,:,:,1:-1] = (uE[:,:,:,2:]-uE[:,:,:,:-2])/dlat2
        # Adding values for endpoints
        conx[:,:,:,0] = (uE[:,:,:,1] - uE[:,:,:,-1])/dlat2
        conx[:,:,:,-1] = (uE[:,:,:,0] - uE[:,:,:,-2])/dlat2
        # Computing the divergene
        divW = ((conx + cony).transpose(0,1,3,2)/(R*clat)).transpose(0,1,3,2)
        #  Averaging the divergence and summing over wavenumbers
        # mdivW = np.mean(divW,axis = 1).sum(axis=0)
        div = xr.DataArray(divW,dims = ['n','time','lat','lon'],\
                           coords = [range(6),times,lats,lons])
        div = div.resample(time = '1D').mean('time')
        div.name = 'divE'
        div.to_netcdf(f'{dirpath}/divergence/divE.WN6.{year}.{month}.nc')

        print(f'{year} {month} complete.')
