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
fnames = [f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divD.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc']
fnames2 = [f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
           f'{datadir}divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
           f'{datadir}divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
           f'{datadir}divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
          ]

d = [xr.open_dataset(fname) for fname in fnames]
d2 = [xr.open_dataset(fname) for fname in fnames2]

cm = 1/2.54
fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=projm),
                        figsize = (1.8*(9+1)*cm,(9)*cm),
                        dpi = 300,
                       )
titles = ['(a)',
          '(b)',
          '(c)',
          '(d)']
varnames = ['divD',
            'divD',
            'divQ',
            'divQ']

grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
scale = 10
levels = scale*np.linspace(-1,1,nlevels)
i = 0
for dat,ax,title,dat2,varname in zip(d,axs,titles,d2,varnames):
    div = -dat['SMB_rec'].data[0,:,:]
    trend = -dat2[varname].data[:,:]
    div*=trend*scale
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
    ax.set_title(f'{title}')
    ax.set_aspect('auto', adjustable = None)


plt.tight_layout(rect = (0,0.1,1,1))
cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
ticks = scale*np.linspace(-1,1,11)
cb = plt.colorbar(m, 
             orientation = 'horizontal',
             #label = r'\small{$\times 10^{-1}$ mm w.e}',
             #fontsize = 'small',
             cax = cax,
             ticks = ticks
             )
cb.set_label(r'$\times 10^{-1}$ mm w.e', size = 'small')
cb.ax.tick_params(labelsize='x-small')
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/trend.syn.plan.toSMB.des2021.timmean.1979-2018.WN0-3.WN4-5.pdf')
fig.savefig('figures/trend.syn.plan.toSMB.des2021.timmean.1979-2018.WN0-3.WN4-5.png')
plt.show()
