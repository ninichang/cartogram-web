import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Mainland China and Taiwan"

    def get_gen_file(self):
        return "{}/china_withSARandTWN_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 34:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Anhui
2 {} Beijing
3 {} Chongqing
4 {} Fujian
5 {} Gansu
6 {} Guangxi
7 {} Guizhou
8 {} Hainan
9 {} Hebei
10 {} Heilongjiang
11 {} Henan
12 {} Hubei
13 {} Hunan
14 {} Jiangsu
15 {} Jiangxi
16 {} Jilin
17 {} Liaoning
18 {} Inner Mongolia
19 {} Ningxia
20 {} Qinghai
21 {} Shaanxi
22 {} Shandong
23 {} Shanghai
24 {} Shanxi
25 {} Sichuan
26 {} Tianjin
27 {} Xinjiang
28 {} Tibet
29 {} Yunnan
30 {} Zhejiang
31 {} Guangdong
32 {} Hong Kong
33 {} Macau
34 {} Taiwan""".format(*values)

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "Province", 0, 1, 2, 3, ["Anhui","Beijing","Chongqing","Fujian","Gansu","Guangxi","Guizhou","Hainan","Hebei","Heilongjiang","Henan","Hubei","Hunan","Jiangsu","Jiangxi","Jilin","Liaoning","Inner Mongolia","Ningxia","Qinghai","Shaanxi","Shandong","Shanghai","Shanxi","Sichuan","Tianjin","Xinjiang","Tibet","Yunnan","Zhejiang","Guangdong","Hong Kong","Macau","Taiwan"], [0.0 for i in range(0,34)], {"Anhui":"1","Beijing":"2","Chongqing":"3","Fujian":"4","Gansu":"5","Guangxi":"6","Guizhou":"7","Hainan":"8","Hebei":"9","Heilongjiang":"10","Henan":"11","Hubei":"12","Hunan":"13","Jiangsu":"14","Jiangxi":"15","Jilin":"16","Liaoning":"17","Inner Mongolia":"18","Ningxia":"19","Qinghai":"20","Shaanxi":"21","Shandong":"22","Shanghai":"23","Shanxi":"24","Sichuan":"25","Tianjin":"26","Xinjiang":"27","Tibet":"28","Yunnan":"29","Zhejiang":"30","Guangdong":"31","Hong Kong":"32","Macau":"33","Taiwan":"34"})
