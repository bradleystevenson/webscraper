import sqlite3



def  get_database_connection():
    return DatabaseConnection()


class DatabaseConnection:

    def __init__(self):
        self.conn = sqlite3.connect("/Users/administrator/Programs/football_grid_trainer/database.db")

    def execute(self, statement):
        print(statement)
        self.conn.execute(statement)
        self.conn.commit()