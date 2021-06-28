# list of useful hardcoded info for a given simulation
# NOTE about model version date:
# Here I use GloSea5 which is applicable to reforecasts
# with model version dates prior to 2019-04-09. So for simplicity
# I just take model version year 2018.

import numpy as np

years             = np.arange(1999,2011,1)
nyears            = years.size
timestamp         = str(years[0]) + '-' + str(years[-1])
nltime            = 60
ltime             = np.arange(1,nltime+1,1)
nens              = 6
origin            = 'egrr'
time              = '00'

# create hindcast and model version date arrays        
hdates_day          = np.array([1,9,17,25])
hdates              = [] # empty list
model_version_dates = []
for month in range(1,13,1):
    for j in hdates_day:
        hdates.append(format(month,"02") + format(j,"02"))
        model_version_dates.append('2018' + format(month,"02") + format(j,"02") )

nhdates = len(hdates)
