#!/usr/bin/env python
import matplotlib.pyplot as plt
import matplotlib
import xarray as xr
import numpy as np
import seaborn as sns
import pandas as pd
from scipy.stats import linregress
import matplotlib as mpl
from matplotlib.ticker import StrMethodFormatter
sns.set_theme(style="white")
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
mpl.rcParams['lines.linewidth'] = 3
#dirpath = '/run/media/the038/external/data/era5/div/vD/'
dirpath = '/run/media/the038/external/data/era5/div/vQ/anomalies/'
#d = xr.open_dataset(f'{dirpath}greenland_divQ.WN1-3.summed.nc')
dirpath = '/mnt/data/greenland/decor/summed/'
#d3 = xr.open_dataset(f'{dirpath}greenland_divQ.WN4-5.summed.nc')
#d = xr.open_dataset(f'{dirpath}divQ.WN0-3.1979-2018.smoothed.addedWN4-5.anom.south_west.to_smb.summed.nc')
#d3 = xr.open_dataset(f'{dirpath}divQ.WN4-5.1979-2018.smoothed.decorWN0-3.anom.south_west.to_smb.summed.nc')
#d4 = xr.open_dataset(f'{dirpath}divQ.WN0-5.1979-2018.smoothed.anom.south_west.to_smb.summed.nc')
#d2 = xr.open_dataset(f'{dirpath}south_west_SMB_Icemask.summed.nc')
d = xr.open_dataset(f'{dirpath}divQ.WN0-3.1979-2018.30d_rm.smoothed.addedWN4-5.anom.south_west.to_smb.summed.nc')
d3 = xr.open_dataset(f'{dirpath}divQ.WN4-5.1979-2018.30d_rm.smoothed.decorWN0-3.anom.south_west.to_smb.summed.nc')
d4 = xr.open_dataset(f'{dirpath}divQ.WN0-5.1979-2018.30d_rm.smoothed.anom.south_west.to_smb.summed.nc')
d2 = xr.open_dataset(f'{dirpath}south_west_SMB_Icemask.summed.nc')
#d = xr.open_dataset(f'{dirpath}divQ.WN0-3.1979-2018.smoothed.addedWN4-5.anom.to_smb.summed.nc')
#d3 = xr.open_dataset(f'{dirpath}divQ.WN4-5.1979-2018.smoothed.decorWN0-3.anom.to_smb.summed.nc')
#d4 = xr.open_dataset(f'{dirpath}divQ.WN0-5.1979-2018.smoothed.anom.to_smb.summed.nc')
#d2 = xr.open_dataset(f'{dirpath}smb.1979-2017.anom.Icemask.summed.nc')
print(d)
d = d.sel(time = d.time.dt.year < 2018)
d3 = d3.sel(time = d3.time.dt.year < 2018)
d4 = d4.sel(time = d4.time.dt.year < 2018)

#d = xr.open_dataset(f'{dirpath}south_west_divE.WN1-3.summed.nc')
#d3 = xr.open_dataset(f'{dirpath}south_west_divE.WN4-5.summed.nc')

#d2 = xr.open_dataset(f'{dirpath2}')
years = 8 
ndays_rolling = 365*years


#d.divQ.data /= np.max(np.abs(d.divQ.data))
#d2.SMB_rec.data /= np.max(np.abs(d2.SMB_rec.data))
#d.divQ.plot()
#d_rolled = d.divQ.rolling(time = ndays_rolling).mean()
#d3_rolled = d3.divQ.rolling(time = ndays_rolling).mean()
#ddsum = (d.divE + d3.divE).rolling(time=ndays_rolling).mean()
d_rolled = d.divD.rolling(time = ndays_rolling).mean()
d3_rolled = d3.divD.rolling(time = ndays_rolling).mean()
d4_rolled = d4.divD.rolling(time = ndays_rolling).mean()
#d2.SMB_rec.plot()
d2_rolled = d2.SMB_rec.rolling(time = ndays_rolling).mean()
#print(d_rolled)
df = pd.DataFrame()
df2 = pd.DataFrame()
smbmax = np.nanmax(np.abs(d2_rolled.data[:,0,0]))
divQmax = max([np.nanmax(np.abs(d_rolled.data[:,0,0])),
    np.nanmax(np.abs(d3_rolled.data[:,0,0])),
    np.nanmax(np.abs(d4_rolled.data[:,0,0]))])

#slope,intercept,rvalue,pvalue,stderr = linregress(d2_rolled.data[:,0,0],
#        d_rolled.data[:,0,0])
#print(slope)


df2['smb'] = d2_rolled.data[ndays_rolling:,0,0]/smbmax
df['divQP'] = d_rolled.data[ndays_rolling:,0,0]/divQmax
#/divQmax #np.nanmax(np.abs(d_rolled.data[:,0,0]))

df['divQS'] = d3_rolled.data[ndays_rolling:,0,0]/divQmax
df['divQ'] = d4_rolled.data[ndays_rolling:,0,0]/divQmax
#print(np.corrcoef(df2['smb'],df['divQ']))
df['smb'] = df2['smb']
print(df.corr())

#/divQmax #np.nanmax(np.abs(d3_rolled.data[:,0,0]))
#df['divQ'] = df['divQS'] + df['divQP']
#slope,intercept,rvalue,pvalue,stderr = linregress(df['divQP'],df['smb'])
#print(slope,intercept)
#df['divQP'] *= slope
#df['divQP'] += intercept

#slope,intercept,rvalue,pvalue,stderr = linregress(df['divQS'],df['smb'])
#df['divQS'] *= slope
#df['divQS'] += intercept
#slope,intercept,rvalue,pvalue,stderr = linregress(df['divQ'],df['smb'])
#df['divQ'] *= slope
#df['divQ'] += intercept
#df['divsum'] = dsum.data[:,0,0]/np.nanmax(np.abs(dsum.data[:,0,0]))
#df['divE'] = (d_rolled.data[:,0,0] + d3_rolled.data[:,0,0])\
 #       /np.nanmax(np.abs(d_rolled.data[:,0,0] + d3_rolled.data[:,0,0]))
smbscaling = 1/10000
divscaling = 1/1000
df['time'] = d_rolled.time.data[ndays_rolling:]
df2['time'] = d_rolled.time.data[ndays_rolling:]
df = df.set_index('time')
df2 = df2.set_index('time')
fig1 = plt.figure(figsize = [24,14])
fig1.suptitle(f'{years} year running mean')
ax = fig1.add_subplot(1,1,1)
ax2 = ax.twinx()

#sns.lineplot(data = df,linewidth = 2.5,ax = ax)
p1, = ax.plot(df.index,df['divQP'],label = 'divQP',color = 'red')#,linestyle = '--')
p2, = ax.plot(df.index,df['divQS'],label = 'divQS',color = 'blue')#,linestyle = 'dotted')
p3, = ax.plot(df.index,df['divQ'],label = 'divQ',color = 'grey')#, linestyle = '-.')

#sns.lineplot(data = df2,linewidth = 2.5,ax = ax2)
ax.set_yticks(np.linspace(-1,1,11))
ax.set_yticklabels(np.round(divscaling*np.linspace(-divQmax,divQmax,11),0))
ax.set_ylabel(f'{1/divscaling:.0E} x mm w.e. (div)')
p4, = ax2.plot(df2.index,df2['smb'],label = 'smb',color = 'k')
ax2.set_yticks(np.linspace(-1,1,11))
ax2.set_yticklabels(np.round(smbscaling*np.linspace(-smbmax,smbmax,11),0))
ax2.set_ylabel(f'{1/smbscaling:.0E} x mm w.e. (smb)')
ax2.axhline(y = 0, color = 'black',alpha = .5,linestyle = '--')
plt.legend(handles = [p1,p2,p3,p4])
df2['smb'] *=smbmax
df['divQP'] *= divQmax
#/divQmax #np.nanmax(np.abs(d_rolled.data[:,0,0]))

df['divQS'] *= divQmax
df['divQ'] *= divQmax
#extra_axis = matplotlib.axis.YAxis(ax)
df1 = df[df.index < pd.to_datetime('1/1/2000')]
df3 = df[df.index >= pd.to_datetime('1/1/2000')]
#extra_axis.tick_right()
df4 = df2[df2.index < pd.to_datetime('1/1/2000')]
df5 = df2[df2.index >= pd.to_datetime('1/1/2000')]

smb_trend = df5.mean()-df4.mean()
divQtrends = df3.mean() - df1.mean()
print(smb_trend)
print(divQtrends)
divQtrends/= smb_trend['smb']
divQtrends*=100
print(divQtrends)

#extra_axis.set_ticks(np.linspace(-1,1,11))
#extra_axis.set_ticklabels(np.round(np.linspace(-smbmax,smbmax,11)))
#extra_axis.set_ylabel('mm w.e.')
#extra_axis.set_label_position('right')
#ax.add_artist(extra_axis)
#
#ax.yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))
#ax2.yaxis.set_major_formatter(StrMethodFormatter('{x:,.2f}'))

axins = inset_axes(ax, width="20%", height="30%", loc=3)
axins.yaxis.tick_right()
axins.yaxis.set_label_position('right')
axins.tick_params(labelbottom = False)

w = 0.2
centre = 0.5
bar1 = axins.bar(centre - w, divQtrends['divQP'],width = w,color = 'red')
bar2 = axins.bar(centre , divQtrends['divQS'],width = w,color = 'blue')
bar3 = axins.bar(centre + w, divQtrends['divQ'],width = w,color = 'grey')
axins.set_xticks(np.linspace(0,1,10))
axins.set_ylabel('% of smb trend')
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        axins.annotate('{a:.1f}'.format(a = height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

autolabel(bar1)
autolabel(bar2)
autolabel(bar3)
axins.set_yticks(np.linspace(0,20,6))
#plt.figure()
#sns.set_theme(style="ticks")
plt.tight_layout(rect=[0, 0, 1, 0.95])
fig1.savefig(f'figures/lineplots_{years}yrmean_1979-2017.smooth10days.greenland.Q.png')
fig1.savefig(f'figures.lineplots_{years}yrmean_1979-2017.smooth10days.greenland.Q.eps')
#fig1.savefig(f'/home/the038/workspace/mid-term-evaluation/presentation/reg_lineplots_{years}yrmean_1979-2017.south_west.Q.png')
#fig = plt.figure(figsize = [12,7])
#fig.suptitle(f'Scatterplots and regressions of {years} year running mean')
#gs = fig.add_gridspec(1,2)
###g = sns.FacetGrid(df,col = 'smb')
###g.map(sns.jointplot,'divS')
#ax1 = fig.add_subplot(gs[0,0])
#sns.regplot(x ='divQP',y = 'smb',data = df,ax = ax1,color = 'b',scatter_kws = {'alpha': .1,'color': 'k'})
#ax2 = fig.add_subplot(gs[0,1])
#sns.regplot(x = 'divQS',y = 'smb',data = df,ax = ax2,color = 'g',scatter_kws = {'alpha': .1,'color': 'k'})
#ax3 = fig.add_subplot(gs[0,2])
#sns.regplot(x = 'divsum',y = 'smb',data = df,ax = ax3,color = 'r',scatter_kws = {'alpha': .1,'color': 'k'})
#ax1.set_xlim([-1,1])
#ax1.set_ylim([-1,1])
#ax2.set_xlim([-1,1])
#ax2.set_ylim([-1,1])
##sns.jointplot(x = 'divP',y='smb',data = df, color = 'm',kind = 'reg',ax = ax1)
##sns.jointplot(x = 'divP',y='smb',data = df, color = 'm',kind = 'reg',ax = iax1)
##sns.lmplot(data = df,x = 'divP',y = 'smb',scatter_kws = {'alpha': .1,'color':'m'})
##sns.pairplot(df,kind = 'reg',hue = 'smb')
#plt.tight_layout(rect=[0, 0, 1, 0.95])

#fig.savefig(f'scatterplots_{years}yrmean_1979-2017.south_west.pdf')
#fig.savefig(f'scatterplots_{years}yrmean_1979-2017.south_west.eps')
##fig.savefig(f'scatterplots_{years}yrmean_1979-2017.south_west.png')
#plt.show()
#d_rolled.plot()
#d2_rolled.plot()
#plt.figure()
#plt.scatter(d_rolled.data,d2_rolled.data,alpha = 0.2)
#dr = d_rolled.data[:,0,0][~np.isnan(d_rolled.data[:,0,0])]
#d2r = d2_rolled.data[:,0,0][~np.isnan(d2_rolled.data[:,0,0])]
#slope,intercept,rvalue,pvalue,stderr = linregress(dr,d2r)
#print(rvalue,pvalue)
#plt.plot(dr,intercept + slope*dr,color = 'red')
plt.show()
