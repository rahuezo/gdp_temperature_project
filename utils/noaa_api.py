import requests as req
import json
import time
import os 
import zipfile
import io


# 1) statistical variable -> tree ring standardized growth index 
# 2) physical property ->tree ring width


tree_ring_sgi_url = 'https://www.ncdc.noaa.gov/paleo-search/study/search.json?dataPublisher=NOAA&dataTypeId=18&cvWhats=statistical%20variable%3Eproxy%20composite%3Etree%20ring%20standardized%20growth%20index&headersOnly=true'
tree_ring_width_url = 'https://www.ncdc.noaa.gov/paleo-search/study/search.json?dataPublisher=NOAA&dataTypeId=18&cvWhats=physical%20property%3Elength%3Etotal%20ring%20width&headersOnly=true'
bundling_url = 'https://www.ncdc.noaa.gov/paleo-search/data/search.json?xmlId={}'

BREAK_LOOPS = 100


def load_json(url): 
    return json.loads(req.get(url).content)


def get_xmlid(json_content): 
    return json_content['xmlId']

def get_bundling_status(json_content): 
    return json_content['statusUrl']

def bundle_data(xmlid): 
    return get_bundling_status(load_json(bundling_url.format(xmlid)))

def check_bundling_status(status_url, break_loops=BREAK_LOOPS):     
    loops = 0 
    while True:         
        json_content = load_json(status_url)

        if(json_content['status'] == 'complete'): 
            return json_content['archive']

        if(loops > break_loops): 
            print "\nReached max loops and status was never complete.\n"
            return False 
        time.sleep(2)
        loops += 1


# import requests, zipfile, io
# r = requests.get(zip_file_url)

# z.extractall()

def get_bundle(bundle_url, directory): 
    output_zip_path = os.path.join(directory, bundle_url.split('/')[-1])
    z = zipfile.ZipFile(io.BytesIO(req.get(bundle_url).content))
    z.extractall(directory)
    return True

get_bundle(
    check_bundling_status('https://www.ncdc.noaa.gov/paleo-search/data/status.json?jobId=2093648196_2018-06-22'),
    'results'    
)







