#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)
#datadir = '/mnt/data/greenland/decor/divD/'
#datadir2 = '/mnt/data/greenland/decor/divQ/'
#gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
#fnames = [f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir}reg.divD.WN4-5.SMB.1979-2018.10d_rm.nc',
#          f'{datadir2}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir2}reg.divQ.WN4-5.SMB.1979-2018.10d_rm.nc']

datadir = '/mnt/data/greenland/decor/div_des2021/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divD.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
          f'{datadir}reg.divQ.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc']

d = [xr.open_dataset(fname) for fname in fnames]

cm = 1/2.54
fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=projm),
                        figsize = (1.8*(9+1)*cm,9*cm),
                        constrained_layout = False,
                        dpi = 300,
                       )
#fig.set_constrained_layout_pads(w_pad=4 / 72, h_pad=36 / 72, hspace=0.2,
#                                wspace=0.2)
titles = ['(a)',
          '(b)',
          '(c)',
          '(d)']
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
scale = 100
lmaxQ = scale*0.1
lmaxD = scale*0.05
levelsQ = np.linspace(-lmaxQ,lmaxQ,nlevels)
levelsD = np.linspace(-lmaxD,lmaxD,nlevels)
i = 0
for dat,ax,title in zip(d,axs,titles):
    div = -scale*dat['SMB_rec'].data[0,:,:]
    print(div.shape)
        
    if i < 2:
        levels = levelsD
        mD = ax.contourf(lon,
                    lat,
                    div,
                    levels = levels,
                    extend = 'both',
                    cmap = 'seismic',
                    transform = proj)
    else:
        levels = levelsQ
        mQ = ax.contourf(lon,
                    lat,
                    div,
                    levels = levels,
                    extend = 'both',
                    cmap = 'seismic',
                    transform = proj)
    i += 1
    #lat = dat['lat'].data
    #lon = dat['lon'].data
    #max_val = np.nanmax(np.abs(div))
    #print(max_val)
    #levels = np.linspace(-max_val,max_val,nlevels)


    ax.coastlines(resolution = '50m')
    #plt.colorbar(m,
    #             ax = ax,
    #             orientation = 'horizontal')
    ax.set_title(f'{title}')
    ax.set_aspect('auto', adjustable = None)


plt.tight_layout(rect = (0,0.1,1,1))
cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
#cax.set_in_layout(True)
cax2 = fig.add_axes([axs[2].get_position().x0, 
                    axs[2].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[2].get_position().x0,
                    0.02])
plt.tight_layout(rect = (0,0.1,1,1))
#cax2.set_in_layout(True)
ticksD = np.round(np.linspace(-lmaxD,lmaxD,11))
ticksQ = np.round(np.linspace(-lmaxQ,lmaxQ,11))
cb1 = plt.colorbar(mD, 
             orientation = 'horizontal',
             #label = r'$\times 10^{-2}$ mm w.e / W m$^{-2}$',
             cax = cax,
             ticks = ticksD
             )

cb1.set_label(r'$\times 10^{-2}$ mm w.e / W m$^{-2}$', size = 'small')
cb1.ax.tick_params(labelsize='x-small')
cb2 = plt.colorbar(mQ, 
             orientation = 'horizontal',
             #label = r'$\times 10^{-2}$ mm w.e / W m$^{-2}$',
             cax = cax2,
             ticks = ticksQ
             )
cb2.set_label(r'$\times 10^{-2}$ mm w.e / W m$^{-2}$', size = 'small')
cb2.ax.tick_params(labelsize='x-small')
fig.savefig('figures/reg.syn.plan.SMB.des2021.1979-2018.WN0-3.WN4-5.pdf')
fig.savefig('figures/reg.syn.plan.SMB.des2021.1979-2018.WN0-3.WN4-5.png')
plt.show()
