
class BaseCartogramHandler:

    def get_gen_file(self):
        raise NotImplementedError("This function must be implemented.")
    
    def validate_values(self, values):
        raise NotImplementedError("This function must be implemented.")
    
    def gen_area_data(self, values):
        raise NotImplementedError("This function must be implemented.")
    
