import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Canada"

    def get_gen_file(self):
        return "{}/can_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 13:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Alberta
2 {} British Columbia
3 {} Manitoba
4 {} New Brunswick
5 {} Newfoundland and Labrador
6 {} Northwest Territories
7 {} Nova Scotia
8 {} Nunavut
9 {} Ontario
10 {} Prince Edward Island
11 {} Quebec
12 {} Saskatchewan
13 {} Yukon""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Alberta","British Columbia","Manitoba","New Brunswick","Newfoundland and Labrador","Northwest Territories","Nova Scotia","Nunavut","Ontario","Prince Edward Island","Quebec","Saskatchewan","Yukon"], [0.0 for i in range(0,13)], {"Alberta":"1","British Columbia":"2","Manitoba":"3","New Brunswick":"4","Newfoundland and Labrador":"5","Northwest Territories":"6","Nova Scotia":"7","Nunavut":"8","Ontario":"9","Prince Edward Island":"10","Quebec":"11","Saskatchewan":"12","Yukon":"13"})
