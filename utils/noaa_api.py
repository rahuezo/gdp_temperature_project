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

BREAK_LOOPS = 20
SLEEP_TIME = 3

TREE_RING_WIDTH_RESULTS = 'results/tree_ring_width/{}'
TREE_RING_SGI_RESULTS = 'results/tree_ring_sgi/{}'


def load_json(url): 
    return json.loads(req.get(url).content)

def get_xmlid(json_content): 
    return json_content['xmlId']

def get_bundling_status(json_content): 
    return json_content['statusUrl']

def get_bundle_url(xmlid): 
    return get_bundling_status(load_json(bundling_url.format(xmlid)))

def check_bundling_status(status_url, break_loops=BREAK_LOOPS):     
    loops = 0 
    while True:         
        json_content = load_json(status_url)
        status = json_content['status']
        print "\tBundling status: {}".format(status)

        if(status == 'complete'): 
            return json_content['archive']

        if(loops > break_loops): 
            print "\n\tReached max loops and job was never complete.\n"
            return False 
        time.sleep(SLEEP_TIME)
        print "\t\tSleeping for {} seconds...".format(SLEEP_TIME)
        loops += 1

def get_bundle(bundle_url, directory, extract=False): 
    zip_filename = bundle_url.split('/')[-1]
    output_zip_path = os.path.join(directory, zip_filename)
    bundle_content = req.get(bundle_url).content

    if extract: 
        zip_file = zipfile.ZipFile(io.BytesIO(bundle_content))
        zip_file.extractall(output_zip_path.replace('.zip', ''))
        return True
    else: 
        with open(output_zip_path, 'wb') as z: 
            z.write(bundle_content)        
    print "\tDownloaded {}".format(zip_filename)
    return True


tree_ring_width_data = load_json(tree_ring_width_url)['study']
tree_ring_sgi_data = load_json(tree_ring_sgi_url)['study']

for i, study in enumerate(tree_ring_width_data): 
    print '{} out of {} studies\n'.format(i + 1, len(tree_ring_width_data))
    xmlid = get_xmlid(study)
    
    print "Current study: {}".format(xmlid)

    results_path = TREE_RING_WIDTH_RESULTS.format(xmlid)

    if os.path.exists(results_path): 
        print "\tSkipping study because it already exists..."
        continue

    bundle_url = get_bundle_url(xmlid)
    current_status = check_bundling_status(bundle_url)

    if current_status:
        if not os.path.exists(results_path): 
            os.makedirs(results_path)
        get_bundle(current_status, results_path, extract=True)


print 

for i, study in enumerate(tree_ring_sgi_data): 
    print '{} out of {} studies\n'.format(i + 1, len(tree_ring_sgi_data))
    xmlid = get_xmlid(study)
    
    print "Current study: {}".format(xmlid)

    results_path = TREE_RING_SGI_RESULTS.format(xmlid)
    if os.path.exists(results_path): 
        print "\tSkipping study because it already exists..."
        continue

    bundle_url = get_bundle_url(xmlid)
    current_status = check_bundling_status(bundle_url)

    if current_status:
        if not os.path.exists(results_path): 
            os.makedirs(results_path)
        get_bundle(current_status, results_path, extract=True)
