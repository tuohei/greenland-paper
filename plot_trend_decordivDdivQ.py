#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()

datadir = '/mnt/data/greenland/decor/decordivD/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.decordivQWN0-3.decordivQWN4-5.anom.trend.nc',
           f'{datadir}divD.WN4-5.1979-2018.greenland_box.smoothed.decordivQWN0-3.decordivQWN4-5.anom.trend.nc',
           f'{datadir}divQ.WN0-3.1979-2018.greenland_box.smoothed.addeddivDWN0-3.addeddivDWN4-5.anom.trend.nc',
           f'{datadir}divQ.WN4-5.1979-2018.greenland_box.smoothed.addeddivDWN0-3.addeddivDWN4-5.anom.trend.nc']

d = [xr.open_dataset(fname) for fname in fnames]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=proj),
                        figsize = (20,10))
varnames = ['divD',
          'divD',
          'divQ',
          'divQ']
nlevels = 42
i = 0
titles = ['divD trend WN0-3',
            'divD trend WN4-5',
            'divQ trend WN0-3',
            'divQ trend WN4-5']
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-225,225,nlevels)

for dat,ax,title,varname in zip(d,axs,titles,varnames):
    div = -dat[varname].data[:,:]
    i +=1 
    lat = dat['lat'].data
    lon = dat['lon'].data
    max_val = np.nanmax(np.abs(div))
    print(max_val)
    if varname == 'divQ':
        levels = np.linspace(-20,20,nlevels)
        ticks = np.linspace(-20,20,9)
        #levels = np.linspace(-30,30,nlevels)
    else:
        levels = np.linspace(-40,40,nlevels)
        ticks = np.linspace(-40,40,9)
        #levels = np.linspace(-160,160,nlevels)



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
                 orientation = 'horizontal',
                 ticks = ticks)
    ax.set_title(f'{title}')
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
fig.savefig('figures/trends.decordivDdivQ.WN0-3.WN4-5.timmean.1979-2018.pdf')
fig.savefig('figures/trends.decordivDdivQ.WN0-3.WN4-5.timmean.1979-2018.png')
plt.show()
