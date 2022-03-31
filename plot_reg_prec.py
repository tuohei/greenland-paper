#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)

datadir = '/mnt/data/greenland/radiation/'

#fnames = ['divQ.WN1-3.1979-2018.greenland_box.smoothed.decorWN4-5.decorWN0.trend.nc',
#          'divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN1-3.decorWN0.trend.nc',
#          'divD.WN1-3.1979-2018.greenland_box.smoothed.decorWN4-5.decorWN0.trend.nc',
#          'divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN1-3.decorWN0.trend.nc']
#fnames = ['reg.LWS.SMB.1979-2018.10d_rm.nc',
#          'reg.SWS.SMB.1979-2018.10d_rm.nc',
#          'reg.SLH.SMB.1979-2018.10d_rm.nc',
#          'reg.SSH.SMB.1979-2018.10d_rm.nc',
#          'reg.TP.SMB.1979-2018.10d_rm.nc']

fnames = ['reg.LWS_decor_TP.SMB.1979-2018.10d_rm.nc',
          'reg.SWS.SMB.1979-2018.10d_rm.nc',
          'reg.SLH.SMB.1979-2018.10d_rm.nc',
          'reg.SSH.SMB.1979-2018.10d_rm.nc',
          'reg.TP.SMB.1979-2018.10d_rm.nc']
d = [xr.open_dataset(f'{datadir}{fname}') for fname in fnames]

datadir = '/mnt/data/greenland/decor/divE/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data

fig, axs = plt.subplots(1,
                        5,
                        subplot_kw=dict(projection=projm),
                        figsize = (20,10))
varnames = 5*['SMB_rec']
#varnames = ['LWS',
#          'SWS',
#          'SLH',
#          'SSH',
#          'TP']
nlevels = 42
i = 0
titles = ['LWS reg coeff',
            'SWS reg coeff',
            'SLH reg coeff',
            'SSH reg coeff',
            'TP reg coeff']
#levels = np.linspace(-1300,1300,nlevels)
max_val = 1
levels = np.linspace(-max_val,max_val,nlevels)

for dat,ax,title,varname in zip(d,axs,titles,varnames):
    div = dat[varname].data[0,:,:]
    i +=1 
    #lat = dat['lat'].data
    #lon = dat['lon'].data
    max_val = np.nanmax(np.abs(div))
    print(max_val)
    levels = np.linspace(-max_val,max_val,nlevels)


    m = ax.contourf(lon,
                lat,
                div,
                levels = levels,
                extend = 'both',
                transform = proj,
                cmap = 'seismic')
    ax.coastlines(resolution = '50m')
    ticks = np.linspace(-max_val,max_val,9)
    plt.colorbar(m,
                 ax = ax,
                 label = r'W m$^{-2}$',
                 orientation = 'horizontal',
                 ticks = ticks,)
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
fig.savefig('figures/regs.rad_prec_reg.1979-2018.pdf')
fig.savefig('figures/regs.rad_prec_reg.1979-2018.png')
plt.show()
