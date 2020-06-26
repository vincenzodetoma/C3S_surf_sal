# C3S_surf_sal
This repository contains the metrics to produce the figures of the assessment report for the C3S_511 project

In particular, the scripts inside this folder produce:

- plot_meanmap.py, plot_meanmap_dan.py, plot_climdiff.py -> plot the climatology and interannual variability for the SSS of ORAS5, CMEMS, ORAS5 on the period of CMEMS, and the climatological difference, together with respective interannual variability maps;

- scripts whose name contain trend calculate trends on the different periods;

- globmean.py -> calculate and show the globally-averaged time series for SSS.

All other scripts are ancillary code to let all the rest to work properly. Masked value in the trend map are controlled by a treshold to set in slice_trend.py: trend,h,p,z,slope,std_conf = mk_test(yearly_trend_component, np.linspace(1,n_years_trend_component,n_years_trend_component), False, 0.05), the last argument meaning that all values which have a % p-value lower than 95% are masked with nan values, because the trend estimate is not statistically significant.
