#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()

datadir = '/mnt/data/greenland/decor/divD/'
datadir2 = '/mnt/data/greenland/decor/divQ/'

fnames = [f'{datadir}divD.WN0.1979-2018.greenland_box.smoothed.decordivQ.timmean.nc',
          f'{datadir}divQ.divD.WN0.cor_component.1979-2018.greenland_box.smoothed.timmean.nc',
          f'{datadir2}divD.divQ.WN0.cor_component.1979-2018.greenland_box.smoothed.timmean.nc',
          f'{datadir2}divQ.WN0.1979-2018.greenland_box.smoothed.decordivD.timmean.nc']

d = [xr.open_dataset(fname) for fname in fnames]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=proj),
                        figsize = (20,10))
titles = ['divDWN0 - divD || divQ',
          'divD || divQ',
          'divQ || divD',
          'divQWN0 - divQ || divD']
nlevels = 41
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-750,750,nlevels)
i = 0
for dat,ax,title in zip(d,axs,titles):
    if i%2== 0:
        div = -dat['divD'].data[0,:,:]
    else:
        div = -dat['divQ'].data[0,:,:]
        
    i+= 1

    lat = dat['lat'].data
    lon = dat['lon'].data
    max_val = np.nanmax(np.abs(div))
    print(max_val)
    #levels = np.linspace(-max_val,max_val,nlevels)


    m = ax.contourf(lon,
                lat,
                div,
                levels = levels,
                extend = 'both',
                cmap = 'seismic')
    ax.coastlines(resolution = '50m')
    #plt.colorbar(m,
    #             ax = ax,
    #             orientation = 'horizontal')
    ax.set_title(f' {title}')
    ax.set_aspect('auto', adjustable = None)


cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
plt.colorbar(m, 
             orientation = 'horizontal',
             label = r'W m$^{-2}$',
             cax = cax,
             )
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/divQ.divD.timmean.1979-2018.WN0.pdf')
fig.savefig('figures/divQ.divD.timmean.1979-2018.WN0.png')
plt.show()
