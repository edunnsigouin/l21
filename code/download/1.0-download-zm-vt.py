# Downloads v and t on a given pressure level for S2S data, one hindcast at a time for all years
# e.g. 19810101, 19820101, 19830101, etc.., then calculates the meridionally averaged zonal-mean
# eddy heat flux, and puts it into one netcdf as a fxn of (time,ensemble_member).
# Control forecasts are included in as the last ensemble member.  

import os                    as os
import numpy                 as np
import xarray                as xr
from l21.misc                import get_model_dim,calc_zm_flux,meridional_average
from l21.download            import download_s2s_data
from l21.config              import dir_s2s_raw,model_names
from matplotlib              import pyplot as plt


#INPUT----------------------------------------------
model_names_local = model_names[0:10]
lev               = np.array([50]) # hPa
lats              = np.array([40,70])
variables         = ['v','t']
#---------------------------------------------------


for model in model_names_local:

    dim = get_model_dim(model=model)
    
    for h in range(0,dim.nhdates,1):
        
        hdate              = dim.hdates[h]
        model_version_date = dim.model_version_dates[h]
        
        print('')
        print('model = ', model,', model version date = ',model_version_date,', hindcast date = ',hdate,', years = ',dim.timestamp)
        print('')

        # define filenames
        filename_cf = dir_s2s_raw + model + "/vt.cf." + hdate + ".nc"
        filename_pf = dir_s2s_raw + model + "/vt.pf." + hdate + ".nc"
        filename_vt = dir_s2s_raw + model + "/vt." + str(lats[0]) + str(lats[-1]) + "." + str(lev[0]) + "hpa." + hdate + ".nc"

        # download data
        download_s2s_data("cf",filename_cf,variables,lev,lats,hdate,model_version_date,dim)
        download_s2s_data('pf',filename_pf,variables,lev,lats,hdate,model_version_date,dim)

        # concatenate perturbed and control forecast and
        # standardize dimension names
        ds_cf = xr.open_dataset(filename_cf)
        ds_pf = xr.open_dataset(filename_pf)
        ds_cf = ds_cf.assign_coords(number=dim.nens+1).expand_dims("number",axis=1)
        ds    = xr.merge([ds_pf,ds_cf])
        ds    = ds.rename({'latitude':'lat','longitude':'lon'})
        ds_cf.close()
        ds_pf.close()

        # calculate eddy heat flux
        vtk1   = calc_zm_flux(ds,variables[0],variables[1],wavenumber=1)
        vtk2   = calc_zm_flux(ds,variables[0],variables[1],wavenumber=2)
        vtkge1 = calc_zm_flux(ds,variables[0],variables[1],wavenumber=-1)
        ds.close()

        # meridional average
        vtk1   = meridional_average(vtk1)
        vtk2   = meridional_average(vtk2)
        vtkge1 = meridional_average(vtkge1)

        # merge all heat fluxes into one dataset
        vtk1.name                   = 'vtk1'
        vtk2.name                   = 'vtk2'
        vtkge1.name                 = 'vtkge1'
        vtk1.attrs['units']         = 'Km/s'
        vtk2.attrs['units']         = 'Km/s'
        vtkge1.attrs['units']       = 'Km/s'
        vtk1.attrs['description']   = 'k1 zonal-mean meridional heat flux'
        vtk2.attrs['description']   = 'k1 zonal-mean meridional heat flux'
        vtkge1.attrs['description'] = 'total eddy zonal-mean meridional heat flux'
        vt                          = xr.merge([vtk1,vtk2,vtkge1])
        
        # write 2 file
        vt.to_netcdf(filename_vt)
        vt.close()

        # remove raw data
        os.remove(filename_cf)
        os.remove(filename_pf)

