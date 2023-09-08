class Object:

    def __init__(self, create_from_web, tables):
        self.tables = tables
        if create_from_web:
            self._create_from_web()
        else:
            for table in tables:
                table.create_from_table()

    def _create_from_web(self):
        pass

    def insert_data(self):
        for table in self.tables:
            table.insert_data()
