import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Australia"

    def get_gen_file(self):
        return "{}/aus_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 8:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Australian Capital Territory
2 {} New South Wales
3 {} Northern Territory
4 {} Queensland
5 {} South Australia
6 {} Tasmania
7 {} Victoria
8 {} Western Australia""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Australian Capital Territory","New South Wales","Northern Territory","Queensland","South Australia","Tasmania","Victoria","Western Australia"], [0.0 for i in range(0,8)], {"Australian Capital Territory":"1","New South Wales":"2","Northern Territory":"3","Queensland":"4","South Australia":"5","Tasmania":"6","Victoria":"7","Western Australia":"8"})
