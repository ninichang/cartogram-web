import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Czech Republic"

    def get_gen_file(self):
        return "{}/cze_processedmap_(1).json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 14:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} South Moravian
2 {} South Bohemian
3 {} Karlovy Vary
4 {} Vysocina
5 {} Hradec Kralove
6 {} Liberec
7 {} Moravian-Silesian
8 {} Olomouc
9 {} Pardubice
10 {} Plzen
11 {} Prague
12 {} Central Bohemian
13 {} Zlin
14 {} Usti nad Labem""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["South Moravian","South Bohemian","Karlovy Vary","Vysocina","Hradec Kralove","Liberec","Moravian-Silesian","Olomouc","Pardubice","Plzen","Prague","Central Bohemian","Zlin","Usti nad Labem"], [0.0 for i in range(0,14)], {"South Moravian":"1","South Bohemian":"2","Karlovy Vary":"3","Vysocina":"4","Hradec Kralove":"5","Liberec":"6","Moravian-Silesian":"7","Olomouc":"8","Pardubice":"9","Plzen":"10","Prague":"11","Central Bohemian":"12","Zlin":"13","Usti nad Labem":"14"})
