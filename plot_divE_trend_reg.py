#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)
datadir = '/mnt/data/greenland/decor/divE/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}reg.divE.WN0-5.SMB.1979-2018.10d_rm.nc']
datadir3 = '/mnt/data/greenland/decor/trends/'
fnames2 = ['divE.WN0-5.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc']

d = [xr.open_dataset(fname) for fname in fnames]
d2 = [xr.open_dataset(f'{datadir3}{fname}') for fname in fnames2]

div = 0
varnames = ['divD']

for dat,dat2,varname in zip(d,d2,varnames):
    div += dat['SMB_rec'].data[0,:,:]*dat2[varname].data[:,:]
print(div.shape)
fig, axs = plt.subplots(1,
                        1,
                        subplot_kw=dict(projection=projm),
                        figsize = (5,10))
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
levels = np.linspace(-1,1,nlevels)
print(levels)

#lat = dat['lat'].data
#lon = dat['lon'].data
#max_val = np.nanmax(np.abs(div))
#print(max_val)
#levels = np.linspace(-max_val,max_val,nlevels)


m = axs.contourf(lon,
            lat,
            div,
            levels = levels,
            extend = 'both',
            cmap = 'seismic',
            transform = proj)
axs.coastlines(resolution = '50m')
#plt.colorbar(m,
#             ax = ax,
#             orientation = 'horizontal')
axs.set_title(f'SMB trend vE')
axs.set_aspect('auto', adjustable = None)


cax = fig.add_axes([axs.get_position().x0, 
                    axs.get_position().y0 - 0.04,
                    axs.get_position().x1 - axs.get_position().x0,
                    0.02])
ticks = np.linspace(-1,1,9)
plt.colorbar(m, 
             orientation = 'horizontal',
             label = r'mm w.e',
             cax = cax,
             ticks = ticks
             )
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/trend.total.SMB.timmean.1979-2018.divE.pdf')
fig.savefig('figures/trend.total.SMB.timmean.1979-2018.divE.png')
plt.show()
