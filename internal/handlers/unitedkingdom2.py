import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "United Kingdom"

    def get_gen_file(self):
        return "{}/gbr_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 4:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} England
2 {} Northern Ireland
3 {} Scotland
4 {} Wales""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["England","Northern Ireland","Scotland","Wales"], [0.0 for i in range(0,4)], {"England":"1","Northern Ireland":"2","Scotland":"3","Wales":"4"})
