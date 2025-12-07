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
        company_name TEXT NOT NULL,
        exp TEXT,
        wage TEXT,
        resp_number INTEGER, 
        common_empl TEXT,
        work_hours TEXT,
        format_work TEXT,
        work_schedule TEXT,
        url TEXT NOT NULL
        );
        ''')

    def write_table(self, vacs):
    
        query = 'INSERT INTO Vacancies (url, title, wage, exp, common_empl, work_hours, format_work, resp_number, work_schedule, company_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

        for vac in vacs:
            self.cursor.execute(query, (vac.url, vac.title,vac.wage,vac.exp,vac.common_empl,vac.work_hours,vac.format_work, vac.resp_number, vac.work_schedule, vac.company_name) )

        self.connection.commit()
        self.connection.close()