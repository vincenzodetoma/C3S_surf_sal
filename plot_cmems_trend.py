import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
import sys
plt.rcParams.update({'font.size':18})
variable='sos_trend_matrix'

surf_path='/DataArchive/C3S/surf_sal'

ds = xr.open_dataset(surf_path+'/Results/cmems_trend_sos_ORCA-0.25x0.25_regular_1993_2018.nc')
var = ds[variable]
meanvar = var.rename(r'SSS trend '+r'$[PSU~{year}^{-1}]$')

fig = plt.figure(1, figsize=(9,4))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                 vmin=-0.03, vmax=0.03,
                 levels=41,
                 #norm=colors.LogNorm(vmin=meanvar.min(), vmax=meanvar.max()),
                 cmap='RdBu_r',
                 cbar_kwargs={'drawedges': True})
ax.background_patch.set_facecolor('lightgrey') #instruction to have nans grey!!!!
ax.coastlines('50m')
ax.set_title('CMEMS trend')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+'cmems_'+variable+'_trend_ORCA-0.25x0.25_regular_1993_2018_v1_high_extremes.png', dpi=300, transparent=True)
plt.show()

fig = plt.figure(1, figsize=(9,4))
ax = fig.add_subplot(111, projection=ccrs.PlateCarree())
p = meanvar.plot.contourf(ax=ax, transform=ccrs.PlateCarree(), extend='both',
                 vmin=-0.01, vmax=0.01,
                 levels=41,
                 #norm=colors.LogNorm(vmin=meanvar.min(), vmax=meanvar.max()),
                 cmap='RdBu_r',
                 cbar_kwargs={'drawedges': True})
ax.background_patch.set_facecolor('lightgrey') #instruction to have nans grey!!!!
ax.coastlines('50m')
ax.set_title('CMEMS trend')
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True)
gl.xlabels_top = False
gl.ylabels_right = False
fig.savefig(surf_path+'/Figures/'+'cmems_'+variable+'_trend_ORCA-0.25x0.25_regular_1993_2018_v1_low_extremes.png', dpi=300, transparent=True)
plt.show()

