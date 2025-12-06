import sqlite3
import matplotlib.pyplot as plt

def show_graphs():
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
        resp.append(vac[9])
        form.append(vac[7])
        wage.append(vac[5])
    print(wage)

    plt.hist(resp)
    plt.show()

    connection.close()