import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Conterminous United States"

    def selector_names(self):
        return ["United States (Conterminous)"]

    def get_gen_file(self):
        return "{}/usa_low48conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
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

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "State", 0, 1, 2, 3, [
            'Alabama', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware',
            'District of Columbia', 'Florida', 'Georgia', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',          'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ], [0.0 for i in range(0,49)], {'Alabama': '43','Arizona': '37','Arkansas': '47','California': '25','Colorado': '32','Connecticut': '19','Delaware': '29','District of Columbia': '28','Florida': '49','Georgia': '45','Idaho': '9','Illinois': '27','Indiana': '22','Iowa': '14','Kansas': '34','Kentucky': '33','Louisiana': '48','Maine': '4','Maryland': '31','Massachusetts': '15','Michigan': '50','Minnesota': '11','Mississippi': '44','Missouri': '36','Montana': '3','Nebraska': '16','Nevada': '23','New Hampshire': '13','New Jersey': '21','New Mexico': '42','New York': '17','North Carolina': '39','North Dakota': '5','Ohio': '26','Oklahoma': '38','Oregon': '12','Pennsylvania': '18','Rhode Island': '20','South Carolina': '46','South Dakota': '6','Tennessee': '40','Texas': '41','Utah': '24','Vermont': '10','Virginia': '35','Washington': '2','West Virginia': '30','Wisconsin': '8','Wyoming': '7'})

