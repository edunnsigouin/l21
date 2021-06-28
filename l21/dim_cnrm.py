# list of useful hardcoded info for a given simulation

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 61
ltime             = np.arange(1,nltime+1,1)
nens              = 14
origin            = 'lfpw'
time              = '00'

# create hindcast date array        
hdates_day          = np.array([1,8,15,22])
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):
    for j in hdates_day:
        hdates.append(format(month,"02") + format(j,"02"))
        model_version_dates.append('20141201')

nhdates = len(hdates)
