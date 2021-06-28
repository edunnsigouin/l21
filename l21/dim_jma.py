# list of useful hardcoded info for a given simulation

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 34
ltime             = np.arange(1,nltime+1,1)
nens              = 4
origin            = 'rjtd'
time              = "1200"

# create hindcast date array
hdates              = []
model_version_dates = [] 
for m in range(1,13,1):
    if ((m == 1) or (m == 3) or (m == 5) or (m == 7) or (m == 8) or (m == 10) or (m == 12)):
        hdates_day = np.array([10,20,31])
    elif ((m == 4) or (m == 6) or (m == 9) or (m == 11)):
        hdates_day = np.array([10,20,30])
    elif m == 2:
        hdates_day = np.array([10,20,28])
        
    for j in range(0,hdates_day.size,1):
        hdates.append( format(m,"02") + format(hdates_day[j],"02") )
        model_version_dates.append('20170131')

nhdates = len(hdates)
