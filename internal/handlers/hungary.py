import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Hungary"

    def get_gen_file(self):
        return "{}/hun_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 20:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Bacs-Kiskun
2 {} Baranya
3 {} Bekes
4 {} Borsod-Abauj-Zemplen
5 {} Budapest
6 {} Csongrad
7 {} Fejer
8 {} Gyor-Moson-Sopron
9 {} Hajdu-Bihar
10 {} Heves
11 {} Jasz-Nagykun-Szolnok
12 {} Komarom-Esztergom
13 {} Nograd
14 {} Pest
15 {} Somogy
16 {} Szabolcs-Szatmar-Bereg
17 {} Tolna
18 {} Vas
19 {} Veszprem
20 {} Zala""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Bacs-Kiskun","Baranya","Bekes","Borsod-Abauj-Zemplen","Budapest","Csongrad","Fejer","Gyor-Moson-Sopron","Hajdu-Bihar","Heves","Jasz-Nagykun-Szolnok","Komarom-Esztergom","Nograd","Pest","Somogy","Szabolcs-Szatmar-Bereg","Tolna","Vas","Veszprem","Zala"], [0.0 for i in range(0,20)], {"Bacs-Kiskun":"1","Baranya":"2","Bekes":"3","Borsod-Abauj-Zemplen":"4","Budapest":"5","Csongrad":"6","Fejer":"7","Gyor-Moson-Sopron":"8","Hajdu-Bihar":"9","Heves":"10","Jasz-Nagykun-Szolnok":"11","Komarom-Esztergom":"12","Nograd":"13","Pest":"14","Somogy":"15","Szabolcs-Szatmar-Bereg":"16","Tolna":"17","Vas":"18","Veszprem":"19","Zala":"20"})
