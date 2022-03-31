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
#fnames = [f'{datadir}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir}reg.divD.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir}reg.divQ.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc']
fnames2 = [f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
           f'{datadir}divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
           f'{datadir}divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
           f'{datadir}divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
          ]
fnames = [f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.sign2000.pos.regrid.nc',
          f'{datadir}divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.sign2000.pos.regrid.nc',
          f'{datadir}divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.sign2000.pos.regrid.nc',
          f'{datadir}divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.sign2000.pos.regrid.nc',
         ]

fnames3 =[f'{datadir}divD.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.sign2000.neg.regrid.nc',
          f'{datadir}divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.sign2000.neg.regrid.nc',
          f'{datadir}divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.sign2000.neg.regrid.nc',
          f'{datadir}divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.sign2000.neg.regrid.nc',
         ]
d = [xr.open_dataset(fname) for fname in fnames]
d2 = [xr.open_dataset(fname) for fname in fnames2]
d3 = [xr.open_dataset(fname) for fname in fnames3]

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
lmaxD = 80
lmaxQ = 20
levelsD = np.linspace(-lmaxD,lmaxD,nlevels)
levelsQ = np.linspace(-lmaxQ,lmaxQ,nlevels)
i = 0
signcolor = 'magenta'
for ax,title,dat2,varname in zip(axs,titles,d2,varnames):
    div = -dat2[varname].data[:,:]

    #lat = dat['lat'].data
    #lon = dat['lon'].data
    #max_val = np.nanmax(np.abs(div))
    #print(max_val)
    #levels = np.linspace(-max_val,max_val,nlevels)

    if i < 2:
        levels = levelsD
        sm = d[i][varname].data[:,:] 
        sm2 = d3[i][varname].data[:,:]
        sm[sm<.9] = 0
        sm2[sm2<.9] = 0
        sm+=sm2
        print(sm)
        if i == 0:
            levels_s = [.90]
        else:
            levels_s = [.90]
        mD = ax.contourf(lon,
                    lat,
                    div,
                    levels = levels,
                    extend = 'both',
                    cmap = 'seismic',
                    transform = proj)
        lines = ax.contour(lon,
                           lat,
                           sm,
                           levels = levels_s,
                           colors = [signcolor],

                           linestyles = ['dashed','dashed'],
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
                  colors=[signcolor],
                  manual=False,  # Automatic placement vs manual placement.
                  inline=True,  # Cut the line where the label will be placed.
                  fontsize = 'xx-small',
                  fmt=' {:.2f} '.format,  # Labes as integers, with some extra space.
                 )
    else:
        levels = levelsQ
        mQ = ax.contourf(lon,
                    lat,
                    div,
                    levels = levels,
                    extend = 'both',
                    cmap = 'seismic',
                    transform = proj)
        sm = d[i][varname].data[:,:] 
        sm2 = d3[i][varname].data[:,:]
        sm[sm<.9] = 0
        sm2[sm2<.9] = 0
        sm+=sm2
        if i == 2:
            levels_s = [.90]
        else:
            levels_s = [.90]
        lines = ax.contour(lon,
                           lat,
                           sm,
                           levels = levels_s,
                           colors = [signcolor],

                           linestyles = ['dashed','dashed'],
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
                  colors=[signcolor],
                  manual=False,  # Automatic placement vs manual placement.
                  inline=True,  # Cut the line where the label will be placed.
                  fontsize = 'xx-small',
                  fmt=' {:.2f} '.format,  # Labes as integers, with some extra space.
                 )
    i += 1

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
#cax = fig.add_axes([axs[0].get_position().x0, 
#                    axs[0].get_position().y0 - 0.04,
#                    axs[-1].get_position().x1 - axs[0].get_position().x0,
#                    0.02])
#ticks = np.linspace(-60,60,9)
#plt.colorbar(m, 
#             orientation = 'horizontal',
#             label = r'mm w.e',
#             cax = cax,
#             ticks = ticks
#             )
cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
cax2 = fig.add_axes([axs[2].get_position().x0, 
                    axs[2].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[2].get_position().x0,
                    0.02])
ticksD = np.round(np.linspace(-lmaxD,lmaxD,9))
ticksQ = np.round(np.linspace(-lmaxQ,lmaxQ,9))
cb1 = plt.colorbar(mD, 
             orientation = 'horizontal',
             #label = r'W m$^{-2}$',
             cax = cax,
             ticks = ticksD
             )
cb1.set_label(r'W m$^{-2}$', size = 'small')
cb1.ax.tick_params(labelsize='x-small')
cb2 = plt.colorbar(mQ, 
             orientation = 'horizontal',
             #label = r'W m$^{-2}$',
             cax = cax2,
             ticks = ticksQ
             )
cb2.set_label(r'W m$^{-2}$', size = 'small')
cb2.ax.tick_params(labelsize='x-small')
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/trend.syn.plan.SMB.des2021.timmean.1979-2018.WN0-3.WN4-5.pdf')
fig.savefig('figures/trend.syn.plan.SMB.des2021.timmean.1979-2018.WN0-3.WN4-5.png')
plt.show()
