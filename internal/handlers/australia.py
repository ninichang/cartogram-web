import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Australia"

    def get_gen_file(self):
        return "{}/gadm36_AUS_islands_removed.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 8:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def remove_holes(self):
        return True
    
    def gen_area_data(self, values):
        return """2 {} New South Wales
7 {} Victoria
4 {} Queensland
5 {} South Australia
8 {} Western Australia
6 {} Tasmania
3 {} Northern Territory
1 {} Australian Capital Territory""".format(*values)

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "State", 0, 1, 2, 3, ["New South Wales","Victoria","Queensland","South Australia","Western Australia","Tasmania","Northern Territory","Australian Capital Territory"], [0.0 for i in range(0,8)], {"New South Wales":"2","Victoria":"7","Queensland":"4","South Australia":"5","Western Australia":"8","Tasmania":"6","Northern Territory":"3","Australian Capital Territory":"1"})
