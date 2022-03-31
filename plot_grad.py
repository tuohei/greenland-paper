#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()

datadir = '/mnt/data/greenland/grads_greenland/'

fnames = ['gradUD.WN0.1979-2018.greenland_box.timmean.smoothed.nc',
          'gradVD.WN0.1979-2018.greenland_box.timmean.smoothed.nc',
          'gradVQ.WN0.1979-2018.greenland_box.timmean.smoothed.nc',
          'gradUQ.WN0.1979-2018.greenland_box.timmean.smoothed.nc']

d = [xr.open_dataset(f'{datadir}{fname}') for fname in fnames]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=proj),
                        figsize = (20,10))
titles = ['uD',
          'vD',
          'vQ',
          'uQ']
nlevels = 41
i = 0
varnames = ['gradUE',
            'gradVE',
            'gradVQ',
            'gradUQ']
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-225,225,nlevels)
for dat,ax,title,varname in zip(d,axs,titles,varnames):
    div = -dat[varname].data[0,:,:]
    i +=1 
    lat = dat['lat'].data
    lon = dat['lon'].data
    max_val = np.nanmax(np.abs(div))
    print(max_val)
    levels = np.linspace(-max_val,max_val,nlevels)


    m = ax.contourf(lon,
                lat,
                div,
                levels = levels,
                extend = 'both',
                cmap = 'seismic')
    ax.coastlines(resolution = '50m')
    plt.colorbar(m,
                 ax = ax,
                 label = r'W m$^{-2}$',
                 orientation = 'horizontal')
    ax.set_title(f'grad{title}')
    ax.set_aspect('auto', adjustable = None)


#cax = fig.add_axes([axs[0].get_position().x0, 
#                    axs[0].get_position().y0 - 0.04,
#                    axs[-1].get_position().x1 - axs[0].get_position().x0,
#                    0.02])
#plt.colorbar(m, 
#             orientation = 'horizontal',
#             label = r'W m$^{-2}$',
#             cax = cax,
#             )
plt.tight_layout()
fig.savefig('figures/gradsWN0.timmean.1979-2018.pdf')
fig.savefig('figures/gradsWN0.timmean.1979-2018.png')
plt.show()
