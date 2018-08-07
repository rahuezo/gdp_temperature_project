import re
import codecs
import chardet

CENTI_MM = 0.01
MILLI_MM = 0.001


class RwlReader: 
    @staticmethod
    def get_units(content): 
        if '-9999' in content: 
            return (MILLI_MM, -9999)
        elif '999': 
            return (CENTI_MM, 999)
        else: 
            return 'NA'

    @staticmethod
    def detect_encoding(f, nlines=4): 
        i = 0
        with open(f, 'r') as fobj:
            content = []
            for line in fobj: 
                if i > nlines: 
                    break 
                content.append(line)            
                i += 1
        encoding = chardet.detect(''.join(content))['encoding']

        # print "Encoding: {}".format(encoding)
        return encoding

            

    @staticmethod
    def get_content(f): 
        # with open(f, 'r') as fobj: 
        #     return fobj.read().encode('ascii', errors='ignore') # OLD WAY
        with codecs.open(f, 'r', encoding=RwlReader.detect_encoding(f)) as fobj: 
            return fobj.read()

    @staticmethod
    def get_header(f): 
        return RwlReader.get_content(f).split('\n')[:3]

    @staticmethod
    def split_row(row): 
        core_id = row[:8].strip()
        decade = row[8:12].strip()

        try: 
            decade = int(decade)
        except ValueError: 
            return False

        data = row[12:].strip().split()
        return core_id, decade, data

    def __init__(self, f): 
        self.f = f
        self.content = RwlReader.get_content(self.f)
        self.units, self.missing_value_id = RwlReader.get_units(self.content)
        self.get_metadata()

    def get_metadata(self): 
        header = self.get_header(self.f) 
        self.site_id = header[0][:6].strip()
        self.site_name = header[0][9:61].strip()
        self.species_id = header[0][61:65].strip()
        self.location = header[1][9:22].strip()
        self.species = header[1][22:40].strip()        
        self.elevation = header[1][40:45].strip().lower().replace('m', '')

        if len(self.elevation.lower().strip()) == 0:
            self.elevation = 0

        self.coordinates = header[1][47:57].strip().replace('_', '')
        self.year_range = header[1][67:76].strip().replace(' ', '-')
        self.investigator = header[2][9:72].strip()
        self.comp_date = header[2][72:80].strip() 

    def get_db_row(self): 
        return (self.site_id, self.site_name, self.species_id, self.location, 
            self.species, self.elevation, self.coordinates, self.units, self.missing_value_id)

    def get_data(self):
        for row in self.content.split('\n')[3:-1]:

            columns = RwlReader.split_row(row)

            if columns: 
                core_id, decade, data = columns
            else: 
                # print "ValueError: {}\n".format(row)
                continue

            for i, ring_width in enumerate(data):
                try:  
                    ring_width = int(ring_width)
                except: 
                    continue
                if ring_width != self.missing_value_id:             
                    year = decade + i
                    yield self.get_db_row() + (core_id, year, ring_width)

    def print_metadata(self):
        print """
        ******************* HEADER *******************
        
        Site ID: {} Site Name: {}   Location: {}    Investigator: {}

        Species: {} Species id: {}    Units: {}mm

        Elevation: {}   Coordinates: {} Year Range: {}  Comp. Date: {}

        File: {}

        **********************************************
        """.format(self.site_id, self.site_name, self.location, 
            self.investigator, self.species, self.species_id,
            self.units, self.elevation, self.coordinates, self.year_range, self.comp_date, self.f)


class CrnReader(RwlReader): 
    @staticmethod
    def split_row(row): 
        site_id = row[:6]
        decade = int(row[6:10].strip())
        records = [(int(col[:4]), int(col[4:])) for col in re.findall(r'.{7}', row[10:])]
        return site_id, decade, records

    def __init__(self, f): 
        self.f = f
        RwlReader.__init__(self, self.f)

    def get_data(self):
        for row in self.content.split('\n')[3:-1]:
            print CrnReader.split_row(row)

    