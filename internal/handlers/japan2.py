import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Japan"

    def get_gen_file(self):
        return "{}/jpn2_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 47:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Aichi
2 {} Akita
3 {} Aomori
4 {} Chiba
5 {} Ehime
6 {} Fukui
7 {} Fukuoka
8 {} Fukushima
9 {} Gifu
10 {} Gunma
11 {} Hiroshima
12 {} Hokkaido
13 {} Hyogo
14 {} Ibaraki
15 {} Ishikawa
16 {} Iwate
17 {} Kagawa
18 {} Kagoshima
19 {} Kanagawa
20 {} Kochi
21 {} Kumamoto
22 {} Kyoto
23 {} Mie
24 {} Miyagi
25 {} Miyazaki
26 {} Nagano
27 {} Nagasaki
28 {} Nara
29 {} Niigata
30 {} Oita
31 {} Okayama
32 {} Okinawa
33 {} Osaka
34 {} Saga
35 {} Saitama
36 {} Shiga
37 {} Shimane
38 {} Shizuoka
39 {} Tochigi
40 {} Tokushima
41 {} Tokyo
42 {} Tottori
43 {} Toyama
44 {} Wakayama
45 {} Yamagata
46 {} Yamaguchi
47 {} Yamanashi""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Prefectures", 0, 1, 2, 3, ["Aichi","Akita","Aomori","Chiba","Ehime","Fukui","Fukuoka","Fukushima","Gifu","Gunma","Hiroshima","Hokkaido","Hyogo","Ibaraki","Ishikawa","Iwate","Kagawa","Kagoshima","Kanagawa","Kochi","Kumamoto","Kyoto","Mie","Miyagi","Miyazaki","Nagano","Nagasaki","Nara","Niigata","Oita","Okayama","Okinawa","Osaka","Saga","Saitama","Shiga","Shimane","Shizuoka","Tochigi","Tokushima","Tokyo","Tottori","Toyama","Wakayama","Yamagata","Yamaguchi","Yamanashi"], [0.0 for i in range(0,47)], {"Aichi":"1","Akita":"2","Aomori":"3","Chiba":"4","Ehime":"5","Fukui":"6","Fukuoka":"7","Fukushima":"8","Gifu":"9","Gunma":"10","Hiroshima":"11","Hokkaido":"12","Hyogo":"13","Ibaraki":"14","Ishikawa":"15","Iwate":"16","Kagawa":"17","Kagoshima":"18","Kanagawa":"19","Kochi":"20","Kumamoto":"21","Kyoto":"22","Mie":"23","Miyagi":"24","Miyazaki":"25","Nagano":"26","Nagasaki":"27","Nara":"28","Niigata":"29","Oita":"30","Okayama":"31","Okinawa":"32","Osaka":"33","Saga":"34","Saitama":"35","Shiga":"36","Shimane":"37","Shizuoka":"38","Tochigi":"39","Tokushima":"40","Tokyo":"41","Tottori":"42","Toyama":"43","Wakayama":"44","Yamagata":"45","Yamaguchi":"46","Yamanashi":"47"})
