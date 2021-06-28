# list of useful hardcoded info for a given simulation

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 62
ltime             = np.arange(1,nltime+1,1)
nens              = 32
origin            = 'ammc'
time              = '00'

# create hindcast and model version date arrays        
hdates_day          = np.array([1,6,11,21,26])
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):
    for dpm in hdates_day:
        hdates.append(format(month,"02") + format(dpm,"02"))
        model_version_dates.append('20140101')

nhdates = len(hdates)
