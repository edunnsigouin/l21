# list of useful hardcoded info for a given simulation

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 60
ltime             = np.arange(1,nltime+1,1)
nens              = 3
origin            = 'babj'
time              = '00'

# create hindcast date array        
hdates_day          = np.array([31,28,31,30,31,30,31,31,30,31,30,31])
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):
    for j in range(1,hdates_day[month-1]+1,1):
        hdates.append( format(month,"02") + format(j,"02") )
        model_version_dates.append('20140501')

nhdates = len(hdates)
