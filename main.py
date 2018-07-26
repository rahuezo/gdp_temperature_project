from utils.finders import rwl_finder
from utils.readers import RwlReader

import tkFileDialog as fd
import os


rwls_path = fd.askdirectory(title="Choose rwls root dir")

for rwl_file in rwl_finder(rwls_path): 
    print os.path.split(rwl_file)[-1]
    # reader = RwlReader(rwl_file)

    # for row in reader.get_data(): 
    #     print row