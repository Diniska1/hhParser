import sqlite3
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

class Graphs():
    def get_sql_info(self):
        connection = sqlite3.connect('Vacancies.db')
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM Vacancies')
        vacs = cursor.fetchall()

        exp = []
        wage = []
        resp = []
        form = []

        for vac in vacs:
            exp.append(vac[3])
            resp.append(vac[5])
            form.append(vac[8])
            wage.append(vac[4])

        connection.close()

        return exp, wage, resp, form
    
    def make_and_save_graph(self, array, graph_type, filename = "Graphs/unknown.png", xlabel_name = "", ylabel_name = ""):
        
        fig, ax = plt.subplots(figsize=(15, 9))
        ax.hist(array)

        ax.set_xlabel(xlabel_name)
        ax.set_ylabel(ylabel_name)

        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))

        plt.savefig(filename)
        plt.clf() 
    

    def make_graphs(self):
        exp, wage, resp, form = self.get_sql_info()
        
        self.make_and_save_graph(exp, plt.hist, "Graphs/Experience.png", "Количество опыта", "Количество вакансий")
        self.make_and_save_graph(resp, plt.hist, "Graphs/Responces.png", "Количество людей, смотрящих вакансию", "Количество вакансий")
        self.make_and_save_graph(form, plt.hist, "Graphs/Working Format.png", "Формат работы", "Количество вакансий")

        