import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Germany"

    def get_gen_file(self):
        return "{}/germany_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 16:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Hamburg HH
2 {} Niedersachsen NI
3 {} Bremen HB
4 {} Nordrhein-Westfalen NW
5 {} Hessen HE
6 {} Rheinland-Pfalz RP
7 {} Baden-Wuerttemberg BW
8 {} Bayern BY
9 {} Saarland SL
10 {} Berlin BE
11 {} Brandenburg BB
12 {} Mecklenburg-Vorpommern MV
13 {} Sachsen SN
14 {} Sachsen-Anhalt ST
15 {} Thueringen TH
16 {} Schleswig-Holstein SH
""".format(*values)

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "State", 0, 1, 2, 3, ['Hamburg','Niedersachsen','Bremen','Nordrhein-Westfalen','Hessen','Rheinland-Pfalz','Baden-Wuerttemberg','Bayern','Saarland','Berlin','Brandenburg','Mecklenburg-Vorpommern','Sachsen','Sachsen-Anhalt','Thueringen','Schleswig-Holstein'
        ], [0.0 for i in range(0,16)], {'Hamburg':'1','Niedersachsen':'2','Bremen':'3','Nordrhein-Westfalen':'4','Hessen':'5','Rheinland-Pfalz':'6','Baden-Wuerttemberg':'7','Bayern':'8','Saarland':'9','Berlin':'10','Brandenburg':'11','Mecklenburg-Vorpommern':'12','Sachsen':'13','Sachsen-Anhalt':'14','Thueringen':'15','Schleswig-Holstein':'16'})

