
class BaseCartogramHandler:

    def get_name(self):
        raise NotImplementedError("This function must be implemented.")

    def get_gen_file(self):
        raise NotImplementedError("This function must be implemented.")
    
    def validate_values(self, values):
        raise NotImplementedError("This function must be implemented.")
    
    def gen_area_data(self, values):
        raise NotImplementedError("This function must be implemented.")
    
    def csv_to_area_string_and_colors(self, csvfile):
        raise NotImplementedError("This function must be implemented.")    

    def order_by_example(self, dict_reader, name_column, data_column, color_column, order, result, color_data):

        color_values = {}

        for row in dict_reader:

            if name_column not in row or data_column not in row or color_column not in row:
                raise ValueError('Invalid CSV file.')
            
            result[order.index(row[name_column])] = float(row[data_column])

            color_values['id_{}'.format(color_data[row[name_column]])] =  row[color_column]
        
        if len(color_values) != len(color_data):
            raise ValueError('Invalid CSV file 1.')
        
        areas_string = ""

        for area in result:
            areas_string += "{};".format(area)
        
        return areas_string.rstrip(';'), color_values


    
