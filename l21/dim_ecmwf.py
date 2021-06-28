# list of useful hardcoded info for a given simulation
# NOTE about ecmwf model version used:
# Here i'm downloading model version CY45R1 which is applicable to reforecasts with
# model version dates between 2018-06-07 and 2019-06-10.

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 46
ltime             = np.arange(1,nltime+1,1)
nens              = 10
origin            = 'ecmwf'
time              = "00"

# create hindcast date array
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):

    if month == 1:
        hdates_day         = np.array([3,7,10,14,17,21,24,28,31])
        model_version_year = np.array([2019,2019,2019,2019,2019,2019,2019,2019,2019])
    elif month == 2:
        hdates_day         = np.array([4,7,11,14,18,21,25,28])
        model_version_year = np.array([2019,2019,2019,2019,2019,2019,2019,2019])
    elif month == 3:
        hdates_day         = np.array([4,7,11,14,18,21,25,28])
        model_version_year = np.array([2019,2019,2019,2019,2019,2019,2019,2019])
    elif month == 4:
        hdates_day         = np.array([1,4,8,11,15,18,22,25,29])
        model_version_year = np.array([2019,2019,2019,2019,2019,2019,2019,2019,2019])
    elif month == 5:
        hdates_day         = np.array([2,6,9,13,16,20,23,27,30])
        model_version_year = np.array([2019,2019,2019,2019,2019,2019,2019,2019,2019])
    elif month == 6: # model_version_year changes here!
        hdates_day         = np.array([3,6,7,11,14,18,21,25,28])
        model_version_year = np.array([2019,2019,2018,2018,2018,2018,2018,2018,2018])
    elif month == 7:
        hdates_day         = np.array([2,5,9,12,16,19,23,26,30])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018,2018])
    elif month == 8:
        hdates_day         = np.array([2,6,9,13,16,20,23,27,30])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018,2018])
    elif month == 9:
        hdates_day         = np.array([3,6,10,13,17,20,24,27])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018])
    elif month == 10:
        hdates_day         = np.array([1,4,8,11,15,18,22,25,29])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018,2018])
    elif month == 11:
        hdates_day         = np.array([1,5,8,12,15,19,22,26,29])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018,2018])
    elif month == 12:
        hdates_day         = np.array([3,6,10,13,17,20,24,27,31])
        model_version_year = np.array([2018,2018,2018,2018,2018,2018,2018,2018,2018])

    for j in range(0,hdates_day.size,1):
        hdates.append(format(month,"02") + format(hdates_day[j],"02") )
        model_version_dates.append(format(model_version_year[j],"04") + format(month,"02") + format(hdates_day[j],"02") )
        
                
nhdates = len(hdates)
