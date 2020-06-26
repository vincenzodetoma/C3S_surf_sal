import xarray as xr
from scipy.stats import mode
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':14})
variable='sos'

surf_path='/DataArchive/C3S/surf_sal'

ds = xr.open_dataset(surf_path+'/Results/sos_ORCA-0.25x0.25_regular_1979_2018.nc')
var = ds[variable].copy()
var = var.sel(time=slice('1993-01-16T00:00:00.000000000', '2018-12-16T00:00:00.000000000'))
meanvar = var.mean(dim='time').rename(r'$SSS~[PSU]$')

fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                 vmin=30., vmax=38.,
                 cmap='YlOrRd',
                 cbar_kwargs={'shrink' : 0.80})
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_meanmap_ORCA-0.25x0.25_regular_1993_2018_v1.png', dpi=300, transparent=True)
plt.show()

stdvar = var.groupby('time.year').mean(dim='time').std('year').rename(r'$\sigma_{SSS}~[PSU]$')

fig = plt.figure(2, figsize=(15,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = stdvar.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                 vmin=0., vmax=.6, cmap='Wistia',
                 levels=21,
                 cbar_kwargs={'drawedges': True, 'shrink' : 0.80},
                 infer_intervals=True)
ax.coastlines('50m')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+variable+'_stdmap_ORCA-0.25x0.25_regular_1993_2018_v1_high_extremes.png', dpi=300, transparent=True)
plt.show()


ds_d = xr.open_dataset(surf_path+'/Results/dataset-sss-ssd-rep-monthly_1993_2018_P20190726T0000Z.nc')
var_d = ds_d[variable].copy()
var_d = var_d.squeeze()
meanvar_d = var_d.mean(dim='time').rename(r'$SSS~[PSU]$')

diff = (meanvar - meanvar_d).squeeze()
diff = diff.rename(r'$\Delta~SSS~[PSU]$')

lev=[-5, -1, -0.5, -0.25, -0.05,-0.01,0.01, 0.05, 0.25, 0.5, 1, 5]
fig = plt.figure(1, figsize=(15,8))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = diff.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                       levels=lev,
                       cmap='RdBu_r',
                       cbar_kwargs={'shrink' : 0.80, 'ticks':lev})
ax.coastlines('50m')
ax.set_title(r'$ORAS5~-~CMEMS$: min='+str(diff.min().values.round(2))+', max='+str(diff.max().values.round(2)))
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/difference_meanmap_oras5_cmems.png', dpi=300, transparent=True)
plt.show()





