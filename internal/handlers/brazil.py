import settings
import handlers.base_handler
import csv

class CartogramHandler(handlers.base_handler.BaseCartogramHandler):

    def get_name(self):
        return "Brazil"

    def get_gen_file(self):
        return "{}/brazil_conic.gen".format(settings.CARTOGRAM_DATA_DIR)
    
    def validate_values(self, values):

        if len(values) != 27:
            return False
        
        for v in values:
            if type(v) != float:
                return False

        return True
    
    def gen_area_data(self, values):
        return """1 {} Acre
2 {} Alagoas
3 {} Amapa
4 {} Amazonas
5 {} Bahia
6 {} Ceara
7 {} Distrito Federal
8 {} Espirito Santo
9 {} Goias
10 {} Maranhao
11 {} Mato Grosso
12 {} Mato Grosso do Sul
13 {} Minas Gerais
14 {} Para
15 {} Paraiba
16 {} Parana
17 {} Pernambuco
18 {} Piaui
19 {} Rio de Janeiro
20 {} Rio Grande do Norte
21 {} Rio Grande do Sul
22 {} Rondonia
23 {} Roraima
24 {} Santa Catarina
25 {} Sao Paulo
26 {} Sergipe
27 {} Tocantins
""".format(*values)

    def csv_to_area_string_and_colors(self, csvfile):

        return self.order_by_example(csv.reader(csvfile), "State", 0, 1, 2, 3, ['Acre','Alagoas','Amapa','Amazonas','Bahia','Ceara','Distrito Federal','Espirito Santo','Goias','Maranhao','Mato Grosso','Mato Grosso do Sul','Minas Gerais','Para','Paraiba','Parana','Pernambuco','Piaui','Rio de Janeiro','Rio Grande do Norte','Rio Grande do Sul','Rondonia','Roraima','Santa Catarina','Sao Paulo','Sergipe','Tocantins'
        ], [0.0 for i in range(0,27)], {'Acre':'1','Alagoas':'2','Amapa':'3','Amazonas':'4','Bahia':'5','Ceara':'6','Distrito Federal':'7','Espirito Santo':'8','Goias':'9','Maranhao':'10','Mato Grosso':'11','Mato Grosso do Sul':'12','Minas Gerais':'13','Para':'14','Paraiba':'15','Parana':'16','Pernambuco':'17','Piaui':'18','Rio de Janeiro':'19','Rio Grande do Norte':'20','Rio Grande do Sul':'21','Rondonia':'22','Roraima':'23','Santa Catarina':'24','Sao Paulo':'25','Sergipe':'26','Tocantins':'27'})

