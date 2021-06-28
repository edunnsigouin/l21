"""
Calculates statistics of extreme heat fluxes for all years
for reanalysis data
"""

import numpy           as np
import xarray          as xr
from l21               import dim_erai as dim
from l21.misc          import meridional_average,get_season,remove_leap_year_days
from l21.config        import dir_erai_processed,dir_interim

#INPUT---------------------------------------------- 
lev               = 100                # hPa
lats              = np.array([60,90]) # heat flux latitude averaging
season            = 'NDJFM'
percentile_crit   = 5                # percentile of extremes for statistics 
write2file        = 1                 
#---------------------------------------------------   

# define paths
dir_in  = dir_erai_processed
dir_out = dir_interim + 'erai' + '/'

# read data & meridionally average
filename = 'yzt.zm.vt.eddy.daily.pl.' + dim.timestamp + '.nc' 
ds       = xr.open_dataset(dir_in + filename).sel(lev = lev,method='nearest')
ds       = ds.sel(lat=slice(lats[-1],lats[0]))
ds       = meridional_average(ds)

# get season and remove leap year days
ds = get_season(ds,season)
ds = remove_leap_year_days(ds)

# calculate percentiles for each year
vt1 = ds['vtk1'].values
vt2 = ds['vtk2'].values
vt3 = ds['vtkge1'].values

ndays = int(vt1.shape[0]/dim.years.size)
vt1   = np.reshape(vt1,(dim.years.size,ndays))
vt2   = np.reshape(vt2,(dim.years.size,ndays))
vt3   = np.reshape(vt3,(dim.years.size,ndays))

vt1 = np.nanpercentile(vt1,percentile_crit,axis=-1)
vt2 = np.nanpercentile(vt2,percentile_crit,axis=-1)
vt3 = np.nanpercentile(vt3,percentile_crit,axis=-1)

# calculate statistics of percentiles
stats_median     = np.zeros((3))
stats_error      = np.zeros((3,2))

stats_median[0]  = np.nanmedian(vt1,axis=0)
stats_median[1]  = np.nanmedian(vt2,axis=0)
stats_median[2]  = np.nanmedian(vt3,axis=0)

stats_error[0,0] = np.nanmedian(vt1,axis=0) - np.nanpercentile(vt1,2.5,axis=0)
stats_error[1,0] = np.nanmedian(vt2,axis=0) - np.nanpercentile(vt2,2.5,axis=0)
stats_error[2,0] = np.nanmedian(vt3,axis=0) - np.nanpercentile(vt3,2.5,axis=0)

stats_error[0,1] = np.nanpercentile(vt1,97.5,axis=0) - np.nanmedian(vt1,axis=0)
stats_error[1,1] = np.nanpercentile(vt2,97.5,axis=0) - np.nanmedian(vt2,axis=0)
stats_error[2,1] = np.nanpercentile(vt3,97.5,axis=0) - np.nanmedian(vt3,axis=0)


if write2file == 1:
    variable = np.arange(0,3,1)
    bound    = np.arange(0,2,1)
    output   = xr.Dataset(data_vars={'stats_median': (('variable'), stats_median.astype(np.float32)),
                                   'stats_error': (('variable','bound'), stats_error.astype(np.float32))},
                          coords={'variable': variable,'bound':bound})

    output.stats_median.attrs['units']       = 'Kms^-1'
    output.stats_median.attrs['_FillValue']  = 'NaN'
    output.stats_median.attrs['description'] = 'median of yearly heat flux extremes'
    output.stats_error.attrs['units']        = 'Kms^-1'
    output.stats_error.attrs['_FillValue']   = 'NaN'
    output.stats_error.attrs['description']  = '95% error bounds of yearly heat flux extremes;0 = 2.5 percentile (bottom), 1 = 97.5 percentile (top)'
    output.variable.attrs['description']     = 'zonal-mean eddy sensible heat flux; 0 = vtk1, 1 = vtk2, 2 = vt all eddies'

    var_string     = 'zm.vt.' + str(lats[0]) + str(lats[-1]) + 'N.' + str(lev) + 'hpa'
    outputfilename = var_string + '.stats.percentile.' + str(percentile_crit) + '.' + season + '.' + dim.timestamp + '.nc'
    output.to_netcdf(dir_out + outputfilename)
    output.close()
