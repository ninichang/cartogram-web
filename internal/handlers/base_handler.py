
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
    
    def remove_holes(self):
        return False
    
    def expect_geojson_output(self):
        return False

    def selector_names(self):
        return [self.get_name()]

    
    # This function takes a CSVReader and returns a tuple containing:
    #   
    #   1. The areas string
    #   2. Color values for each region
    #   3. Tooltip data for each region
    #   
    # The required input is as follows:
    #
    #   dict_reader: An instance of CSVReader
    #   name_column: The name of the column that contains the region names
    #   data_column: The name of the column that contains the user data
    #   color_column: The name of the column that contains the color data
    #   order:  An array contain the region names in the order they are found in the area data template. So, if your
    #           area data template looks like:
    #
    #           1 {} RegionA
    #           2 {} RegionB
    #           3 {} RegionC
    #           ...
    #           
    #           Then your array should look like ['RegionA','RegionB','RegionC',...]
    #   result:     An array that is as long as the number of regions containing the default value (usually 0.0)
    #   id_data:    A dictionary whose keys are region names and whose values are their corresponding IDs. For the above
    #               example, the dictionary would look like: {'RegionA': '1', 'RegionB': '2', 'RegionC': '3', ...}
    def order_by_example(self, csv_reader, region_name, name_column, population_column, data_column, color_column, order, result, id_data):

        first_row = True
        color_values = {}
        tooltip = {'label': 'User Data', 'unit': '', 'data': {}}
        grid_document = {'name': self.get_name(), 'width': 4, 'height': len(order) + 1, 'edit_mask': [{'row': None, 'col': 0, 'editable': False}, {'row': None, 'col': 1, 'editable': False}, {'row': 0, 'col': None, 'editable': False}, {'row': None, 'col': 3, 'type': 'color'}, {'row': None, 'col': 2, 'type': 'number', 'min': 0, 'max': None}, {'row': 0, 'col': None, 'type': 'text'}, {'row': 0, 'col': 2, 'editable': True}], 'contents': [region_name, 'Population', 'User Data', 'Colour']}

        for row in csv_reader:

            if len(row) < (max(name_column, data_column, population_column, color_column) + 1):
                raise ValueError('Invalid CSV File')

            if first_row:
                first_row = False
                tooltip['label'] = row[data_column]
                grid_document['contents'][2] = row[data_column]
                continue

            #if name_column not in row or data_column not in row or color_column not in row:
            #    raise ValueError('Invalid CSV file.')           

            result[order.index(row[name_column])] = row[data_column].strip()

            try:
                result[order.index(row[name_column])] = float(result[order.index(row[name_column])])
                tooltip['data']['id_{}'.format(id_data[row[name_column]])] = {'name': row[name_column], 'value': float(row[data_column])}
            except ValueError:
                if row[data_column].strip() != "NA":
                    raise ValueError("Value must be number or 'NA'")
                
                tooltip['data']['id_{}'.format(id_data[row[name_column]])] = {'name': row[name_column], 'value': "NA"}

            color_values['id_{}'.format(id_data[row[name_column]])] = row[color_column]
            

            grid_document['contents'].extend([row[name_column], row[population_column], row[data_column], row[color_column]])
        
        areas_string = ""

        for area in result:
            areas_string += "{};".format(area)
        
        return areas_string.rstrip(';'), color_values, tooltip, grid_document


    
