from bs4 import BeautifulSoup
from .base import VacData
import asyncio
import aiohttp

class Parse:

    def __init__(self, url):
        self.base_url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        }
        self.is_first_page = 1
        self.parse_vacs = 0
    
    async def get_page_http(self, session, url):
        try:
            async with session.get(url, headers=self.headers, timeout=10) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    print(f"Status {response.status} for {url}")
                    return None
        except Exception as e:
            print(f"Error {e} while getting html of page: {url}")
            

    async def data_from_vac(self, session, url):
        http = await self.get_page_http(session, url)

        try:
            soup = BeautifulSoup(http, 'html.parser')
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
            company_name = soup.find("a", {"data-qa": "vacancy-company-name"}).text

            resp = soup.find('div', {"class":"noprint"}).text
            resp_number = ''.join(filter(str.isdigit, resp))
            resp_number = "1" if len(resp_number) == 0 else resp_number

            format_work = "Не указан" if format_work == None else format_work.text[len(s2): ]

            res = VacData(url, title, wage, exp, common_empl, work_hours, format_work, resp_number, work_schedule, company_name)
        
        except Exception as e:
            print(f"Error {e} while parsing page {url}")

        return res

        
    async def get_all_vacancies_on_page(self, session, url, num_vacancies):
        
        try:
            http = await self.get_page_http(session, url)

            vacs = []
            tasks = []
            
            soup = BeautifulSoup(http, 'html.parser')
            vacs_soup = soup.find_all("div", {"class":"magritte-redesign"})
            
            if self.is_first_page:
                all_vacs = soup.find("div", {"data-qa":"title-container"}).text
                print(f"{all_vacs}")
                num_all_vacs = ''.join(filter(str.isdigit, all_vacs))
                self.parse_vacs = min(self.parse_vacs, int(num_all_vacs))
                self.is_first_page = 0
            
            for vac in vacs_soup[1:num_vacancies+1]:
                vac_ref = vac.find("a", {"data-qa" : "serp-item__title"}).attrs['href']
                task = asyncio.create_task(
                    self.data_from_vac(session, vac_ref)
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                vacs.append(result)
        except Exception as e:
            print(f"Error {e} while parsing main page: {url}")
        
        return vacs
        
    async def get_all_vacancies(self, num_vacancies = 10, concurrent_requests = 1):
        self.parse_vacs = num_vacancies

        connector = aiohttp.TCPConnector(limit=concurrent_requests)
        timeout = aiohttp.ClientTimeout(total=30)

        vacs = []
        parsed = 0
        page_num = 0
        
        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            while len(vacs) < self.parse_vacs:
                page_vacs = await self.get_all_vacancies_on_page(session, self.base_url + f"&page={page_num}", self.parse_vacs - parsed)
                
                for vac in page_vacs:
                    vacs.append(vac)
                
                page_num += 1
                parsed += len(page_vacs)

        return vacs
