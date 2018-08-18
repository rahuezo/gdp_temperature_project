import tkFileDialog as fd
import csv



def tb_to_csv(tb_file): 
    records = {}

    with open(tb_file, 'rb') as f: 
        reader = csv.reader(f)

        # Read header and skip
        reader.next()

        for row in reader:             
            key = (row[3], row[6], row[7])

            if key not in records: 
                records[key] = row + [None]
            else: 
                records[key][-1] = row[-1]

    return records



f = fd.askopenfilename(title="Choose tree level records csv")

print "Records: "
print tb_to_csv(f)



# ['Latitude', 'Longitude', 'Elevation', 'Site ID', 'Site Name', 'Species Name', 'Tree ID', 'Year']
# ['61.1333', '-142.0667', '876', 'wr20', 'hawkins glacier', 'white spruce', 'wr16a', '1760']



