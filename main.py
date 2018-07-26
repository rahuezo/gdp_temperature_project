from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database
import tkFileDialog as fd
import os


rwls_path = fd.askdirectory(title="Choose rwls root dir")



# self.site_id, self.site_name, self.species_code, self.location, 
# self.species, self.elevation, self.coordinates, self.year_range, 
# self.investigator, self.comp_date, self.units, self.missing_value_code
# core_id, year, ring_width

db_header = """site_id TEXT, site_name TEXT, species_code TEXT, location TEXT,
species_name TEXT, elevation TEXT, coordinates TEXT, year_range TEXT,
lead_investigator TEXT, comp_date TEXT, units REAL, missing_value_code INT,
core_id TEXT, year INT, ring_width INT
"""

if not os.path.exists('./results'): 
    os.makedirs('results')

db = Database('results/tree_ring_data.db')
tb = db.create_table('tree_ring_widths', db_header)


for rwl_file in rwl_finder(rwls_path): 
    reader = RwlReader(rwl_file)

    db.cursor.execute('BEGIN')
    db.insert("""INSERT INTO {} VALUES({})""".format(tb, ','.join(['?' for _ in xrange(15)])), reader.get_data(), many=True) 
    db.connection.commit()
        