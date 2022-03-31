#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)
datadir = '/mnt/data/greenland/decor/div_des2021/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}Ucorr.1979-2018.greenland_box.daily.trend.regrid.nc']
sm = f'{datadir}Ucorr.1979-2018.greenland_box.daily.trend.sign4000.neg.regrid.nc'
sm2 = f'{datadir}Ucorr.1979-2018.greenland_box.daily.trend.sign4000.pos.regrid.nc'

sm = xr.open_dataset(sm)
sm2 = xr.open_dataset(sm2)
d = [xr.open_dataset(fname) for fname in fnames]

div = 0
varname = 'U'
div = d[0][varname].data[:,:]
sm = sm[varname].data[:,:]
sm2 = sm2[varname].data[:,:]
sm[sm < .9] = 0
sm2[sm2 < .9] = 0
sm += sm2
print(div.shape)
fig, ax = plt.subplots(1,
                        1,
                        subplot_kw=dict(projection=projm),
                        figsize = (10,10))
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
max_val = np.nanmax(np.abs(div))
levels = np.linspace(-max_val,max_val,nlevels)
#lat = dat['lat'].data
#lon = dat['lon'].data
#print(max_val)
#levels = np.linspace(-max_val,max_val,nlevels)



title = 'Massflux trend'
m = ax.contourf(lon,
            lat,
            div,
            levels = levels,
            extend = 'both',
            cmap = 'seismic',
            transform = proj)
lines = ax.contour(lon,
            lat,
            sm,
            levels = [.90,.95],
            colors = ['white'],
            linestyles = ['solid','dashed','dotted'],

            transform = proj)
ax.contourf(lon,
            lat,
            div,
            levels = levels,
            extend = 'both',
            cmap = 'seismic',
            alpha = 0,
            transform = proj)
ax.clabel(
        lines,  # Typically best results when labelling line contours.
        colors=['white'],
        manual=False,  # Automatic placement vs manual placement.
        inline=True,  # Cut the line where the label will be placed.
        fmt=' {:.2f} '.format,  # Labes as integers, with some extra space.
    )
ax.coastlines(resolution = '50m')
#plt.colorbar(m,
#             ax = ax,
#             orientation = 'horizontal')
ax.set_title(title)
ax.set_aspect('auto', adjustable = None)

#cax = fig.add_axes([axs[0].get_position().x0, 
#                    axs[0].get_position().y0 - 0.04,
#                    axs[-1].get_position().x1 - axs[0].get_position().x0,
#                    0.02])
ticks = np.linspace(-max_val,max_val,9)
plt.colorbar(m, 
             orientation = 'horizontal',
             label = r'kg',
             ticks = ticks
             )
plt.tight_layout()
#plt.tight_layout(rect = (0,0.1,1,1))
#fig.savefig('figures/trend.massflux.timmean.1979-2018.eps')
#fig.savefig('figures/trend.massflux.timmean.1979-2018.png')
plt.show()
