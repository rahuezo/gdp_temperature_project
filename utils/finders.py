import os
import tkFileDialog as fd

def rwl_finder(path): 
    path_dirs = [os.path.join(path, d) for d in os.listdir(path)]

    for pdir in path_dirs: 
        package = {'paleodata':[], 'metadata':[], 'correlation':[]}

        for root, dirs, files in os.walk(pdir): 
            if root.endswith('metadata'): 
                package['metadata'].extend(files)
            
            if root.endswith('correlation-stats'): 
                package['correlation'].extend(files)

            if 'measurements' in root and all([f.endswith('.rwl') for f in files]):         
                package['paleodata'].extend(files)
        
            if not all([len(package[key]) > 0 for key in package]): 
                print "ERROR "*10
                continue
            yield package
        
            # for f in files: 
            #     printf
                # if f.lower().endswith('.rwl'): 
                #     yield os.path.join(root, f)

p = fd.askdirectory(title="Choose path")


for i in rwl_finder(p): 
    print i