import tkFileDialog as fd
import csv

LAT_MIN = -89.75
LON_MIN = -179.75
STR_LEN = 8


def round_coords(coords): 
    lat, lon = coords
    rlat, rlon = round(lat), round(lon)

    def tug(x, rx): 
        return rx + 0.25 if rx < x else rx - 0.25
    return tug(lat, rlat), tug(lon, rlon)

def get_rowcol(rcoords, multiplier=2): 
    rlat, rlon = rcoords

    def transform(x, xmin): 
        return x + abs(xmin)
    return int(transform(rlat, LAT_MIN) * multiplier), int(transform(rlon, LON_MIN) * multiplier)

def get_value_from_row(row_str, col):
    return row_str[col*STR_LEN : col*STR_LEN + STR_LEN]

def read_cru(p): 
    i = 0
    for line in open(p, 'r'): 
        yield i, line
        i = 0 if i == 359 else i + 1

def load_coords(p, header=True): 
    with open(p, 'rb') as f: 
        if header: f.next()

        groups = {}

        for row in csv.reader(f, delimiter=','): 
            rcoords = round_coords(map(float, row))
            row, col = get_rowcol(rcoords)

            if row not in groups: 
                groups[row] = [rcoords]
            else: 
                groups[row].append(rcoords)
        return groups
    

coordsp = fd.askopenfilename(title="Choose coords file")

groups = load_coords(coordsp)
for i in sorted(groups.iterkeys()): 
    print i, len(groups[i])


crup = fd.askopenfilename(title="Choose cru file")
for line in read_cru(crup): 
    i, values = line

    if i in groups: 
        for coord in groups[i]: 
            row, col = get_rowcol(coord)

            print "Coord: ", coord, "Value: ", get_value_from_row(values, col)



#     print line[0]

    # if line[0] == 359: 
    #     break


# p = r'C:\Users\Rudy\Downloads\cru_ts4.01.2011.2016.pre.dat.gz'

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



    

