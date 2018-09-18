from finders import rwl_finder
from readers import RwlReader
from database import Database

import os, time, csv, sys
import tkFileDialog as fd
import cPickle as pk




def get_year(line, a, b): 
    def between(n, a, b): 
        return a <= n <= b
    result = []

    i = len(line)

    while i > 0:
        num = line[i - 1]
        if num.isdigit(): 
            result.insert(0, num)
        else: 
            break
        i -= 1
        
        current_result = ''.join(result)
        if not (current_result.isdigit() or between(int(current_result))): 
            break
    return ''.join(result)

rwls_path = fd.askdirectory(title="Choose rwls root dir")

if not rwls_path: 
    print "\nNo directory selected. Goodbye!\n"
    sys.exit()


for package in rwl_finder(rwls_path):
    package_paleodata_files = package['paleodata']

    for paleodata_file in package_paleodata_files: 
        package_copy = {
            'correlation': package['correlation'], 
            'paleodata': [paleodata_file],
            'metadata': package['metadata']
        }

        try: 
            rwl_reader = RwlReader(package)
        except Exception as e: 
            print e, paleodata_file
            # writer.writerow([paleodata_file, e])
            continue

        for row in rwl_reader.get_data(test=0): 
            print row[1][:12]
            # print "Parsed Year: ", row[0][-1], get_year(row[1], rwl_reader.year_range[0], rwl_reader.year_range[1]) 
            # print "Re-parsed year: ", get_year(row[1], rwl_reader.year_range[0], rwl_reader.year_range[1]) 




# print between(1600)











