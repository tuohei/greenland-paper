#!/usr/bin/env python
import xarray as xr
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt

proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)
datadir = '/mnt/data/greenland/decor/divD/'
datadir2 = '/mnt/data/greenland/decor/divQ/'
datadir3 = '/mnt/data/greenland/decor/divE/'
datadir4 = '/mnt/data/greenland/decor/trends/'
datadir5 = '/mnt/data/greenland/decor/div_des2021/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}reg.divD.WN0-5.SMB.1979-2018.10d_rm.nc',
          f'{datadir2}reg.divQ.WN0-5.SMB.1979-2018.10d_rm.nc']
#          f'{datadir2}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
#          f'{datadir2}reg.divQ.WN4-5.SMB.1979-2018.10d_rm.nc']
fnames2 = [f'{datadir}divD.WN0-5.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
           f'{datadir2}divQ.WN0-5.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc']
#           'divQ.WN0-3.1979-2018.greenland_box.smoothed.addedWN4-5.trend.regrid.nc',
#           'divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.trend.regrid.nc']

fnames_E = [f'{datadir3}reg.divE.WN0-5.SMB.1979-2018.10d_rm.nc']
fnames_E_t = [f'{datadir4}divE.WN0-5.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc']

dE = xr.open_dataset(fnames_E[0])
dE2 = xr.open_dataset(fnames_E_t[0])
div1 = dE['SMB_rec'].data[0,:,:]*dE2['divD'].data[:,:]

fnames_sp = [f'{datadir5}reg.divD.WN0-3.SMB.1979-2018.10d_rm.nc',
             f'{datadir5}reg.divD.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc',
             f'{datadir5}reg.divQ.WN0-3.SMB.1979-2018.10d_rm.nc',
             f'{datadir5}reg.divQ.WN4-5.decorWN0-3.SMB.1979-2018.10d_rm.nc',
            ]

fnames_sp_t = [f'{datadir5}divD.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
               f'{datadir5}divD.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
               f'{datadir5}divQ.WN0-3.1979-2018.greenland_box.smoothed.anom.trend.regrid.nc',
               f'{datadir5}divQ.WN4-5.1979-2018.greenland_box.smoothed.decorWN0-3.anom.trend.regrid.nc',
              ]

d = [xr.open_dataset(fname) for fname in fnames]
d2 = [xr.open_dataset(fname) for fname in fnames2]

fig, axs = plt.subplots(1,
                        4,
                        subplot_kw=dict(projection=projm),
                        figsize = (16,9))
titles = ['(a)',
          '(b)',
          '(c)',
          '(d)']
#          'divQ WN0-3',
#          'divQ WN4-5']
varnames = ['divD',
            'divQ']
#            'divQ',
#            'divQ']
div2 = 0
for dat,dat2,varname in zip(d,d2,varnames):
    div2 += dat['SMB_rec'].data[0,:,:]*dat2[varname].data[:,:]

d = [xr.open_dataset(fname) for fname in fnames_sp]
d2 = [xr.open_dataset(fname) for fname in fnames_sp_t]
varnames = ['divD',
            'divD',
            'divQ',
            'divQ']
div3 = 0
for dat,dat2,varname in zip(d,d2,varnames):
    div3 += dat['SMB_rec'].data[0,:,:]*dat2[varname].data[:,:]


grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data
nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
l_lim = 1.5
levels = np.linspace(-l_lim,l_lim,nlevels)
i = 0
datadir3 = '/mnt/data/greenland/decor/trends/'
smb = xr.open_dataset(f'{datadir3}smb.anom.diffperiods.nc')['SMB_rec']
smb = smb[0,:,:]
#lat = dat['lat'].data
#lon = dat['lon'].data
#max_val = np.nanmax(np.abs(div))
#print(max_val)
#levels = np.linspace(-max_val,max_val,nlevels)



data_plt = [div1,div2,div3,smb]
#titles = ['SMB trend vE', 'SMB trend']
for dt,ax,title in zip(data_plt,axs,titles):
    m = ax.contourf(lon,
                lat,
                dt,
                levels = levels,
                extend = 'both',
                cmap = 'seismic',
                transform = proj)
    ax.coastlines(resolution = '50m')
    #plt.colorbar(m,
    #             ax = ax,
    #             orientation = 'horizontal')
    ax.set_title(title)
    ax.set_aspect('auto', adjustable = None)


cax = fig.add_axes([axs[0].get_position().x0, 
                    axs[0].get_position().y0 - 0.04,
                    axs[-1].get_position().x1 - axs[0].get_position().x0,
                    0.02])
ticks = np.linspace(-l_lim,l_lim,9)
plt.colorbar(m, 
             orientation = 'horizontal',
             label = r'mm w.e',
             cax = cax,
             ticks = ticks
             )
plt.tight_layout(rect = (0,0.1,1,1))
fig.savefig('figures/all_trends.syn.plan.SMB.with_SMB.timmean.des2021.1979-2018.WN0-5.pdf')
fig.savefig('figures/all_trends.syn.plan.SMB.with_SMB.timmean.des2021.1979-2018.WN0-5.png')
plt.show()
