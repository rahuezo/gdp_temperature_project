import os


def rwl_finder(path): 
    path_dirs = [os.path.join(path, d) for d in os.listdir(path)]

    for pdir in path_dirs: 
        package = {'paleoData':[], 'metadata':[], 'correlation':[]}

        for root, dirs, files in os.walk(pdir): 
            if root.endswith('metadata'): 
                package['metadata'].extend(files)
            
            if root.endswith('correlation-stats'): 
                package['correlation'].extend(files)

            if 'measurements' in root and all([f.endswith('.rwl') for f in files]): 
                package['paleoData'].extend(files)
        
        print package
            # for f in files: 
            #     printf
                # if f.lower().endswith('.rwl'): 
                #     yield os.path.join(root, f)


rwl_finder(r"E:\gdp_temperature_project\results\treering_data_width")