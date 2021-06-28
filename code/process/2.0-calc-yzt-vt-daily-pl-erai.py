"""
Calculates daily zonal-mean eddy heat flux for reanalysis data 
as a function of yzt on pressure levels 
"""

import numpy           as np
import xarray          as xr
from dask.diagnostics  import ProgressBar
from l21               import dim_erai as dim
from l21.misc          import get_filenames_erai,calc_zm_flux
from l21.config        import dir_erai_raw,dir_erai_processed

#INPUT---------------------------------------------- 
write2file = 1
#---------------------------------------------------   

# define paths
dir_in  = dir_erai_raw
dir_out = dir_erai_processed

# read data 
files_v  = get_filenames_erai('v','pl',dir_in,dim)
files_t  = get_filenames_erai('t','pl',dir_in,dim)
ds_v     = xr.open_mfdataset(files_v)
ds_t     = xr.open_mfdataset(files_t)

# calculate flux
vtk1   = calc_zm_flux(ds_v['v'],ds_t['t'],wavenumber=1)
vtk2   = calc_zm_flux(ds_v['v'],ds_t['t'],wavenumber=2)
vtkge1 = calc_zm_flux(ds_v['v'],ds_t['t'],wavenumber=-1)

# calculate dask array explicitely 
with ProgressBar():
    vtk1   = vtk1.compute()
    vtk2   = vtk2.compute()
    vtkge1 = vtkge1.compute()

if write2file == 1:    
    vt                             = xr.merge([vtk1,vtk2,vtkge1])
    vt.vtk1.attrs['units']         = 'Km/s'
    vt.vtk2.attrs['units']         = 'Km/s'
    vt.vtkge1.attrs['units']       = 'Km/s'
    vt.vtk1.attrs['description']   = 'zonal-mean wave-1 eddy sensible heat flux'
    vt.vtk2.attrs['description']   = 'zonal-mean wave-2 eddy sensible heat flux'
    vt.vtkge1.attrs['description'] = 'zonal-mean eddy sensible heat flux'
    
    filename = 'yzt.zm.vt.eddy.daily.pl.' + dim.timestamp + '.nc'
    vt.to_netcdf(dir_out + filename)
        


