class DataDictFromObject:


    def __init__(self, fields_function_dict, hardcoded_dict=None):
        self.fields_function_dict = fields_function_dict
        self.hardcoded_dict = hardcoded_dict

    def parse(self, object):
        data = {}
        for field in self.fields_function_dict.keys():
            data[field] = self.fields_function_dict[field](object)
        if self.hardcoded_dict is not None:
            for field in self.hardcoded_dict.keys():
                data[field] = self.hardcoded_dict[field]
        return data