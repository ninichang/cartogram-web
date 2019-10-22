import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Nigeria"

    def get_gen_file(self):
        return "{}/nga_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 37:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Abia
2 {} Adamawa
3 {} Akwa Ibom
4 {} Anambra
5 {} Bauchi
6 {} Bayelsa
7 {} Benue
8 {} Borno
9 {} Cross River
10 {} Delta
11 {} Ebonyi
12 {} Edo
13 {} Ekiti
14 {} Enugu
15 {} Federal Capital Territory
16 {} Gombe
17 {} Imo
18 {} Jigawa
19 {} Kaduna
20 {} Kano
21 {} Katsina
22 {} Kebbi
23 {} Kogi
24 {} Kwara
25 {} Lagos
26 {} Nassarawa
27 {} Niger
28 {} Ogun
29 {} Ondo
30 {} Osun
31 {} Oyo
32 {} Plateau
33 {} Rivers
34 {} Sokoto
35 {} Taraba
36 {} Yobe
37 {} Zamfara""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Abia","Adamawa","Akwa Ibom","Anambra","Bauchi","Bayelsa","Benue","Borno","Cross River","Delta","Ebonyi","Edo","Ekiti","Enugu","Federal Capital Territory","Gombe","Imo","Jigawa","Kaduna","Kano","Katsina","Kebbi","Kogi","Kwara","Lagos","Nassarawa","Niger","Ogun","Ondo","Osun","Oyo","Plateau","Rivers","Sokoto","Taraba","Yobe","Zamfara"], [0.0 for i in range(0,37)], {"Abia":"1","Adamawa":"2","Akwa Ibom":"3","Anambra":"4","Bauchi":"5","Bayelsa":"6","Benue":"7","Borno":"8","Cross River":"9","Delta":"10","Ebonyi":"11","Edo":"12","Ekiti":"13","Enugu":"14","Federal Capital Territory":"15","Gombe":"16","Imo":"17","Jigawa":"18","Kaduna":"19","Kano":"20","Katsina":"21","Kebbi":"22","Kogi":"23","Kwara":"24","Lagos":"25","Nassarawa":"26","Niger":"27","Ogun":"28","Ondo":"29","Osun":"30","Oyo":"31","Plateau":"32","Rivers":"33","Sokoto":"34","Taraba":"35","Yobe":"36","Zamfara":"37"})
