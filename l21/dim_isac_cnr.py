# list of useful hardcoded info for a given simulation

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 32
ltime             = np.arange(1,nltime+1,1)
nens              = 4
origin            = 'isac'
time              = "00"

# create hindcast date array
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):    
    if month == 1:
        hdates_day = np.array([1,6,11,16,21,26,31])
    elif month == 2:
        hdates_day = np.array([5,10,15,20,25])
    elif month == 3:
        hdates_day = np.array([2,7,12,17,22,27])
    elif month == 4:
        hdates_day = np.array([1,6,11,16,21,26])
    elif month == 5:
        hdates_day = np.array([1,6,11,16,21,26,31])
    elif month == 6:
        hdates_day = np.array([5,10,15,20,25,30])
    elif month == 7:
        hdates_day = np.array([5,10,15,20,25,30])
    elif month == 8:
        hdates_day = np.array([4,9,14,19,24,29])
    elif month == 9:
        hdates_day = np.array([3,8,13,18,23,28])
    elif month == 10:
        hdates_day = np.array([3,8,13,18,23,28])
    elif month == 11:
        hdates_day = np.array([2,7,12,17,22,27])
    elif month == 12:
        hdates_day = np.array([2,7,12,17,22,27])
        
    for j in range(0,hdates_day.size,1):
        hdates.append(format(month,"02") + format(hdates_day[j],"02") )
        model_version_dates.append('20170608')
        
                
nhdates = len(hdates)
