import requests
from bs4 import BeautifulSoup
from .base import VacData

class Parse:

    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }

    def data_from_vac(self, url):
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            s1 = "Опыт работы: "
            s2 = "Формат работы: "
            s3 = "Рабочие часы: "
            s5 = "График: "

            title_and_wage = soup.find('div', {'class': "vacancy-title"}).text
            title = soup.find('h1', {'data-qa': "vacancy-title"}).text
            wage = title_and_wage[len(title):]
            
            exp = soup.find('p', {"data-qa": "work-experience-text"}).text[len(s1):]
            common_empl = soup.find("div", {"data-qa":"common-employment-text"}).text
            work_hours = soup.find('div', {"data-qa":"working-hours-text"}).text[len(s3):]
            format_work = soup.find('p', {"data-qa":"work-formats-text"})
            work_schedule = soup.find("p", {"data-qa":"work-schedule-by-days-text"}).text[len(s5):]

            resp = soup.find('div', {"class":"noprint"}).text
            resp_number = ''.join(filter(str.isdigit, resp))

        format_work = "Не указан" if format_work == None else format_work.text[len(s2): ]

        res = VacData(url, title, wage, exp, common_empl, work_hours, format_work, resp_number, work_schedule)

        return res

        
    def get_all_vacancies(self, url, search, filter_experience, num_vacancies = 10):

        response = requests.get(url, headers=self.headers)

        vacs = []
        if response.status_code == 200:

            soup = BeautifulSoup(response.text, 'html.parser')
            vacs_soup = soup.find_all("div", {"class":"magritte-redesign"})

            for vac in vacs_soup[1:num_vacancies]:
                vac_ref = vac.find("a", {"data-qa" : "serp-item__title"}).attrs['href']
                vacs.append(self.data_from_vac(vac_ref))
        else:
            print("ERROR: response.status_code != 200")
            exit(1)
        
        return vacs