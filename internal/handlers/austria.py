import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Austria"

    def get_gen_file(self):
        return "{}/aut_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 9:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Burgenland
2 {} Carinthia 
3 {} Lower Austria 
5 {} Salzburg
6 {} Styria 
7 {} Tyrol 
4 {} Upper Austria 
9 {} Vienna
8 {} Vorarlberg""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Burgenland","Carinthia ","Lower Austria ","Salzburg","Styria ","Tyrol ","Upper Austria ","Vienna","Vorarlberg"], [0.0 for i in range(0,9)], {"Burgenland":"1","Carinthia ":"2","Lower Austria ":"3","Salzburg":"5","Styria ":"6","Tyrol ":"7","Upper Austria ":"4","Vienna":"9","Vorarlberg":"8"})
