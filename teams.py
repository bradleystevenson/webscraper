from table import ObjectTable

class Teams:


    def __init__(self, create_from_web, franchises, leagues):
        self.teams_table = ObjectTable('teams', ['franchise_id', 'year', 'team_url', 'league_year_id', 'team_id'], 'team_id')

        if create_from_web:
            pass
        else:
            self.teams_table.create_from_table()


    def insert_data(self):
        self.teams_table.insert_data()