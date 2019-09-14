import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Russia"

    def get_gen_file(self):
        return "{}/rus_processedmap.json".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 83:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Adygey
2 {} Altay
3 {} Amur
4 {} Arkhangel'sk
5 {} Astrakhan'
6 {} Bashkortostan
7 {} Belgorod
8 {} Bryansk
9 {} Buryat
10 {} Chechnya
11 {} Chelyabinsk
12 {} Chukot
13 {} Chuvash
14 {} City of St. Petersburg
15 {} Dagestan
16 {} Gorno-Altay
17 {} Ingush
18 {} Irkutsk
19 {} Ivanovo
20 {} Kabardin-Balkar
21 {} Kaliningrad
22 {} Kalmyk
23 {} Kaluga
24 {} Kamchatka
25 {} Karachay-Cherkess
26 {} Karelia
27 {} Kemerovo
28 {} Khabarovsk
29 {} Khakass
30 {} Khanty-Mansiy
31 {} Kirov
32 {} Komi
33 {} Kostroma
34 {} Krasnodar
35 {} Krasnoyarsk
36 {} Kurgan
37 {} Kursk
38 {} Leningrad
39 {} Lipetsk
40 {} Maga Buryatdan
41 {} Mariy-El
42 {} Mordovia
43 {} Moscow City
44 {} Moskva
45 {} Murmansk
46 {} Nenets
47 {} Nizhegorod
48 {} North Ossetia
49 {} Novgorod
50 {} Novosibirsk
51 {} Omsk
52 {} Orel
53 {} Orenburg
54 {} Penza
55 {} Perm'
56 {} Primor'ye
57 {} Pskov
58 {} Rostov
59 {} Ryazan'
60 {} Sakha
61 {} Sakhalin
62 {} Samara
63 {} Saratov
64 {} Smolensk
65 {} Stavropol'
66 {} Sverdlovsk
67 {} Tambov
68 {} Tatarstan
69 {} Tomsk
70 {} Tula
71 {} Tuva
72 {} Tver'
73 {} Tyumen'
74 {} Udmurt
75 {} Ul'yanovsk
76 {} Vladimir
77 {} Volgograd
78 {} Vologda
79 {} Voronezh
80 {} Yamal-Nenets
81 {} Yaroslavl'
82 {} Yevrey
83 {} Zabaykal'ye""".format(*values)
    
    def expect_geojson_output(self):
        return True

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Region", 0, 1, 2, 3, ["Adygey","Altay","Amur","Arkhangel'sk","Astrakhan'","Bashkortostan","Belgorod","Bryansk","Buryat","Chechnya","Chelyabinsk","Chukot","Chuvash","City of St. Petersburg","Dagestan","Gorno-Altay","Ingush","Irkutsk","Ivanovo","Kabardin-Balkar","Kaliningrad","Kalmyk","Kaluga","Kamchatka","Karachay-Cherkess","Karelia","Kemerovo","Khabarovsk","Khakass","Khanty-Mansiy","Kirov","Komi","Kostroma","Krasnodar","Krasnoyarsk","Kurgan","Kursk","Leningrad","Lipetsk","Maga Buryatdan","Mariy-El","Mordovia","Moscow City","Moskva","Murmansk","Nenets","Nizhegorod","North Ossetia","Novgorod","Novosibirsk","Omsk","Orel","Orenburg","Penza","Perm'","Primor'ye","Pskov","Rostov","Ryazan'","Sakha","Sakhalin","Samara","Saratov","Smolensk","Stavropol'","Sverdlovsk","Tambov","Tatarstan","Tomsk","Tula","Tuva","Tver'","Tyumen'","Udmurt","Ul'yanovsk","Vladimir","Volgograd","Vologda","Voronezh","Yamal-Nenets","Yaroslavl'","Yevrey","Zabaykal'ye"], [0.0 for i in range(0,83)], {"Adygey":"1","Altay":"2","Amur":"3","Arkhangel'sk":"4","Astrakhan'":"5","Bashkortostan":"6","Belgorod":"7","Bryansk":"8","Buryat":"9","Chechnya":"10","Chelyabinsk":"11","Chukot":"12","Chuvash":"13","City of St. Petersburg":"14","Dagestan":"15","Gorno-Altay":"16","Ingush":"17","Irkutsk":"18","Ivanovo":"19","Kabardin-Balkar":"20","Kaliningrad":"21","Kalmyk":"22","Kaluga":"23","Kamchatka":"24","Karachay-Cherkess":"25","Karelia":"26","Kemerovo":"27","Khabarovsk":"28","Khakass":"29","Khanty-Mansiy":"30","Kirov":"31","Komi":"32","Kostroma":"33","Krasnodar":"34","Krasnoyarsk":"35","Kurgan":"36","Kursk":"37","Leningrad":"38","Lipetsk":"39","Maga Buryatdan":"40","Mariy-El":"41","Mordovia":"42","Moscow City":"43","Moskva":"44","Murmansk":"45","Nenets":"46","Nizhegorod":"47","North Ossetia":"48","Novgorod":"49","Novosibirsk":"50","Omsk":"51","Orel":"52","Orenburg":"53","Penza":"54","Perm'":"55","Primor'ye":"56","Pskov":"57","Rostov":"58","Ryazan'":"59","Sakha":"60","Sakhalin":"61","Samara":"62","Saratov":"63","Smolensk":"64","Stavropol'":"65","Sverdlovsk":"66","Tambov":"67","Tatarstan":"68","Tomsk":"69","Tula":"70","Tuva":"71","Tver'":"72","Tyumen'":"73","Udmurt":"74","Ul'yanovsk":"75","Vladimir":"76","Volgograd":"77","Vologda":"78","Voronezh":"79","Yamal-Nenets":"80","Yaroslavl'":"81","Yevrey":"82","Zabaykal'ye":"83"})
