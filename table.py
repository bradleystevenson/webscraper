import database_connection
from database_connection import DatabaseConnection

class Table:

    def __init__(self, table_name, table_columns):
        self.table_name = table_name
        self.table_columns = table_columns
        self.data = []

    def append(self, new_row):
        print("APPENDING NEW ROW FINALLY")
        print(new_row)
        self.data.append(new_row)
        print(self.data)
    def create_table(self):
        execution_string = 'CREATE TABLE ' + self.table_name + ' ('
        for table_column in self.table_columns:
            execution_string += table_column + ', '
        execution_string = execution_string[:-2] + ')'
        database_connection.get_database_connection().execute(execution_string)

    def insert_data(self):
        insert_string = 'INSERT INTO ' + self.table_name + ' ('
        for table_column in self.table_columns:
            insert_string += table_column + ', '
        insert_string = insert_string[:-2] + ') VALUES '
        for row in self.data:
            row_string = "("
            for table_column in self.table_columns:
                if isinstance(row[table_column], int):
                    row_string += str(row[table_column])
                else:
                    row_string += '"' + row[table_column] + '"'
                row_string += ', '
            row_string = row_string[:-2] + ')'
            insert_string += row_string + ', '
        insert_string = insert_string[:-2]
        database_connection.get_database_connection().execute(insert_string)

class ObjectTable(Table):

    def __init__(self, table_name, table_columns, primary_key):
        super().__init__(table_name, table_columns)
        self.primary_key = primary_key
        self.max_id = 1

    def append(self, new_row):
        print("APPEND NEW_ROW")
        print(new_row)
        print(self.data)
        new_row[self.primary_key] = self.max_id
        super().append(new_row)
        self.max_id += 1

    def get_primary_key_by_column_search(self, column_name, column_value):
        for row in self.data:
            if row[column_name] == column_value:
                return row[self.primary_key]