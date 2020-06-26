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

var = ds[variable].sel(lat=slice(-5,5), lon=slice(130, 280))
weights = np.cos(ds.lat*np.pi/180).sel(lat=slice(-5,5))

hov_nino = var.weighted(weights).mean(dim='lat')

climatology_mean = hov_nino.groupby("time.month").mean('time')
climatology_std = hov_nino.groupby("time.month").std("time")
stand_anomalies = xr.apply_ufunc(
    lambda x, m: (x - m),
    hov_nino.groupby("time.month"),
    climatology_mean,
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
                  levels=int(s*10*2) +1,
                  #norm=colors.LogNorm(vmin=hov_nino.min(), vmax=hov_nino.max()),
                  cbar_kwargs={'drawedges': True})
#cont.plot.contour(ax=ax, vmin=33., vmax=34., levels=3, colors='k', add_colorbar=False)
fig.savefig(surf_path+'/Figures/'+variable+'_hovmoller_ORCA-0.25x0.25_regular_1979_2018_v1.png', dpi=300, transparent=True)
plt.show()

