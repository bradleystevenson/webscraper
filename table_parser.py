class TableParser:

    def __init__(self, table, valid_row_function, data_dict_from_object):
        self.data = []
        for table_row in table.find("tbody").find_all("tr"):
            if valid_row_function(table_row):
                self.data.append(data_dict_from_object.parse(table_row))