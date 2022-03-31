#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)
datadir = '/mnt/data/greenland/decor/decordivD/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}reg.divD.WN0-3.decordivQ.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divD.WN4-5.decordivQ.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN0-3.addeddivD.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN4-5.addeddivD.SMB.1979-2018.10d_rm.nc']

d = [xr.open_dataset(fname) for fname in fnames]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=projm),
                        figsize = (20,10))
titles = ['divD WN0-3',
          'divD WN4-5',
          'divQ WN0-3',
          'divQ WN4-5']
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-0.1,0.1,nlevels)
i = 0
for dat,ax,title in zip(d,axs,titles):
    div = -dat['SMB_rec'].data[0,:,:]
        
    i+= 1

    #lat = dat['lat'].data
    #lon = dat['lon'].data
    #max_val = np.nanmax(np.abs(div))
    #print(max_val)
    #levels = np.linspace(-max_val,max_val,nlevels)


    m = ax.contourf(lon,
                lat,
                div,
                levels = levels,
                extend = 'both',
                cmap = 'seismic',
                transform = proj)
    ax.coastlines(resolution = '50m')
    #plt.colorbar(m,
    #             ax = ax,
    #             orientation = 'horizontal')
    ax.set_title(f'reg {title}')
    ax.set_aspect('auto', adjustable = None)


cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
ticks = np.linspace(-0.1,0.1,9)
plt.colorbar(m, 
             orientation = 'horizontal',
             label = r'mm w.e / W m$^{-2}$',
             cax = cax,
             ticks = ticks
             )
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/reg.syn.plan.SMB.decordivDdivQ.timmean.1979-2018.WN0-3.WN4-5.pdf')
fig.savefig('figures/reg.syn.plan.SMB.decordivDdivQ.timmean.1979-2018.WN0-3.WN4-5.png')
plt.show()
