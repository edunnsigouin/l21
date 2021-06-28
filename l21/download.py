"""
collection of useful functions to download s2s data from ecmwf
"""

import numpy  as np
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()


def download_s2s_data(ftype,filename,variables,levs,lats,hdate,model_version_date,dim):
    """                  
    downloads s2s model data from ecmwf for a given hindcast date   
    """    
    # define input kwargs 
    hdatestring = ""
    for year in dim.years:
        hdatestring = hdatestring + str(year) + hdate + "/"
    hdatestring = hdatestring[:-1]

    levelist = ""
    for lev in levs:
        levelist = levelist + str(lev) + "/"
    levelist = levelist[:-1]

    param = ""
    for var in variables:
        param = param + var + "/"
    param = param[:-1]

    area   = str(lats[1]) + "/-180/" + str(lats[0]) + "/180"
    if dim.time == "1200":
        step = "12/to/" + str(24*dim.nltime) + "/by/24"
    else:    
        step = "24/to/" + str(24*dim.nltime) + "/by/24"
    number = "1/to/" + str(dim.nens)

    origin = dim.origin
    time   = dim.time
    
    # download forecast data
    if ftype == "cf":
        
        server.retrieve({
            "class": "s2",
            "dataset": "s2s",
            "hdate": hdatestring,
            "date": model_version_date,
            "expver": "prod",
            "levtype": "pl",
            "levelist": levelist,
            "origin": origin,
            "param": param,
            "area": area,
            "step": step,
            "stream": "enfh",
            "format": "netcdf",
            "target": filename,
            "time": time,
            "type": ftype,
        })

    elif ftype == "pf":
        
        server.retrieve({
            "class": "s2",
            "dataset": "s2s",
            "hdate": hdatestring,
            "date": model_version_date,
            "expver": "prod",
            "levtype": "pl",
            "levelist": levelist,
            "origin": origin,
            "param": param,
            "area": area,
            "step": step,
            "stream": "enfh",
            "format": "netcdf",
            "target": filename,
            "time": time,
            "type": ftype,
            "number": number,
        })

            
    return
