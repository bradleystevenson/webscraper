import database_connection
from database_connection import DatabaseConnection
import sqlite3

class Table:

    def __init__(self, table_name, table_columns):
        self.table_name = table_name
        self.table_columns = table_columns
        self.data = []

    def create_from_table(self):
        self.data = database_connection.get_database_connection().select_statement(self.table_name, self.table_columns)



    def append(self, new_row):
        self.data.append(new_row)

    def create_table(self):
        execution_string = 'CREATE TABLE ' + self.table_name + ' ('
        for table_column in self.table_columns:
            execution_string += table_column + ', '
        execution_string = execution_string[:-2] + ')'
        database_connection.get_database_connection().execute(execution_string)

    def insert_data(self):
        try:
            self.create_table()
        except sqlite3.OperationalError:
            print("Cant create table, already exist yet")
        try:
            database_connection.get_database_connection().delete_from_table(self.table_name)
        except sqlite3.OperationalError:
            print("Cant delete table, doesnt exist yet")
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
        new_row[self.primary_key] = self.max_id
        super().append(new_row)
        self.max_id += 1

    def get_primary_key_by_column_search(self, column_name, column_value):
        for row in self.data:
            if row[column_name] == column_value:
                return row[self.primary_key]
        raise Exception("No match for column value")

    def get_primary_key_by_columns_search(self, search_dict):
        for row in self.data:
            if self._is_match(row, search_dict):
                return row[self.primary_key]
        print(search_dict)
        raise Exception("No Match for " + str(search_dict))


    def _is_match(self, row, search_dict):
        for key in search_dict.keys():
            if row[key] != search_dict[key]:
                return False
        return True
