from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database

import tkFileDialog as fd
import os, time


rwls_path = fd.askdirectory(title="Choose rwls root dir")

if not os.path.exists('./results'): 
    os.makedirs('results')

# Connect / Create results database

db = Database('results/tree_ring_data.db')

# Create all tables

species_tb = db.create_table("species", "species_id NVARCHAR(4) PRIMARY KEY NOT NULL, species_name NVARCHAR(8) NULL")

sites_tb = db.create_table("sites", 
    """
    site_id NVARCHAR(7) PRIMARY KEY NOT NULL, 
    site_name NVARCHAR(52) NULL, 
    location NVARCHAR(13) NULL,
    elevation NVARCHAR(5) NULL,
    coordinates NVARCHAR(10) NULL
    """)

trees_tb = db.create_table("trees", 
    """
    tree_id NVARCHAR(7) PRIMARY KEY NOT NULL,
    ring_width REAL NOT NULL,
    species_id NVARCHAR(4) REFERENCES species(species_id) NOT NULL,
    site_id NVARCHAR(4) REFERENCES sites(site_id) NOT NULL
    """)

observations_tb = db.create_table("observations", 
    """
    observation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    tree_id NVARCHAR(4) REFERENCES trees(tree_id) NOT NULL,
    ring_width REAL REFERENCES trees(ring_width) NOT NULL,
    year INT NULL
    """)




print "Started processing rwl files..."

total_time = 0 
overall_start_time = time.time()
file_count = 1

species_ids = {}
core_ids = {}
site_ids = {}

# (self.site_id, self.site_name, self.species_id, self.location, 
#             self.species, self.elevation, self.coordinates, self.units, self.missing_value_id, core_id, year, ring_width)

print "Grabbing data for PK tables..."

for rwl_file in rwl_finder(rwls_path): 
    start_time = time.time()

    reader = RwlReader(rwl_file)
    print "\tLoaded {}".format(os.path.split(rwl_file)[-1])
    print "\t\tStarting transaction..."

    for row in reader.get_data():
        species_id = row[2]

        core_id = row[-3]
        site_id = row[0]
        


        if core_id not in core_ids: 
            width = row[-1]*row[-5]
            core_ids[core_id] = (width, species_id, site_id)

        if species_id not in species_ids: 
            species_name = row[4]
            
            species_ids[species_id] = species_name

        if site_id not in site_ids: 
            site_name = row[1]
            location = row[3]
            elevation = row[5]
            coordinates = row[6]

            site_ids[site_id] = (site_name, location, elevation, coordinates)
        
    elapsed_time = time.time() - start_time
    total_time += elapsed_time 
    print "\t\tTime Elapsed: {}s\tAvg. Time: {}s\n".format(round(elapsed_time, 2), round(total_time/file_count, 2))

    file_count += 1

print "Populating PK tables..."

# Inserting into species table

print "\tPopulating species..."
db.cursor.execute('BEGIN')

for species_id in species_ids: 
    values = (species_id, species_ids[species_id])
    db.insert("""INSERT INTO {} VALUES(?,?)""".format(species_tb), values)

db.connection.commit()

# Inserting into sites table
print "\tPopulating sites..."

db.cursor.execute('BEGIN')

for site_id in site_ids: 
    values = (site_id,) + site_ids[site_id]
    
    db.insert("""INSERT INTO {} VALUES(?,?,?,?,?)""".format(sites_tb), values)

db.connection.commit()

# Inserting into trees table
print "\tPopulating trees..."

db.cursor.execute('BEGIN')

for core_id in core_ids: 
    values = (core_id,) + core_ids[core_id]
    
    db.insert("""INSERT INTO {} VALUES(?,?,?,?)""".format(trees_tb), values)

db.connection.commit()

# Inserting into observations table
print "\tPopulating observations..."

db.cursor.execute('BEGIN')

db.insert("""INSERT INTO {} VALUES(?,?,?,?)""")

db.connection.commit()

print "Finished processing rwl files in {}s".format(round(total_time, 2))        


# print species_ids
# print core_ids

# print site_ids



# OLD CODE

# db_header = """site_id TEXT, site_name TEXT, species_id TEXT, location TEXT,
# species_name TEXT, elevation TEXT, coordinates TEXT, year_range TEXT,
# lead_investigator TEXT, comp_date TEXT, units REAL, missing_value_id INT,
# core_id TEXT, year INT, ring_width INT
# """
# tb = db.create_table('tree_ring_widths', db_header)

#     try: 
#         db.cursor.execute('BEGIN')
#         db.insert("""INSERT INTO {} VALUES({})""".format(tb, ','.join(['?' for _ in xrange(15)])), reader.get_data(), many=True) 
#         db.connection.commit()
#         print "\t\tFinished transaction!"
#     except Exception as e: 
#         print e