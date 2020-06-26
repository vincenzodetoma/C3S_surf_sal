import xarray as xr
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
var = ds[variable]
weights = np.cos(ds.lat*np.pi/180.)
globmean = var.weighted(weights).mean(dim=['lat','lon'])

ds_new = xr.open_dataset(surf_path+'/Results/dataset-sss-ssd-rep-monthly_1993_2018_P20190726T0000Z.nc')
var_new = ds_new[variable].squeeze()
globmean_new = var_new.weighted(weights).mean(dim=['lat', 'lon'])

fig = plt.figure(1, figsize=(9,4))
ax = fig.add_subplot(111)
globmean.plot(ax=ax, marker='o', color='k')
globmean_new.plot(ax=ax, marker='o', color='blue')
ax.set_xlabel('time [yr]')
ax.set_ylabel('SSS [PSU]')
ax.set_title('Global Average of SSS')
fig.savefig(surf_path+'/Figures/'+variable+'_globmean_ORAS5_1979_2018_CMEMS_1993_2018.png', dpi=300, transparent=True)
plt.show()


