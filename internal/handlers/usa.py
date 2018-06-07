import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_gen_file(self):
        return "{}/usa_low48_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 49:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """43 {} Alabama
37 {} Arizona
47 {} Arkansas
25 {} California
32 {} Colorado
19 {} Connecticut
29 {} Delaware
28 {} District of Columbia
49 {} Florida
45 {} Georgia
9 {} Idaho
27 {} Illinois
22 {} Indiana
14 {} Iowa
34 {} Kansas
33 {} Kentucky
48 {} Louisiana
4 {} Maine
31 {} Maryland
15 {} Massachusetts
50 {} Michigan
11 {} Minnesota
44 {} Mississippi
36 {} Missouri
3 {} Montana
16 {} Nebraska
23 {} Nevada
13 {} New Hampshire
21 {} New Jersey
42 {} New Mexico
17 {} New York
39 {} North Carolina
5 {} North Dakota
26 {} Ohio
38 {} Oklahoma
12 {} Oregon
18 {} Pennsylvania
20 {} Rhode Island
46 {} South Carolina
6 {} South Dakota
40 {} Tennessee
41 {} Texas
24 {} Utah
10 {} Vermont
35 {} Virginia
2 {} Washington
30 {} West Virginia
8 {} Wisconsin
7 {} Wyoming""".format(*values)

    def csv_to_area_string(self, csvfile):

        return self.order_by_example(csv.DictReader(csvfile), "State", "Data", [
            'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
            'District of Columbia', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',          'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ], [0.0 for i in range(0,49)])

