import settings
import handlers.base_handler

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_gen_file(self):
        return "{}/usa_low48splitME_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 50:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Alabama
4 {} Arizona
5 {} Arkansas
6 {} California
8 {} Colorado
9 {} Connecticut
10 {} Delaware
11 {} District of Columbia
12 {} Florida
13 {} Georgia
16 {} Idaho
17 {} Illinois
18 {} Indiana
19 {} Iowa
20 {} Kansas
21 {} Kentucky
22 {} Louisiana
2301 {} Maine
2302 {} Maine
24 {} Maryland
25 {} Massachusetts
26 {} Michigan
27 {} Minnesota
28 {} Mississippi
29 {} Missouri
30 {} Montana
31 {} Nebraska
32 {} Nevada
33 {} New Hampshire
34 {} New Jersey
35 {} New Mexico
36 {} New York
37 {} North Carolina
38 {} North Dakota
39 {} Ohio
40 {} Oklahoma
41 {} Oregon
42 {} Pennsylvania
44 {} Rhode Island
45 {} South Carolina
46 {} South Dakota
47 {} Tennessee
48 {} Texas
49 {} Utah
50 {} Vermont
51 {} Virginia
53 {} Washington
54 {} West Virginia
55 {} Wisconsin
56 {} Wyoming""".format(*values)

