import re
import codecs
import chardet
import json

CENTI_MM = 0.01
MILLI_MM = 0.001


def get_first(l): 
    if len(l) > 0: 
        return l[0]
    return None

# {'correlation': [u'brit043cof.txt'], 'paleodata': [u'brit043.rwl'], 'metadata': [u'noaa-tree-2670.json']}

class RwlReader: 
    def __init__(self, package): 
        self.metadata_file = get_first(package['metadata'])
        self.correlation_file = get_first(package['correlation'])
        self.paleodata_file = get_first(package['paleodata'])
        self.site_id = self.site_name = self.species = self.species_id = self.elevation = self.coordinates = self.year_range = None

        self.units, self.missing_value_id = self.get_units(self.get_content(self.paleodata_file, raw=True))

        self.set_header_from_metadata()
        self.set_header_from_correlation()
        self.set_header_from_rwl()

        if not self.elevation: 
            self.elevation = 0

        # print "site id: ", self.site_id
        # print "site name: ", self.site_name
        # print "species: ", self.species
        # print "species id: ", self.species_id
        # print "elevation: ", self.elevation
        # print "coords: ", self.coordinates
        # print "year range: ", self.year_range

        # print self.units


    def set_header_from_metadata(self): 
        with open(self.metadata_file, 'rb') as mf: 
            metadata = json.load(mf)
            if 'site' in metadata: 
                site_data = get_first(metadata['site'])
                if site_data: 
                    if 'siteName' in site_data: 
                        site_name = site_data['siteName']                 
                        if site_name and len(site_name) and self.site_name == None: 
                            self.site_name = site_name.lower()
                    if 'geo' in site_data: 
                        geo = site_data['geo']
                        if 'geometry' in geo: 
                            geometry = geo['geometry']
                            if 'coordinates' in geometry: 
                                coordinates = geometry['coordinates']
                                if coordinates and len(coordinates) >= 2 and self.coordinates == None: 
                                    self.coordinates = coordinates
                        if 'properties' in geo: 
                            properties = geo['properties']
                            if 'maxElevationMeters' in properties: 
                                max_elevation = properties['maxElevationMeters']
                                if max_elevation and len(str(max_elevation)) and self.elevation == None: 
                                    self.elevation = max_elevation
                    if 'paleoData' in site_data: 
                        paleodata = get_first(site_data['paleoData'])
                        
                        if 'earliestYear' in paleodata and 'mostRecentYear' in paleodata: 
                            first_year = paleodata['earliestYear']
                            last_year = paleodata['mostRecentYear']
                            if first_year and last_year and len(str(first_year)) and len(str(last_year)) and self.year_range == None: 
                                self.year_range = [first_year, last_year]

                        if 'species' in paleodata: 
                            species_data = get_first(paleodata['species'])

                            if species_data: 
                                if 'speciesCode' in species_data: 
                                    species_code = species_data['speciesCode']
                                    if species_code and len(species_code) and self.species_id == None: 
                                        self.species_id = species_code.lower()
                                if 'commonName' in species_data: 
                                    common_name = species_data['commonName']
                                    if common_name and len(common_name) and self.species == None: 
                                        self.species = ' '.join(common_name).lower()
        
    def set_header_from_correlation(self):         
        content = RwlReader.get_content(self.correlation_file, raw=True) 

        first_year = re.findall(r'Beginning year.*?:.*?([0-9]+)', content)
        last_year = re.findall(r'Ending year.*?:.*?([0-9]+)', content)
        site_name = re.findall(r'Site name.*?:(.*)', content)
        species_info = re.findall(r'Species information.*?:(.*)', content)
        latitude = re.findall(r'Latitude.*?:(.*)', content)
        longitude = re.findall(r'Longitude.*?:(.*)', content)
        elevation = re.findall(r'Elevation.*?:(.*)', content)

        if first_year and last_year: 
            first_year = get_first(first_year).strip()
            last_year = get_first(last_year).strip()
            if not self.year_range:
                self.year_range = [first_year, last_year]
        if site_name: 
            site_name = get_first(site_name).strip().lower()
            if not self.site_name: 
                self.site_name = site_name
        if species_info: 
            species_info = get_first(species_info).split()
            species_id = species_info[0].strip().lower()
            species = ' '.join(species_info[1:]).strip().lower()
            if species_id and species: 
                if not self.species_id: 
                    self.species_id = species_id
                if not self.species: 
                    self.species = species
        if latitude and longitude: 
            latitude = get_first(latitude).strip().lower()
            longitude = get_first(longitude).strip().lower()
            if not self.coordinates: 
                self.coordinates = [latitude, longitude]
        if elevation: 
            elevation = get_first(elevation).strip().lower()
            if not self.elevation and elevation.replace('m', ''):
                self.elevation = elevation

    def set_header_from_rwl(self): 
        header = self.get_content(self.paleodata_file, end=3)

        site_id = header[0][:6].strip().lower()
        if site_id and not self.site_id: 
            self.site_id = site_id

        site_name = header[0][9:61].strip().lower()
        if site_name and not self.site_name: 
            self.site_name = site_name

        species_id = header[0][61:65].strip().lower()
        if species_id and not self.species_id: 
            self.species_id = species_id 

        species = header[1][22:40].strip().lower()
        if species and not self.species: 
            self.species = species

        elevation = header[1][40:45].strip().lower().replace('m', '')
        if elevation and not self.elevation: 
            self.elevation = elevation

        coordinates = header[1][47:57].strip().lower()

        print "Coordinates from rwl: ", coordinates
        year_range = header[1][67:76].strip().split(' ')

        if year_range and len(year_range) > 1 and not self.year_range: 
            self.year_range = year_range

    def get_data(self): 
        paleodata_rows = self.get_content(self.paleodata_file, start=3)

        def split_row(row): 
            core_id = row[:8].strip().lower()
            decade = row[8:12].strip()
            data = row[12:].strip().split()
            
            return core_id, decade, data

        for row in paleodata_rows:  
            core_id, decade, data = split_row(row)
            for i, ring_width in enumerate(data):
                try:  
                    ring_width = int(ring_width)
                except: 
                    continue

                try: 
                    decade = int(decade)

                except: 
                    continue

                if ring_width != self.missing_value_id:             
                    year = decade + i
                    yield (self.site_id, self.site_name, self.species, self.species_id, self.elevation, 
                            self.coordinates, self.year_range, core_id, year, round(ring_width*self.units, 6))
            
    @staticmethod
    def get_units(content): 
        if '-9999' in content: 
            return (MILLI_MM, -9999)
        elif '999': 
            return (CENTI_MM, 999)
        else: 
            return 'NA'
    
    @staticmethod
    def detect_encoding(f, nlines=40): 
        i = 0
        with open(f, 'r') as fobj:
            content = []
            for line in fobj: 
                if i > nlines: 
                    break 
                content.append(line)            
                i += 1
        encoding = chardet.detect(''.join(content))['encoding']
        return encoding

    @staticmethod
    def get_content(f, start=0, end=None, raw=False): 
        with codecs.open(f, 'r', encoding=RwlReader.detect_encoding(f)) as fobj: 
            content = fobj.read().replace('\r\n', '\n').replace('\r', '\n')
            
            if raw: 
                return content
            return content.split('\n')[start:end]


# package = {}
# package['metadata'] = [r"C:\Users\Rudy\programming_projects\extra_curricular\gdp_temperature_project\results\treering_data_width\11990\440359102_2018-07-09\metadata\noaa-tree-13992.json"]
# package['paleodata'] = [r"C:\Users\Rudy\programming_projects\extra_curricular\gdp_temperature_project\results\treering_data_width\11990\440359102_2018-07-09\data\pub\data\paleo\treering\measurements\northamerica\usa\vt010.rwl"]
# package['correlation'] = [r"C:\Users\Rudy\programming_projects\extra_curricular\gdp_temperature_project\results\treering_data_width\11990\440359102_2018-07-09\data\pub\data\paleo\treering\measurements\correlation-stats\vt010.txt"]



# reader = RwlReader(package)
# # reader.set_header_from_metadata()


# for row in reader.get_data(): 
#     print row






# class RwlReader: 
#     @staticmethod
#     def get_units(content): 
#         if '-9999' in content: 
#             return (MILLI_MM, -9999)
#         elif '999': 
#             return (CENTI_MM, 999)
#         else: 
#             return 'NA'

#     @staticmethod
#     def detect_encoding(f, nlines=4): 
#         i = 0
#         with open(f, 'r') as fobj:
#             content = []
#             for line in fobj: 
#                 if i > nlines: 
#                     break 
#                 content.append(line)            
#                 i += 1
#         encoding = chardet.detect(''.join(content))['encoding']

#         # print "Encoding: {}".format(encoding)
#         return encoding

            

#     @staticmethod
#     def get_content(f): 
#         # with open(f, 'r') as fobj: 
#         #     return fobj.read().encode('ascii', errors='ignore') # OLD WAY
#         with codecs.open(f, 'r', encoding=RwlReader.detect_encoding(f)) as fobj: 
#             return fobj.read().replace('\r\n', '\n').replace('\r', '\n')

#     @staticmethod
#     def get_header(f): 
#         return RwlReader.get_content(f).split('\n')[:3]

#     @staticmethod
#     def split_row(row): 
#         core_id = row[:8].strip()
#         decade = row[8:12].strip()

#         try: 
#             decade = int(decade)
#         except ValueError: 
#             return False

#         data = row[12:].strip().split()
#         return core_id, decade, data

#     def __init__(self, f): 
#         self.f = f
#         self.content = RwlReader.get_content(self.f)
#         self.units, self.missing_value_id = RwlReader.get_units(self.content)
#         print "Before metadata"
#         self.get_metadata()
#         print "After metadata"

#     def get_metadata(self): 
#         header = self.get_header(self.f) 
#         print "Header"
#         print header
#         print "After Header"
#         self.site_id = header[0][:6].strip()
#         self.site_name = header[0][9:61].strip()
#         self.species_id = header[0][61:65].strip()
#         self.location = header[1][9:22].strip()
#         self.species = header[1][22:40].strip()        
#         self.elevation = header[1][40:45].strip().lower().replace('m', '')

#         if len(self.elevation.lower().strip()) == 0:
#             self.elevation = 0

#         self.coordinates = header[1][47:57].strip().replace('_', '')
#         self.year_range = header[1][67:76].strip().replace(' ', '-')
#         self.investigator = header[2][9:72].strip()
#         self.comp_date = header[2][72:80].strip() 

#     def get_db_row(self): 
#         return (self.site_id, self.site_name, self.species_id, self.location, 
#             self.species, self.elevation, self.coordinates, self.units, self.missing_value_id)

#     def get_data(self):
#         for row in self.content.split('\n')[3:-1]:

#             columns = RwlReader.split_row(row)

#             if columns: 
#                 core_id, decade, data = columns
#             else: 
#                 # print "ValueError: {}\n".format(row)
#                 continue

#             for i, ring_width in enumerate(data):
#                 try:  
#                     ring_width = int(ring_width)
#                 except: 
#                     continue
#                 if ring_width != self.missing_value_id:             
#                     year = decade + i
#                     yield self.get_db_row() + (core_id, year, ring_width)

#     def print_metadata(self):
#         print """
#         ******************* HEADER *******************
        
#         Site ID: {} Site Name: {}   Location: {}    Investigator: {}

#         Species: {} Species id: {}    Units: {}mm

#         Elevation: {}   Coordinates: {} Year Range: {}  Comp. Date: {}

#         File: {}

#         **********************************************
#         """.format(self.site_id, self.site_name, self.location, 
#             self.investigator, self.species, self.species_id,
#             self.units, self.elevation, self.coordinates, self.year_range, self.comp_date, self.f)


# class CrnReader(RwlReader): 
#     @staticmethod
#     def split_row(row): 
#         site_id = row[:6]
#         decade = int(row[6:10].strip())
#         records = [(int(col[:4]), int(col[4:])) for col in re.findall(r'.{7}', row[10:])]
#         return site_id, decade, records

#     def __init__(self, f): 
#         self.f = f
#         RwlReader.__init__(self, self.f)

#     def get_data(self):
#         for row in self.content.split('\n')[3:-1]:
#             print CrnReader.split_row(row)

    