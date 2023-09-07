class DataDictFromObject:


    def __init__(self, fields_function_dict):
        self.fields_function_dict = fields_function_dict

    def parse(self, object):
        data = {}
        for field in self.fields_function_dict.keys():
            data[field] = self.fields_function_dict[field](object)
        return data