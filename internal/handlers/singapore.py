import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Singapore"

    def get_gen_file(self):
        return "{}/singapore_map_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 5:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} CENTRAL REGION
2 {} EAST REGION
3 {} NORTH REGION
4 {} NORTH-EAST REGION
5 {} WEST REGION""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["CENTRAL REGION","EAST REGION","NORTH REGION","NORTH-EAST REGION","WEST REGION"], [0.0 for i in range(0,5)], {"CENTRAL REGION":"1","EAST REGION":"2","NORTH REGION":"3","NORTH-EAST REGION":"4","WEST REGION":"5"})
