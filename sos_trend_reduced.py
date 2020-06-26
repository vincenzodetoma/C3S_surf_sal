import xarray as xr
import xarray.ufuncs as xu
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import cartopy.crs as ccrs
from mk_test import mk_test
from trend_2d_parallel import trend_2d_parallel
from statsmodels.tsa.seasonal import seasonal_decompose
import sys
plt.rcParams.update({'font.size':14})
variable='sos'

surf_path='/DataArchive/C3S/surf_sal'

ds = xr.open_dataset(surf_path+'/Results/sos_ORCA-0.25x0.25_regular_1979_2018.nc')
lat = ds.lat
lon = ds.lon
var = ds[variable]
var=var.sel(time=slice('1993-01-16T00:00:00.000000000', '2018-12-16T00:00:00.000000000')) 
time=var.time

frequency = 12*2 #12=months; 2=years
nsplit = 16
trend_matrix, trend_pvalue, trend_significance = trend_2d_parallel(var.fillna(0), var.fillna(0), lat, lon, time, var[0,0,0], frequency, nsplit)
trend_matrix = xr.DataArray(trend_matrix,
                            coords={'lat':lat, 'lon':lon},
                            dims=['lat','lon'])

trend_pvalue = xr.DataArray(trend_pvalue,
                            coords={'lat':lat, 'lon':lon},
                            dims=['lat','lon'])

mask = trend_pvalue / trend_pvalue #create the mask
trend_pvalue = trend_pvalue / mask
trend_matrix = trend_matrix.rename('sos_trend_matrix')
trend_pvalue = trend_pvalue.rename('sos_trend_pvalue')

trend_matrix.to_netcdf(surf_path+'/Results/'+'reduced_trend_sos_ORCA-0.25x0.25_regular_1979_2018.nc')
trend_pvalue.to_netcdf(surf_path+'/Results/'+'reduced_pvalue_sos_ORCA-0.25x0.25_regular_1979_2018.nc')

