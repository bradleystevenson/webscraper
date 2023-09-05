import sqlite3



def  get_database_connection():
    return DatabaseConnection()


class DatabaseConnection:

    def __init__(self):
        self.conn = sqlite3.connect("/Users/administrator/Programs/football_grid_trainer/database.db")

    def execute(self, statement):
        self.conn.execute(statement)
        self.conn.commit()

    def select_statement(self, table_name, table_columns):
        cursor = self.conn.cursor()
        cursor.execute(self._build_select_statement(table_name, table_columns))
        records = cursor.fetchall()
        return_array = []
        for record in records:
            new_dict = {}
            inx = 0
            for table_column in table_columns:
                new_dict[table_column] = record[inx]
                inx += 1
            return_array.append(new_dict)
        return return_array

    def delete_from_table(self, table_name):
        execution_string = 'DELETE FROM ' + table_name
        self.conn.execute(execution_string)
        self.conn.commit()

    def _build_select_statement(self, table_name, table_columns):
        execution_string = 'SELECT '
        for table_column in table_columns:
            execution_string += table_column + ', '
        return execution_string[:-2] + ' FROM ' + table_name
