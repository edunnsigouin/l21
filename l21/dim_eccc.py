# list of useful hardcoded info for a given simulation
# NOTE about ecmwf model version used:
# Here i'm downloading  ECCC GEPS 6.0 Jul-2019 (high top) data
# which is applicable to reforecasts made between model version
# dates 2019-07-04 to the present. For simplicity, I just use model
# version year 2020.


import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 32
ltime             = np.arange(1,nltime+1,1)
nens              = 3
origin            = 'cwao'
time              = "00"

# create hindcast date array
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):
    if month == 1:
        hdates_day = np.array([2,9,16,23,30])
    elif month == 2:
        hdates_day = np.array([6,13,20,27])
    elif month == 3:
        hdates_day = np.array([5,12,19,26])
    elif month == 4:
        hdates_day = np.array([2,9,16,23,30])
    elif month == 5:
        hdates_day = np.array([7,14,21,28])
    elif month == 6: 
        hdates_day = np.array([4,11,18,25])
    elif month == 7:
        hdates_day = np.array([2,9,16,23,30])
    elif month == 8:
        hdates_day = np.array([6,13,20,27])
    elif month == 9:
        hdates_day = np.array([3,10,17,24])
    elif month == 10:
        hdates_day = np.array([1,15,22,29])
    elif month == 11:
        hdates_day = np.array([5,12,19,26])
    elif month == 12:
        hdates_day = np.array([3,10,17,24,31])

    for j in range(0,hdates_day.size,1):
        hdates.append(format(month,"02") + format(hdates_day[j],"02") )
        model_version_dates.append('2020' + format(month,"02") + format(hdates_day[j],"02") )
        
                
nhdates = len(hdates)
