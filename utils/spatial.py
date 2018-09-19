from math import sqrt

import numpy as np
import matplotlib.pyplot as plt


def make_grid(lat_min=-89.75, lon_min=-179.75, step=0.5):
    lat_max = 180 + lat_min
    lon_max = 360 + lon_min

    lat_range = np.arange(lat_min, lat_max + step, step)
    lon_range = np.arange(lon_min, lon_max + step, step)

    grid = {}

    for i, lon in enumerate(lon_range): 
        for j, lat in enumerate(lat_range):
            key = (i, j)
            grid[key] = (lon, lat)
    return grid


def get_closest_cell(lon, lat, grid): 
    mkey = min(grid, key=lambda k: sqrt((grid.get(k)[0] - lon)**2 + (grid.get(k)[1] - lat)**2))   
    return mkey, grid[mkey]


def cru_dat_to_grid(p): 
    grid = {}
    with open(p, 'r') as f: 
        for i, row in enumerate(f.readlines()[:360]):
            columns = row.strip().split('    ')

            for j, col in enumerate(columns): 
                grid[(i, j)] = col

    return grid



p = r'C:\Users\Rudy\Downloads\cru_ts4.01.1901.1910.tmn.dat.gz'

g = cru_dat_to_grid(p)

print g[(147,0)]













# g = make_grid()

# print get_closest_cell(-105.75, 32.93, g)



    

