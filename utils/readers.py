from enum import Enum

 
CENTI_MM = 0.01
MILLI_MM = 0.001


class RWLReader: 
    @staticmethod
    def get_units(content): 
        if '-9999' in content: 
            return MILLI_MM
        return CENTI_MM

    def __init__(self, rwl_file): 
        self.rwl_file = rwl_file
        self.get_metadata() 

    def get_content(self): 
        with open(self.rwl_file, 'r') as f: 
            return f.read()

    def get_header(self): 
        return self.get_content().split('\n')[:3]

    def get_metadata(self): 
        header = self.get_header() 
        self.site_id = header[0][:7]
        self.site_name = header[0][7:61].strip()
        self.species_code = header[0][61:].strip()
        self.location = header[1][7:22].strip()
        self.species = header[1][22:42].strip()
        self.elevation = header[1][42:47].strip()
        self.coordinates = header[1][47:67].strip().replace('_', '')
        self.year_range = header[1][67:].strip().replace(' ', ' - ')
        self.investigator = header[2][7:70].strip()
        self.comp_date = header[2][70:].strip()
        self.units = RWLReader.get_units(self.get_content())

    def print_metadata(self):
        print """
        ******************* HEADER *******************
        
        Site ID: {} Site Name: {}   Location: {}    Investigator: {}

        Species: {} Species Code: {}    Units: {}

        Elevation: {}   Coordinates: {} Year Range: {}  Comp. Date: {}

        File: {}

        **********************************************
        """.format(self.site_id, self.site_name, self.location, 
            self.investigator, self.species, self.species_code,
            self.units, self.elevation, self.coordinates, self.year_range, self.comp_date, self.rwl_file)


reader = RWLReader(r"C:\Users\Mark\programming_projects\extra_curricular\gdp_temperature_project\results\treering_data_width\11836\104980115_2018-07-09\data\pub\data\paleo\treering\measurements\northamerica\usa\nc022.rwl")
# print reader
reader.print_metadata()
    