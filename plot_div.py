#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()

datadir = '/mnt/data/greenland/decor/divQ/'

fnames = ['divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.timmean.nc',
          'divQ.WN0-3.WN4-5.cor_component.1979-2018.greenland_box.smoothed.timmean.nc',
          'divQ.WN4-5.WN0-3.cor_component.1979-2018.greenland_box.smoothed.timmean.nc',
          'divQ.WN0-3.1979-2018.greenland_box.smoothed.decorWN4-5.timmean.nc']

d = [xr.open_dataset(f'{datadir}{fname}') for fname in fnames]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=proj),
                        figsize = (20,10))
titles = ['WN4-5',
          'WN4-5 || WN0-3',
          'WN0-3 || WN4-5',
          'WN0-3']
nlevels = 41
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-225,225,nlevels)
for dat,ax,title in zip(d,axs,titles):
    div = -dat['divQ'].data[0,:,:]
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
    ax.set_title(f'divQ {title}')
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
fig.savefig('figures/divQ.WN0-3.WN4-5.timmean.1979-2018.pdf')
fig.savefig('figures/divQ.WN0-3.WN4-5.timmean.1979-2018.png')
plt.show()
