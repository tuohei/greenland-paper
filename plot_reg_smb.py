#!/usr/bin/env python
import numpy as np
import xarray as xr
from math import pi
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import sys
import glob
from mpl_toolkits.axes_grid1 import make_axes_locatable
#import matplotlib
#matplotlib.rcParams['text.usetex'] = True
var = 'D'
datadir = f'/mnt/data/greenland/decor/divD/'

gpath = '/mnt/data/greenland/decor/divD/Icemask_Topo_Iceclasses\
_lon_lat_average_1km.nc'
grid = xr.open_dataset(gpath)
lat = grid['LAT']
lon = grid['LON']
topo = grid['Topography']
#paths = glob.glob(f'{datadir}reg.{var}.n1-3.SMB.1979-2017*.nc')
#paths = glob.glob(f'{datadir}cor_syn_SMB.1979-2017.nc')
#path = f'{datadir}reg.Q.n4-5.SMB.1979-2017.nc'
path = f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc'
path2 = f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.smoothed.nc'
path3 = f'{datadir}reg.divD.WN4-5.SMB.1979-2018.10d_rm.nc'

c = xr.open_dataset(path)
c2 = xr.open_dataset(path2)
c3 = xr.open_dataset(path3)
# print(c)
sec_to_days = 1/86400
cor = -c[f'SMB_rec'].data[0,:,:]#*sec_to_days
cor2 = -c2[f'SMB_rec'].data[0,:,:]#*sec_to_days
cor3 = -c3[f'SMB_rec'].data[0,:,:]#*sec_to_days
print(cor3.shape)
#cor = c['divD'].data[0,:,:]
# print(cor.shape)

fig = plt.figure(figsize = [13,7])
#fig = plt.figure()
proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude=70, central_longitude= -40)
ax = fig.add_subplot(1,3,1,projection = projm)
ax2 = fig.add_subplot(1,3,2,projection = projm)
ax3 = fig.add_subplot(1,3,3,projection = projm)
#ax.set_extent((-70,-10,90,50),crs = proj)
#ax.set_title(fname)
#ax.set_title(r'SMB regressed on synoptic $\nabla \cdot vQ$')
#ax.set_title(r'SMB regressed on $\nabla \cdot vQ_s$')
#ax2.set_title(r'SMB regressed on $\nabla \cdot vQ_s$')

ax.set_title('(a)')
ax2.set_title('(b)')
ax3.set_title('(c)')
#levels = np.linspace(-np.nanmax(np.abs(cor)),np.nanmax(np.abs(cor)),51)
#scaling = 1/100000
scaling = 1
#levels = np.linspace(-np.nanmax(np.abs(cor3)),np.nanmax(np.abs(cor3)),51)/scaling
levels = np.linspace(-0.1,0.1,51)
#levels = np.linspace(-0.09,0.09,41)
#elevel = np.concatenate([np.linspace(0,1400,3),np.linspace(1500,3000,10)])
elevel = np.linspace(1700,3000,13)
cf = ax.contourf(lon,lat,cor3/scaling,levels = levels,cmap = 'seismic',extend = 'both',transform=proj)
cf2 = ax2.contourf(lon,lat,cor2/scaling,levels = levels,cmap = 'seismic',extend = 'both',transform=proj)
cf3 = ax3.contourf(lon,lat,cor/scaling,levels = levels,cmap = 'seismic',extend = 'both',transform=proj)
#divider = make_axes_locatable(ax)
cax = fig.add_axes([ax.get_position().x0,ax.get_position().y0 - 0.04,
    ax3.get_position().x1 - ax.get_position().x0, 0.02])
print(ax2.get_position())
print(ax.get_position())
print(cax.get_position())
label_string =  f"{scaling:.0E}" + r'$ \times \frac{\mathrm{W/m}^2}{\mathrm{W/m}^2 \,\mathrm{day}}$'
#cax = divider.append_axes('right',size = '5%',pad = 0.05)
plt.colorbar(cf,orientation = 'horizontal',extend = 'both',
        label =label_string,
        format = '%.1f',
        cax = cax)
#plt.colorbar(cf,orientation = 'horizontal',label = r'$\frac{\mathrm{mm\ w.e.}}{\mathrm{W/m}^2}$', cax = cax)
#plt.colorbar(cf,orientation = 'horizontal',label = r'$\frac{\mathrm{mm}}{\mathrm{W/m}^2}$', cax = cax)
#        fraction=0.046*8/12, pad=0.04)

ax.coastlines(resolution = '50m')
ax2.coastlines(resolution = '50m')
ax3.coastlines(resolution = '50m')
#ax.contour(lon,lat,mask,colors = ['g'],alpha= .1,transform=proj)
#elev = ax.contour(lon,lat,topo,transform = proj,levels=elevel, colors = ['black'],alpha = .2)
#ax.clabel(elev,colors = ['black'],manual = False, inline = True, fmt = ' {:.2f}m '.format)
fig.savefig(f'figures/convQ_syn_plan_SMB_rmean_10days_decor.pdf')
fig.savefig(f'figures/convQ_syn_plan_SMB_rmean_10days_decor.eps')
fig.savefig(f'figures/convQ_syn_plan_SMB_rmean_10days_decor.png')
plt.show()
