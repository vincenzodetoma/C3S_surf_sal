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

ds = xr.open_dataset(surf_path+'/Results/dataset-sss-ssd-rep-monthly_1993_2018_P20190726T0000Z.nc')

var = ds[variable].sel(lat=slice(-5,5), lon=slice(130, 280)).squeeze(dim='depth')
weights = np.cos(ds.lat*np.pi/180).sel(lat=slice(-5,5))

hov_nino = var.weighted(weights).mean(dim='lat')

climatology_mean = hov_nino.groupby("time.month").mean('time')
climatology_std = hov_nino.groupby("time.month").std("time")
stand_anomalies = xr.apply_ufunc(
    lambda x, m: (x - m),
    hov_nino.groupby("time.month"),
    climatology_mean
)

hov_nino = stand_anomalies.rename(r'$SSS~anomalies~[PSU]$')
m=np.nanmin(hov_nino).round(1)
M = np.nanmax(hov_nino).round(1)
s = min(-m, M)
fig=plt.figure(1, figsize=(8,10))
ax=fig.add_subplot(111)
p = hov_nino.plot.contourf(ax=ax, 
                  extend='both',
                  cmap='RdBu_r', 
                  vmin=-s, vmax=s, 
                  levels=int(s*10*4) +1,
                  #norm=colors.LogNorm(vmin=hov_nino.min(), vmax=hov_nino.max()),
                  cbar_kwargs={'drawedges': True})
#cont.plot.contour(ax=ax, vmin=33., vmax=34., levels=3, colors='k', add_colorbar=False)
ax.set_title(' ')
fig.savefig(surf_path+'/Figures/cmems_'+variable+'_hovmoller_0.25x0.25_regular_1993_2018_v1.png', dpi=300, transparent=True)
plt.show()

#check

var = ds[variable]#.groupby('time.year').mean(dim='time').squeeze('depth')
meanvar = var.groupby('time.month').mean('time')
anom = xr.apply_ufunc(lambda x,m: (x-m), var.groupby('time.month'), meanvar)
anom_2016_2017 = anom.sel(time=slice('2015-01-15T00:00:00.000000000','2016-12-15T00:00:00.000000000'))
#plot the two years
plt.rcParams.update({'font.size': 11})
p = anom_2016_2017.plot(vmin=-0.2, vmax=0.2, extend='both', col='time', col_wrap=6, cmap='jet', transform=ccrs.PlateCarree(), subplot_kws={'projection': ccrs.Robinson()}, figsize=(18,10), cbar_kwargs={'orientation' : 'vertical'})
for ax in p.axes.flat:
  ax.coastlines()
  ax.gridlines()

p.fig.savefig(surf_path+'/Figures/cmems_anom'+variable+'_0.25x0.25_regular_2015_2016_v1.png', dpi=300, transparent=True)
plt.show()






