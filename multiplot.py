#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import numpy as np
import seaborn as sns
import pandas as pd
from scipy.stats import linregress
import cartopy.crs as ccrs
import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter
sns.set_theme(style="ticks")
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
#mpl.rcParams['lines.linewidth'] = 3
proj = ccrs.PlateCarree()
projm = ccrs.Stereographic(central_latitude = 70,
                           central_longitude = -40)

# Fig layout
x = [['M','L','L','L'],
     ['A','B','C','D'],
    ]
cm = 1/2.54
fig, axes = plt.subplot_mosaic(x,
                               figsize = (25*cm,20*cm),
                               dpi = 300,
                               constrained_layout=True)
# Lineplots
dirpath = '/mnt/data/greenland/decor/summed/'
dirpath2='/mnt/data/greenland/decor/div_feb2022/'
d = xr.open_dataset(f'{dirpath2}south_west_divD_divQ_WN0-5.to_smb.summed.nc')
d5 = xr.open_dataset(f'{dirpath}south_west_divD_divQ_WN0-3_WN4-5.to_smb.summed.nc')
d2 = xr.open_dataset(f'{dirpath}south_west_SMB_Icemask.summed.nc')
d3 = xr.open_dataset(f'{dirpath}south_west_divQ_divD_WN0-5.to_smb.summed.nc')
d4 = xr.open_dataset(f'{dirpath}south_west_divE.WN0-5.1979-2018.anom.to_smb.summed.nc')
dirpath_m = '/mnt/data/greenland/massflux/'
dm = xr.open_dataset(f'{dirpath_m}south_west.Ucorr.1979-2018.daily.anom.summed.nc')


years = 8
ndays_rolling = 365*years
d = d.sel(time = d.time.dt.year <2018)
dm = dm.sel(time = dm.time.dt.year <2018)
d3 = d3.sel(time = d3.time.dt.year < 2018)
d4 = d4.sel(time = d4.time.dt.year < 2018)
d5 = d5.sel(time = d5.time.dt.year < 2018)


d_rolled = d.divQ.rolling(time = ndays_rolling).mean()
d2_rolled = d2.SMB_rec.rolling(time = ndays_rolling).mean()
d3_rolled = d3.divD.rolling(time = ndays_rolling).mean()
d4_rolled = d4.divD.rolling(time = ndays_rolling).mean()
d5_rolled = d5.divQ.rolling(time = ndays_rolling).mean()
smbmax = np.nanmax(np.abs(d2_rolled.data))
smbscaling = 1e5


dm_rolled = dm.UM.rolling(time = ndays_rolling).mean()
um_max = np.nanmax(np.abs(dm_rolled.data))
um_scaling = 1e9
time = d_rolled.time.data[ndays_rolling:]
p1, = axes['L'].plot(time,d5_rolled[ndays_rolling:,0,0]/smbscaling,color = 'red',
                     label =r'$vE_a$')
p2, = axes['L'].plot(time,d2_rolled[ndays_rolling:,0,0]/smbscaling,color = 'black',
                     label = 'smb')
p3, = axes['L'].plot(time,d3_rolled[ndays_rolling:,0,0]/smbscaling,color = 'blue',
                     label = r'$vE_b$')
p4, = axes['L'].plot(time,d4_rolled[ndays_rolling:,0,0]/smbscaling,color = 'gray',
                     label = r'$vE_c$')
p5, = axes['L'].plot(time,d_rolled[ndays_rolling:,0,0]/smbscaling,
                     color = 'red', linestyle = 'dotted', linewidth = 1,
                     )
ax2 = axes['L'].twinx()
axes['L'].set_title('(b)')
print(smbmax)
smbmax = np.round(smbmax/smbscaling,1)

axes['L'].set_ylim(-smbmax,smbmax)
axes['L'].set_yticks([-smbmax,0,smbmax])
axes['L'].set_ylabel(r'$\times 10^5$ mm w.e.')
ax2.set_ylabel(r'$\times 10^9$ kg m s$^{-1}$')
p5, = ax2.plot(time,dm_rolled[ndays_rolling:,0,0]/um_scaling,color = 'orange',
               label = 'UM')
ax2.legend(handles = [p1,p3,p4,p2,p5], fontsize = 'xx-small',loc = 'lower left')
print(um_max)
um_max = np.round(um_max/um_scaling,1)
ax2.set_ylim(-um_max,um_max)
ax2.set_yticks([-um_max,0,um_max])
#ax2.xaxis.set_major_locator(plt.MaxNLocator(6))
#ax2.set_xticks(time[::2*365])
# Greenland

axes['M'] = plt.subplot(2,4,1,projection = projm)
axes['A'] = plt.subplot(2,4,5,projection = projm)

axes['B'] = plt.subplot(2,4,6,projection = projm)
axes['C'] = plt.subplot(2,4,7,projection = projm)
axes['D'] = plt.subplot(2,4,8,projection = projm)



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


titles = ['(c)',
          '(d)',
          '(e)',
          '(f)']
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



data_plt = [smb,div3,div2,div1]
axnames = ['A','B','C','D']


for dt,ax,title in zip(data_plt,axnames,titles):
    m = axes[ax].contourf(lon,
                lat,
                dt,
                levels = levels,
                extend = 'both',
                cmap = 'seismic',
                transform = proj)
    axes[ax].coastlines(resolution = '50m')
    #plt.colorbar(m,
    #             ax = ax,
    #             orientation = 'horizontal')
    axes[ax].set_title(title)
    #axes[ax].set_aspect(.7, adjustable = 'box')
    #axes[ax].set_aspect('auto', adjustable = 'box')
#plt.tight_layout(rect = (0,0.1,1,1)) 
#cax = fig.add_axes([axes['A'].get_position().x0,
#                    axes['A'].get_position().y0 - 0.04,
#                    axes['D'].get_position().x1 - axes['A'].get_position().x0,
#                    0.02])
ticks = np.linspace(-l_lim,l_lim,7)
plt.colorbar(m,
             orientation = 'vertical',
             label = r'mm w.e',
             ax = axes['A'],
             shrink = .7,
             ticks = ticks,
             location = 'left'
             )

#plt.tight_layout(rect = (0,0.1,1,1)) 



datadir = '/mnt/data/greenland/decor/div_des2021/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
fnames = [f'{datadir}Ucorr.1979-2018.greenland_box.daily.trend.regrid.nc']
sm = f'{datadir}Ucorr.1979-2018.greenland_box.daily.trend.sign4000.neg.regrid.nc'
d = [xr.open_dataset(fname) for fname in fnames]
sm = xr.open_dataset(sm)
div = 0
varname = 'U'
UM = d[0][varname].data[:,:]
sm = sm[varname].data[:,:]

nlevels = 42
#levels = np.linspace(-1300,1300,nlevels)
scaling = 10000

UM /= scaling
max_val = np.nanmax(np.abs(UM))
levels = np.linspace(-max_val,max_val,nlevels)
#lat = dat['lat'].data
#lon = dat['lon'].data
#print(max_val)
#levels = np.linspace(-max_val,max_val,nlevels)



title = 'Massflux trend'
m = axes['M'].contourf(lon,
            lat,
            UM,
            levels = levels,
            extend = 'both',
            cmap = 'seismic',
            transform = proj)
#axes['M'].contour(lon,
#            lat,
#            sm,
#            levels = [0,.90,.95],
#            colors = ['white'],
#            linestyles = ['solid','dashed','dotted'],
#
#            transform = proj)

lines = axes['M'].contour(lon,
                          lat,
                          sm,
                          levels = [.90,.95],
                          colors = ['white'],
                          linestyles = ['solid','dashed','dotted'],
                          transform = proj)
axes['M'].contourf(lon,
                   lat,
                   UM,
                   levels = levels,
                   extend = 'both',
                   cmap = 'seismic',
                   alpha = 0,
                   transform = proj)
axes['M'].clabel(
                 lines,  # Typically best results when labelling line contours.
                 colors=['white'],
                 manual=False,  # Automatic placement vs manual placement.
                 inline=True,  # Cut the line where the label will be placed.
                 fontsize = 'x-small',
                 fmt=' {:.2f} '.format,  # Labes as integers, with some extra space.
                )
axes['M'].coastlines(resolution = '50m')
#plt.colorbar(m,
#             ax = ax,
#             orientation = 'horizontal')
axes['M'].set_title('(a)')
axes['M'].set_aspect('auto', adjustable = None)

#cax = fig.add_axes([axs[0].get_position().x0, 
#                    axs[0].get_position().y0 - 0.04,
#                    axs[-1].get_position().x1 - axs[0].get_position().x0,
#                    0.02])
ticks = np.linspace(-1,1,5)
plt.colorbar(m, 
             orientation = 'vertical',
             label = r'$\times 10^5$kg m s$^{-1}$',
             ticks = ticks,
             ax = axes['M'],
             location = 'left',
             )


fig.savefig('figures/5panelplot_2nd.png')
fig.savefig('figures/5panelplot_2nd.pdf')

plt.show()
