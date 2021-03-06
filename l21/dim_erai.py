# list of useful hardcoded constants, coordinate grids and times for ERA interim

import numpy as np

years      = np.arange(1999,2011,1)
months     = np.arange(1,13,1)
days       = np.arange(1,366,1)
wavenumber = np.arange(0,41,1)

lat        = np.arange(90,-92.5,-2.5)
lon        = np.arange(0,360,2.5)
lev        = np.array([1, 2, 3, 5, 7, 10, 20, 30, 50, 70, 100, 125, 150, 175, 200, 225, 250, 
                       300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 775, 800, 825, 850, 
                       875, 900, 925, 950, 975, 1000])
    
timestamp  = str(years[0]) + '-' + str(years[-1])

