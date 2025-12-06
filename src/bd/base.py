import sqlite3

class DataBase():
    def __init__(self, name = "Vacancies.db"):
        self.connection = sqlite3.connect(name)
        self.cursor = self.connection.cursor()

    def create_table(self):
        self.cursor.execute('DROP TABLE IF EXISTS Vacancies;')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS Vacancies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        url TEXT NOT NULL,
        exp TEXT,
        common_empl TEXT,
        wage TEXT,
        work_hours TEXT,
        format_work TEXT,
        work_schedule TEXT,
        resp_number INTEGER
        );
        ''')

    def write_table(self, vacs):
    
        query = 'INSERT INTO Vacancies (url, title, wage, exp, common_empl, work_hours, format_work, resp_number, work_schedule) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'

        for vac in vacs:
            self.cursor.execute(query, (vac.url, vac.title,vac.wage,vac.exp,vac.common_empl,vac.work_hours,vac.format_work, vac.resp_number, vac.work_schedule) )

        self.connection.commit()
        self.connection.close()