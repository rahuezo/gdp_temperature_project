import os


def rwl_finder(path): 
    for root, dirs, files in os.walk(path): 
        for f in files: 
            if f.lower().endswith('.rwl'): 
                yield os.path.join(root, f)
