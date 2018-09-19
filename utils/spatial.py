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



# p = r'C:\Users\Rudy\Downloads\cru_ts4.01.2011.2016.pre.dat.gz'

# g = cru_dat_to_grid(p)

# print g

# var a = csv.select(x => new coordinate(x[0], x[1]))
#     .groupby(x => x.row)
#     .todictionary(x => x.Key, y => y.tolist());

# int i = 0;
# foreach(var line in lines)
# {
#     if (a.containskey(i))
#         a[i].foreach(x => x.precip.add(line.substring(x.col * 8, 8)));
#     i = i == 359 ? 0 : i + 1;
# }

# class coordinate{
#     public coordinate(double lat, double lng){
#         this.original_lat = lat;
#         this.original_lng = lng;
#         this.precip = new List<int>();
#     }
#     private double _rounded_lat = int.min;
#     private double _rounded_lng = int.min;
#     private int _row = int.min;
#     private int _col = int.min;

#     public double original_lat {get;set;}
#     public double original_lng {get;set;}
#     public double rounded_lat {get {return _rounded_lat == int.min ? _rounded_lat = correctlat(this.original_lat) : _rounded_lat; } }
#     public double rounded_lng {get{return _rounded_lng == int.min ? _rounded_lng = correctlng(this.original_lng) : _rounded_lng; }}
#     public double row {get { return _row == int.min ? _row = (this.rounded_lat + 89.75) * 2 : _row; } }
#     public double col {get { return _col == int.min ? _col = (this.rounded_lng + 179.75) * 2 : _col; } }
#     public List<int> precip {get { return _precip; }}
# }













# g = make_grid()

# print get_closest_cell(-105.75, 32.93, g)



    

