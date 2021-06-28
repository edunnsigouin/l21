# collection of useful functions for S2S analysis

import xrft as xrft
import numpy as np
import xarray as xr


def get_model_dim(model):
    """
    imports a set of predifined values specific to 
    a given model 
    """
    if model == 'bom':
        from l21 import dim_bom as dim
    if model == 'cma':
        from l21 import dim_cma as dim
    if model == 'cnrm':
        from l21 import dim_cnrm as dim
    if model == 'ecmwf':
        from l21 import dim_ecmwf as dim
    if model == 'kma':
        from l21 import dim_kma as dim
    if model == 'ncep':
        from l21 import dim_ncep as dim
    if model == 'ukmo':
        from l21 import dim_ukmo as dim
    if model == 'eccc':
        from l21 import dim_eccc as dim
    if model == 'isac_cnr':
        from l21 import dim_isac_cnr as dim
    if model == 'jma':
        from l21 import dim_jma as dim
        
    return dim




def get_zonal_wavenumber(da,wavenumber):
    """
    extracts specified zonal-wavenumber
    from zonal direction in an xarray data array
    NOTE: can only extract a single wavenumber or
    all eddies (k >= 1). Need to add option for 
    specified range of wavenumbers
    """
    # fft
    da['lon'] = np.deg2rad(da['lon'])
    da_fft    = xrft.fft(da,dim='lon')
    da['lon'] = np.rad2deg(da['lon'])
    
    # filter out wavenumber(s)
    wavenumbers = abs(np.rint(da_fft.freq_lon*np.pi*2)).astype(int)
    if wavenumber >= 0:
        condition = wavenumbers == wavenumber
    else:
        condition = wavenumbers >= 1
    da_fft = da_fft.where(condition,other=0.0) # make other wavenumbers zero

    # inverse fft
    ida_fft = xrft.ifft(da_fft,dim='freq_lon')
    ida_fft = ida_fft.assign_coords(lon=da['lon']) # fix phase shifted longitude

    return ida_fft.real




def meridional_average(ds):
    """
    performs a latitude weighted meridional average
    on an xarray dataset or dataarray.
    NOTE: lats must be in degrees
    """
    weights = np.cos(np.deg2rad(ds.lat))

    return ds.weighted(weights).mean(dim='lat')



def calc_zm_flux(da1,da2,wavenumber):
    """
    calculates the zonal-mean flux 
    \overline{var1*var2} in an xarray dataset  
    """

    flux  = get_zonal_wavenumber(da1,wavenumber)*get_zonal_wavenumber(da2,wavenumber)
    flux  = flux.mean('lon')
    
    # metadata
    if wavenumber >= 0:
        flux.name = da1.name + da2.name + 'k' + str(wavenumber)
    else:
        flux.name = da1.name + da2.name + 'kge1'
        
    return flux



def get_season(ds,season):
    """        
    extracts season dates
    """
    months = ds['time.month']

    if season == 'NDJFM':
        index = (months >= 11) | (months <= 3)
    elif season == 'MJJAS':
        index = (months >= 5) & (months <= 9)
    elif season == 'ANNUAL':
        index = (months >= 1) & (months <= 12)
    elif season == 'DJF':
        index = (months >= 12) | (months <= 2)
    elif season == 'MAM':
        index = (months >= 3) & (months <= 5)
    elif season == 'JJA':
        index = (months >= 6) & (months <= 8)
    elif season == 'SON':
        index = (months >= 9) & (months <= 11)
    elif season == 'JFM':
        index = (months >= 1) & (months <= 3)
    
    return ds.sel(time=index)



def mask_season(da,season):
    """  
    mask dates not part of season as nan
    """
    
    months = da['time.month']

    if season == 'NDJFM':
        index = (months >= 11) | (months <= 3)
    elif season == 'MJJAS':
        index = (months >= 5) & (months <= 9)
    elif season == 'ANNUAL':
        index = (months >= 1) & (months <= 12)
    elif season == 'DJF':
        index = (months >= 12) | (months <= 2)
    elif season == 'MAM':
        index = (months >= 3) & (months <= 5)
    elif season == 'JJA':
        index = (months >= 6) & (months <= 8)
    elif season == 'SON':
        index = (months >= 9) & (months <= 11)
    elif season == 'JFM':
        index = (months >= 1) & (months <= 3)

    return da.where(index)





def get_filenames_erai(var,levtype,dir_in,dim):
    """
    generates a list of file names
    for a given variable across different
    monthly chunks                                                                                                     
    """
    base_dir = dir_in + levtype + '/' + var + '/' + var
    files    = [f'{base_dir}_{year}-{format(month,"02")}.nc' \
                for year in dim.years for month in dim.months]
    return files




def remove_leap_year_days(ds):
    """   
    removes leap-year days from daily xrray dataset
    """
    return ds.sel(time=~((ds.time.dt.month == 2) & (ds.time.dt.day == 29)))





def tic():
    # python version of matlab tic function
    import time
    global startTime_for_tictoc
    startTime_for_tictoc = time.time()


def toc():
    # python version of matlab tic function 
    import time
    if 'startTime_for_tictoc' in globals():
        print("Elapsed time is " + str(time.time() - startTime_for_tictoc) + " seconds.")
    else:
        print("Toc: start time not set")







