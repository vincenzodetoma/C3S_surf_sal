import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':18})
variable='sos'

surf_path='/DataArchive/C3S/surf_sal'

ds = xr.open_dataset(surf_path+'/Results/sos_ORCA-0.25x0.25_regular_1979_2018.nc')
var = ds[variable]
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
fig.savefig(surf_path+'/Figures/'+variable+'_meanmap_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
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
fig.savefig(surf_path+'/Figures/'+variable+'_stdmap_ORCA-0.25x0.25_regular_1979_2018_v1_high_extremes.png', dpi=300, transparent=True)
plt.show()

