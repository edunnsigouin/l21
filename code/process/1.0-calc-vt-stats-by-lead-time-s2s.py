"""
calculates statistics of extreme heat fluxes as a function lead-time
for all years, ensemble members and hindcasts for s2s model data 
"""

import numpy     as np
import xarray    as xr
from l21.misc    import get_model_dim, mask_season, tic, toc
from l21.config  import dir_s2s_raw,dir_interim,model_names


#INPUT----------------------------------------------    
model_names_local = model_names
lev               = 50                # hPa 
lats              = np.array([60,90]) # heat flux latitude averaging
season            = 'NDJFM'           
binlength         = 5                 # days
max_nltime        = 70                # max leadtime for all models  
percentile_crit   = 95                # percentile of extremes for statistics
write2file        = 0                # write netcdf flag
#---------------------------------------------------

# initialize statistics output array
max_nbins    = np.floor_divide(max_nltime,binlength)
stats_median = np.zeros((3,len(model_names_local),max_nbins)) + np.nan
stats_error  = np.zeros((3,len(model_names_local),max_nbins,2)) + np.nan
    
for m in range(0,len(model_names_local),1):

    tic()

    dir_in      = dir_s2s_raw + model_names_local[m] + '/'
    dir_out     = dir_interim + 's2s/'    
    dim         = get_model_dim(model=model_names_local[m])
    dim.nens    = dim.nens + 1 # perturbed + control forecast

    print('')
    print('model = ', model_names_local[m],', years = ',dim.timestamp)
    print('')

    
    # initialize raw data array
    nbins = np.floor_divide(dim.nltime,binlength)
    vt1   = np.zeros((dim.nhdates,dim.nyears,dim.nltime,dim.nens)) + np.nan
    vt2   = np.zeros((dim.nhdates,dim.nyears,dim.nltime,dim.nens)) + np.nan
    vt3   = np.zeros((dim.nhdates,dim.nyears,dim.nltime,dim.nens)) + np.nan
    
    for h in range(0,dim.nhdates,1):

        # read data        
        filename = dir_in + 'vt.' + str(lats[0]) + str(lats[-1]) + \
                   '.' + str(lev) + 'hpa' + '.' + dim.hdates[h] + '.nc'
        ds       = xr.open_dataset(filename)
        da1      = ds['vtk1']
        da2      = ds['vtk2']
        da3      = ds['vtkge1']
        year     = ds['time.year']
        ds.close()
        
        # mask out dates not in season with nan
        da1 = mask_season(da1,season)
        da2 = mask_season(da2,season)
        da3 = mask_season(da3,season)
        
        # Mask out lead-time dates outside 1999-2010 with nan
        # e.g. hindcast starting dec 21st 2010 will have lead times
        # in year 2011
        index = (year >= dim.years[0]) | (year <= dim.years[-1])  
        da1   = da1.where(index)
        da2   = da2.where(index)
        da3   = da3.where(index)
         
        # change year for seasons spanning two calendar years
        # e.g. november 1980 is part of NDJFM 1981 
        year = year - dim.years[0]
        if season == 'NDJFM':
            month       = da1['time.month']
            index       = (month == 11) | (month == 12)
            year[index] = year[index] + 1

        # dump in bigger array
        da1          = da1.values
        da2          = da2.values
        da3          = da3.values
        da1          = np.reshape(da1,(dim.nyears,dim.nltime,dim.nens))
        da2          = np.reshape(da2,(dim.nyears,dim.nltime,dim.nens))
        da3          = np.reshape(da3,(dim.nyears,dim.nltime,dim.nens))
        year         = year.values
        year         = np.reshape(year,(dim.nyears,dim.nltime))
        for yr in range(0,dim.nyears,1):
            for lt in range(0,dim.nltime,1):
                # when month = Nov/Dec of last year (e.g. 2010),                                                                                                    
                # data should go into next year bin (e.g. 2011)                                                                                                     
                # but it doesn't exist. Therefore don't                                                                                                 
                # record it.
                if year[yr,lt] <= dim.nyears-1: 
                    vt1[h,year[yr,lt],lt,:] = da1[yr,lt,:]                
                    vt2[h,year[yr,lt],lt,:] = da2[yr,lt,:]
                    vt3[h,year[yr,lt],lt,:] = da3[yr,lt,:]

    # reduce lead time length to have whole # of bins 
    vt1       = np.moveaxis(vt1,3,-3)
    vt2       = np.moveaxis(vt2,3,-3)
    vt3       = np.moveaxis(vt3,3,-3)    
    nbins     = np.floor_divide(dim.nltime,binlength)
    vt1       = vt1[:,:,:,0:nbins*binlength] 
    vt2       = vt2[:,:,:,0:nbins*binlength]
    vt3       = vt3[:,:,:,0:nbins*binlength]

    # collect data into lead-time bins
    vt1       = np.reshape(vt1,(dim.nhdates,dim.nens,dim.nyears,nbins,binlength))
    vt2       = np.reshape(vt2,(dim.nhdates,dim.nens,dim.nyears,nbins,binlength))
    vt3       = np.reshape(vt3,(dim.nhdates,dim.nens,dim.nyears,nbins,binlength))
    vt1       = np.moveaxis(vt1,4,0)
    vt2       = np.moveaxis(vt2,4,0)
    vt3       = np.moveaxis(vt3,4,0)
    vt1       = np.reshape(vt1,(binlength*dim.nhdates*dim.nens,dim.nyears,nbins))
    vt2       = np.reshape(vt2,(binlength*dim.nhdates*dim.nens,dim.nyears,nbins))
    vt3       = np.reshape(vt3,(binlength*dim.nhdates*dim.nens,dim.nyears,nbins))


    # calculate stats by heat flux type, model and lead time bin 
    vt1 = np.nanpercentile(vt1,percentile_crit,axis=0)
    vt2 = np.nanpercentile(vt2,percentile_crit,axis=0)
    vt3 = np.nanpercentile(vt3,percentile_crit,axis=0)
    
    stats_median[0,m,0:nbins] = np.nanmedian(vt1,axis=0)
    stats_median[1,m,0:nbins] = np.nanmedian(vt2,axis=0)
    stats_median[2,m,0:nbins] = np.nanmedian(vt3,axis=0)

    stats_error[0,m,0:nbins,0] = np.nanmedian(vt1,axis=0) - np.nanpercentile(vt1,2.5,axis=0)
    stats_error[1,m,0:nbins,0] = np.nanmedian(vt2,axis=0) - np.nanpercentile(vt2,2.5,axis=0)
    stats_error[2,m,0:nbins,0] = np.nanmedian(vt3,axis=0) - np.nanpercentile(vt3,2.5,axis=0)

    stats_error[0,m,0:nbins,1] = np.nanpercentile(vt1,97.5,axis=0) - np.nanmedian(vt1,axis=0)
    stats_error[1,m,0:nbins,1] = np.nanpercentile(vt2,97.5,axis=0) - np.nanmedian(vt2,axis=0)
    stats_error[2,m,0:nbins,1] = np.nanpercentile(vt3,97.5,axis=0) - np.nanmedian(vt3,axis=0)
    
    toc()
    

    
if write2file == 1:
    variable      = np.arange(0,3,1)
    bound         = np.arange(0,2,1)
    model         = np.arange(0,len(model_names_local),1)
    lead_time_bin = np.arange(1,max_nbins+1,1)
    
    output = xr.Dataset(data_vars={'stats_median': (('variable','model','lead_time_bin'), stats_median.astype(np.float32)),
                                   'stats_error': (('variable','model','lead_time_bin','bound'), stats_error.astype(np.float32))},
 			coords={'variable': variable,'model':model,'lead_time_bin':lead_time_bin,'bound':bound})
    
    output.stats_median.attrs['units']        = 'Kms^-1'
    output.stats_median.attrs['_FillValue']   = 'NaN'
    output.stats_median.attrs['description']  = 'median of yearly heat flux extremes for all ensembles and hindcasts in a given lead time bin'
    output.stats_error.attrs['units']         = 'Kms^-1'
    output.stats_error.attrs['_FillValue']    = 'NaN'
    output.stats_error.attrs['description']   = '95% error bounds of yearly heat flux extremes for all ensembles and hindcasts in a given lead time bin; 0 = 2.5 percentile (bottom), 1 = 97.5 percentile (top)'
    output.variable.attrs['description']      = 'zonal-mean eddy sensible heat flux; 0 = vtk1, 1 = vtk2, 2 = vt all eddies'
    output.model.attrs['description']         = '0 = jma, 1 = ncep, 2 = bom, 3 = cma, 4 = cnrm, 5 = ukmo, 6 = kma, 7 = ecmwf, 8 = isac_cnr, 9 = eccc'
    output.lead_time_bin.attrs['description'] = '0 = 1-5, 1 = 6-10, ... , 13 = 65-70'	    
    output.lead_time_bin.attrs['units']       = 'days'

    var_string     = 'zm.vt.' + str(lats[0]) + str(lats[-1]) + 'N.' + str(lev) + 'hpa' 
    outputfilename = var_string + '.stats.percentile.' + str(percentile_crit) + '.' + season + '.' + dim.timestamp + '.nc'
    output.to_netcdf(dir_out + outputfilename)
    output.close()

