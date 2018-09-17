from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database

import tkFileDialog as fd
import os, time, csv, sys
import cPickle as pk


rwls_path = fd.askdirectory(title="Choose rwls root dir")

if not rwls_path: 
    print "\nNo directory selected. Goodbye!\n"
    sys.exit()

lines = data.split('\n')


def between(n): 
    if abs(fyear) > abs(lyear): 
        a, b = lyear, fyear
    else: 
        a, b = fyear, lyear
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


fyear = 785
lyear = 1995

for line in lines:
    year = get_year(line)
    cid = line[:-len(year)]
    print cid, '|', year





# print between(1600)











