from utils.finders import rwl_finder
from utils.readers import RwlReader
from utils.database import Database

import tkFileDialog as fd
import os, time, csv
import cPickle as pk


rwls_path = fd.askdirectory(title="Choose rwls root dir")


if not os.path.exists('./results'): 
    os.makedirs('results')

# # Connect / Create results database

# db = Database('results/tree_ring_data.db')

# # Create all tables

# species_tb = db.create_table("species", "species_id NVARCHAR(4) PRIMARY KEY NOT NULL, species_name NVARCHAR(8) NULL")

# sites_tb = db.create_table("sites", 
#     """
#     site_id NVARCHAR(7) PRIMARY KEY NOT NULL, 
#     site_name NVARCHAR(52) NULL, 
#     location NVARCHAR(13) NULL,
#     elevation NVARCHAR(5) NULL,
#     coordinates NVARCHAR(11) NULL
#     """)

# trees_tb = db.create_table("trees", 
#     """
#     tree_id NVARCHAR(7) PRIMARY KEY NOT NULL,
#     species_id NVARCHAR(4) REFERENCES species(species_id) NOT NULL,
#     site_id NVARCHAR(7) REFERENCES sites(site_id) NOT NULL
#     """)

# observations_tb = db.create_table("observations", 
#     """
#     observation_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
#     tree_id NVARCHAR(7) REFERENCES trees(tree_id) NOT NULL,
#     site_id NVARCHAR(7) REFERENCES sites(site_id) NOT NULL, 
#     year INT NULL,
#     year_range NVARCHAR(10) NULL,
#     ring_width REAL NOT NULL
#     """)


# print "Started processing rwl files...\n"

# total_time = 0 
# overall_start_time = time.time()
# file_count = 1

# species_ids = {}
# core_ids = {}
# site_ids = {}

# errors_file = open('errors.csv', 'wb')
# writer = csv.writer(errors_file, delimiter=',')

import sys

if not all([os.path.exists('species_dict.pkl'), os.path.exists('cores_dict.pkl'), os.path.exists('sites_dict.pkl')]): 
    print "Grabbing data for PK tables from scratch..."

    for package in rwl_finder(rwls_path): 
        # start_time = time.time()
        
        package_paleodata_files = package['paleodata']

        for paleodata_file in package_paleodata_files: 
            package_copy = {
                'correlation': package['correlation'], 
                'paleodata': [paleodata_file],
                'metadata': package['metadata']
            }

            try: 
                rwl_reader = RwlReader(package)
            except: 
                sys.exit()
                print paleodata_file
                break 



        
    #     try:
    #         reader = RwlReader(rwl_file)
    #         print "\tLoaded {}".format(os.path.split(rwl_file)[-1])

    #     except Exception as e: 
    #         print e
    #         writer.writerow([rwl_file, e])
    #         continue


    #     for row in reader.get_data():
    #         species_id = row[2]

    #         core_id = row[-3]
    #         site_id = row[0]
            


    #         if core_id not in core_ids: 
    #             core_ids[core_id] = (species_id, site_id)

    #         if species_id not in species_ids: 
    #             species_name = row[4]
                
    #             species_ids[species_id] = species_name

    #         if site_id not in site_ids: 
    #             site_name = row[1]
    #             location = row[3]
    #             elevation = row[5]
    #             coordinates = row[6]

    #             site_ids[site_id] = (site_name, location, elevation, coordinates)
            
    #     elapsed_time = time.time() - start_time
    #     total_time += elapsed_time 
    #     print "\t\tTime Elapsed: {}s\tAvg. Time: {}s\n".format(round(elapsed_time, 2), round(total_time/file_count, 2))

    #     file_count += 1

    # with open('species_dict.pkl', 'wb') as species_pkf, open('cores_dict.pkl', 'wb') as cores_pkf, open('sites_dict.pkl', 'wb') as sites_pkf:
    #     pk.dump(species_ids, species_pkf, protocol=pk.HIGHEST_PROTOCOL)
    #     pk.dump(core_ids, cores_pkf, protocol=pk.HIGHEST_PROTOCOL)
    #     pk.dump(site_ids, sites_pkf, protocol=pk.HIGHEST_PROTOCOL)
else: 
    print "Loading data for PK tables from pickles..."
    
    with open('species_dict.pkl', 'rb') as species_pkf, open('cores_dict.pkl', 'rb') as cores_pkf, open('sites_dict.pkl', 'rb') as sites_pkf:
        species_ids = pk.load(species_pkf)
        core_ids = pk.load(cores_pkf)
        site_ids = pk.load(sites_pkf)

# print "Populating PK tables..."

# # Inserting into species table

# print "\tPopulating species..."
# db.cursor.execute('BEGIN')

# for species_id in species_ids: 
#     values = (species_id, species_ids[species_id])
#     db.insert("""INSERT INTO {} VALUES(?,?)""".format(species_tb), values)

# db.connection.commit()

# # Inserting into sites table
# print "\tPopulating sites..."

# db.cursor.execute('BEGIN')

# for site_id in site_ids: 
#     values = (site_id,) + site_ids[site_id]
    
#     db.insert("""INSERT INTO {} VALUES(?,?,?,?,?)""".format(sites_tb), values)

# db.connection.commit()

# # Inserting into trees table
# print "\tPopulating trees..."

# db.cursor.execute('BEGIN')

# for core_id in core_ids: 
#     values = (core_id,) + core_ids[core_id]
    
#     db.insert("""INSERT INTO {} VALUES(?,?,?)""".format(trees_tb), values)

# db.connection.commit()

# # Inserting into observations table
# print "\tPopulating observations...\n"

# # print "Started processing rwl files..."

# file_count = 1

# # (self.site_id, self.site_name, self.species_id, self.location, 
# #             self.species, self.elevation, self.coordinates, self.units, self.missing_value_id, core_id, year, ring_width)


# for rwl_file in rwl_finder(rwls_path): 
#     start_time = time.time()

#     try:
#         reader = RwlReader(rwl_file)
#         print "\tLoaded {}".format(os.path.split(rwl_file)[-1])

#     except Exception as e: 
#         print e
#         writer.writerow([rwl_file, e])

#         continue
        
#     print "\t\tStarting transaction..."

#     db.cursor.execute('BEGIN')

#     for row in reader.get_data():
#         core_id = row[-3]
#         site_id = row[0]
#         year = row[-2]
#         year_range = reader.year_range
#         ring_width = row[-1]*row[-5]

#         values = (core_id, site_id, year, year_range, ring_width)

#         db.insert("""INSERT INTO {} VALUES(NULL,?,?,?,?,?)""".format(observations_tb), values)

#     db.connection.commit()        
        
#     elapsed_time = time.time() - start_time
#     total_time += elapsed_time 
#     print "\t\tTime Elapsed: {}s\tAvg. Time: {}s\n".format(round(elapsed_time, 2), round(total_time/file_count, 2))

#     file_count += 1


# # db.cursor.execute('BEGIN')

# # db.insert("""INSERT INTO {} VALUES(?,?,?,?)""")

# # db.connection.commit()

# print "Finished processing rwl files in {}s".format(round(total_time, 2))        






# errors_file.close()






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