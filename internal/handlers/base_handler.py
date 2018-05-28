
class BaseCartogramHandler:

    def get_gen_file(self):
        raise NotImplementedError("This function must be implemented.")
    
    def validate_values(self, values):
        raise NotImplementedError("This function must be implemented.")
    
    def gen_area_data(self, values):
        raise NotImplementedError("This function must be implemented.")
    
    def csv_to_area_string(self, csvfile):
        raise NotImplementedError("This function must be implemented.")    

    def order_by_example(self, dict_reader, name_column, data_column, order, result):

        for row in dict_reader:

            if name_column not in row or data_column not in row:
                raise ValueError('Invalid CSV file.')
            
            result[order.index(row[name_column])] = int(row[data_column])
        
        areas_string = ""

        for area in result:
            areas_string += "{};".format(area)
        
        return areas_string.rstrip(';')


    
