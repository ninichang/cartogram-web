import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Finland"

    def get_gen_file(self):
        return "{}/fin_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 5:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Eastern Finland
2 {} Lapland
3 {} Oulu
4 {} Southern Finland
5 {} Western Finland""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Eastern Finland","Lapland","Oulu","Southern Finland","Western Finland"], [0.0 for i in range(0,5)], {"Eastern Finland":"1","Lapland":"2","Oulu":"3","Southern Finland":"4","Western Finland":"5"})
