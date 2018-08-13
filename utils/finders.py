import os
import tkFileDialog as fd

def rwl_finder(path): 
    path_dirs = [os.path.join(path, d) for d in os.listdir(path)]

    for pdir in path_dirs: 
        package = {'paleodata':[], 'metadata':[], 'correlation':[]}

        for root, dirs, files in os.walk(pdir): 
            if root.endswith('metadata'): 
                package['metadata'].extend(map(lambda p: os.path.join(root, p), files))
            
            if root.endswith('correlation-stats'): 
                package['correlation'].extend(map(lambda p: os.path.join(root, p), files))

            if 'measurements' in root and all([f.endswith('.rwl') for f in files]):         
                package['paleodata'].extend(map(lambda p: os.path.join(root, p), files))
        
        if len(package['paleodata']) > 0: 
            yield package
        else: 
            print "ERROR ", pdir, package
            continue
        
        