import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "India"

    def get_gen_file(self):
        return "{}/india_noLD_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 35:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Andaman and Nicobar Islands AN
2 {} Andhra Pradesh AP
3 {} Arunachal Pradesh AR
4 {} Assam AS
5 {} Bihar BR
6 {} Chandigarh CH
7 {} Chhattisgarh CT
8 {} Dadra and Nagar Haveli DN
9 {} Daman and Diu DD
10 {} Delhi DL
11 {} Goa GA
12 {} Gujarat GJ
13 {} Haryana HR
14 {} Himachal Pradesh HP
15 {} Jammu and Kashmir JK
16 {} Jharkhand JH
17 {} Karnataka KA
18 {} Kerala KL
20 {} Madhya Pradesh MP
21 {} Maharashtra MH
22 {} Manipur MN
23 {} Meghalaya ML
24 {} Mizoram MZ
25 {} Nagaland NL
26 {} Odisha OD
27 {} Puducherry PY
28 {} Punjab PB
29 {} Rajasthan RJ
30 {} Sikkim SK
31 {} Tamil Nadu TN
32 {} Telangana TG
33 {} Tripura TR
34 {} Uttar Pradesh UP
35 {} Uttarakhand UK
36 {} West Bengal WB""".format(*values)

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "State", 0, 1, 2, 3, ['Andaman and Nicobar Islands','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli','Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarakhand','West Bengal'], [0.0 for i in range(0,35)], {'Andaman and Nicobar Islands':'1','Andhra Pradesh':'2','Arunachal Pradesh':'3','Assam':'4','Bihar':'5','Chandigarh':'6','Chhattisgarh':'7','Dadra and Nagar Haveli':'8','Daman and Diu':'9','Delhi':'10','Goa':'11','Gujarat':'12','Haryana':'13','Himachal Pradesh':'14','Jammu and Kashmir':'15','Jharkhand':'16','Karnataka':'17','Kerala':'18','Madhya Pradesh':'20','Maharashtra':'21','Manipur':'22','Meghalaya':'23','Mizoram':'24','Nagaland':'25','Odisha':'26','Puducherry':'27','Punjab':'28','Rajasthan':'29','Sikkim':'30','Tamil Nadu':'31','Telangana':'32','Tripura':'33','Uttar Pradesh':'34','Uttarakhand':'35','West Bengal':'36'})

