from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database

import tkFileDialog as fd
import os, time


rwls_path = fd.askdirectory(title="Choose rwls root dir")

db_header = """site_id TEXT, site_name TEXT, species_code TEXT, location TEXT,
species_name TEXT, elevation TEXT, coordinates TEXT, year_range TEXT,
lead_investigator TEXT, comp_date TEXT, units REAL, missing_value_code INT,
core_id TEXT, year INT, ring_width INT
"""

if not os.path.exists('./results'): 
    os.makedirs('results')

db = Database('results/tree_ring_data.db')
tb = db.create_table('tree_ring_widths', db_header)

print "Started processing rwl files..."

total_time = 0 
overall_start_time = time.time()
file_count = 1

for rwl_file in rwl_finder(rwls_path): 
    start_time = time.time()

    reader = RwlReader(rwl_file)
    print "\tLoaded {}".format(os.path.split(rwl_file)[-1])
    print "\t\tStarting transaction..."
    db.cursor.execute('BEGIN')
    db.insert("""INSERT INTO {} VALUES({})""".format(tb, ','.join(['?' for _ in xrange(15)])), reader.get_data(), many=True) 
    db.connection.commit()
    print "\t\tFinished transaction!"

    elapsed_time = time.time() - start_time
    total_time += elapsed_time

    print "\t\tTime Elapsed: {}s\tAvg. Time: {}s\n".format(round(elapsed_time, 2), round(total_time/file_count, 2))

    file_count += 1


print "Finished processing rwl files in {}s".format(round(total_time, 2))        