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
#fnames = ['reg.SSH.SMB.1979-1985.10d_rm.nc',
#          'reg.SSH.SMB.2012-2018.10d_rm.nc',
#          'reg.SLH.SMB.1979-1985.10d_rm.nc',
#          'reg.SLH.SMB.2012-2018.10d_rm.nc']

fnames = ['reg.totrad.SMB.1979-2018.10d_rm.nc',
          'reg.totrad.decorTP.SMB.1979-2018.10d_rm.nc',
          'reg.TP.SMB.1979-2018.10d_rm.nc',
         ]
d = [xr.open_dataset(f'{datadir}{fname}') for fname in fnames]

datadir = '/mnt/data/greenland/decor/divE/'
gpath = f'{datadir}Icemask_Topo_Iceclasses_lon_lat_average_1km.nc' 
grid = xr.open_dataset(gpath)
lat = grid['LAT'].data
lon = grid['LON'].data

cm = 1/2.54
fig, axs = plt.subplots(1,
                        len(fnames),
                        subplot_kw=dict(projection=projm),
                        figsize = (18*cm,11*cm),
                        constrained_layout = True,
                        dpi = 300)
varnames = len(fnames)*['SMB_rec']
#varnames = ['LWS',
#axs = [axs]
#          'SWS',
#          'SLH',
#          'SSH',
#          'TP']
nlevels = 42
i = 0
#titles = ['SSH 1st period',
#            'SSH 2nd period',
#            'SLH 1st period',
#            'SLH 2nd period']
titles = ['(a)',
          '(b)',
          '(c)',
         ]
#levels = np.linspace(-1300,1300,nlevels)
max_val = 1
levels = np.linspace(-max_val,max_val,nlevels)
scaling = [100,100,1/1000]
labels = [r'$\times 10^{-2}$ mm w.e. / W m$^{-2}$',
          r'$\times 10^{-2}$ mm w.e. / W m$^{-2}$',
          r'$\times 10^{3}$ mm w.e. / m',
         ]



for dat,ax,title,varname,scale,label in zip(d,axs,titles,varnames,scaling,labels):
    ax.set_aspect('auto', adjustable = None)
    if title == '(a)' or title == '(b)': 
        div = scale*86400*dat[varname].data[0,:,:]
    else:
        div = scale*dat[varname].data[0,:,:]
    i +=1 
    #lat = dat['lat'].data
    #lon = dat['lon'].data
    max_val = np.nanmax(np.abs(div))/2
    max_val = np.round(max_val)
    print(max_val)
    levels =np.linspace(-max_val,max_val,nlevels)


    m = ax.contourf(lon,
                lat,
                div,
                levels = levels,
                extend = 'both',
                transform = proj,
                cmap = 'seismic')
    ax.coastlines(resolution = '50m')
    ticks = np.linspace(-max_val,max_val,9)
    if scale == 100:
        ticks = np.array([-6,-4,-2,0,2,4,6])
    else:
        ticks = np.array([-5,-3,-1,0,1,3,5])
    plt.colorbar(m,
                 ax = ax,
                 label = label,
                 orientation = 'horizontal',
                 ticks = ticks,)
    ax.set_title(f'{title}')


#cax = fig.add_axes([axs[0].get_position().x0, 
#                    axs[0].get_position().y0 - 0.04,
#                    axs[-1].get_position().x1 - axs[0].get_position().x0,
#                    0.02])
#plt.colorbar(m, 
#             orientation = 'horizontal',
#             label = r'mm w.e.',
#             cax = cax,
#             ticks = ticks,
#             )
fig.savefig('figures/regs.tot_rad.decorTP.andTP.1979-2018.pdf')
fig.savefig('figures/regs.tot_rad.decorTP.andTP.1979-2018.png')
plt.show()
