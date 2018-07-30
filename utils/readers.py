import re

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
    def get_content(f): 
        with open(f, 'r') as fobj: 
            return fobj.read()

    @staticmethod
    def get_header(f): 
        return RwlReader.get_content(f).split('\n')[:3]

    @staticmethod
    def split_row(row): 
        core_id = row[:7].strip()
        decade = row[7:12].strip()

        try: 
            decade = int(decade)
        except ValueError: 
            return False

        data = row[12:].strip().split()
        return core_id, decade, data

    def __init__(self, f): 
        self.f = f
        self.content = RwlReader.get_content(self.f)
        self.units, self.missing_value_code = RwlReader.get_units(self.content)
        self.get_metadata()

    def get_metadata(self): 
        header = self.get_header(self.f) 
        self.site_id = header[0][:7].strip()
        self.site_name = header[0][7:61].strip()
        self.species_code = header[0][61:].strip()
        self.location = header[1][7:22].strip()
        self.species = header[1][22:41].strip()
        self.elevation = header[1][41:44].strip()
        self.coordinates = header[1][47:56].strip().replace('_', '')
        self.year_range = header[1][67:].strip().replace(' ', '-')
        self.investigator = header[2][7:71].strip()
        self.comp_date = header[2][71:].strip() 

    def get_db_row(self): 
        return (self.site_id, self.site_name, self.species_code, self.location, 
            self.species, self.elevation, self.coordinates, self.year_range, 
            self.investigator, self.comp_date, self.units, self.missing_value_code)

    def get_data(self):
        for row in self.content.split('\n')[3:-1]:

            columns = RwlReader.split_row(row)

            if columns: 
                core_id, decade, data = columns
            else: 
                # print "ValueError: {}\n".format(row)
                continue

            for i, ring_width in enumerate(data): 
                ring_width = int(ring_width)
                if ring_width != self.missing_value_code:             
                    year = decade + i
                    yield self.get_db_row() + (core_id, year, ring_width)

    def print_metadata(self):
        print """
        ******************* HEADER *******************
        
        Site ID: {} Site Name: {}   Location: {}    Investigator: {}

        Species: {} Species Code: {}    Units: {}mm

        Elevation: {}   Coordinates: {} Year Range: {}  Comp. Date: {}

        File: {}

        **********************************************
        """.format(self.site_id, self.site_name, self.location, 
            self.investigator, self.species, self.species_code,
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

    