import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Denmark"

    def get_gen_file(self):
        return "{}/dnk_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 5:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Hovedstaden
2 {} Midtjylland
3 {} Nordjylland
4 {} Sjaelland
5 {} Syddanmark""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Hovedstaden","Midtjylland","Nordjylland","Sjaelland","Syddanmark"], [0.0 for i in range(0,5)], {"Hovedstaden":"1","Midtjylland":"2","Nordjylland":"3","Sjaelland":"4","Syddanmark":"5"})
