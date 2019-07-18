import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "United Arab Emirates"

    def get_gen_file(self):
        return "{}/are_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 7:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Abu Dhabi
2 {} Ajman
3 {} Dubai
4 {} Fujairah
5 {} Ras Al-Khaimah
6 {} Sharjah
7 {} Umm Al-Quwain""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Emirate", 0, 1, 2, 3, ["Abu Dhabi","Ajman","Dubai","Fujairah","Ras Al-Khaimah","Sharjah","Umm Al-Quwain"], [0.0 for i in range(0,7)], {"Abu Dhabi":"1","Ajman":"2","Dubai":"3","Fujairah":"4","Ras Al-Khaimah":"5","Sharjah":"6","Umm Al-Quwain":"7"})
