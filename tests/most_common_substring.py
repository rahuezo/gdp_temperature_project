import os, time, csv, sys


sys.path.append(os.path.abspath(os.path.join('..', 'utils')))

from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database

import tkFileDialog as fd
import cPickle as pk


def between(n, a=0, b=1): 
    return a <= n <= b

def get_year(line): 
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
            writer.writerow([paleodata_file, e])
            continue

        for row in rwl_reader.get_data(test=1): 
            print row




# print between(1600)











