from bd.base import DataBase
from methods.http import Parse

parser = Parse()
db = DataBase()

search = "Ml engineer"
search = search.replace(" ", "+")
search = "&text="+search

filter_experience = \
""
# "&experience=between3And6"
# "&experience=noExperience"
# "&experience=between1And3"
# "&experience=between3And6"
# "&experience=moreThan6"


url = 'https://hh.ru/search/vacancy?from=suggest_post&clickedSuggestId=b79c31ab-471f-4a35-95e9-a7fe296deb98&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line' + search + filter_experience


vacs = parser.get_all_vacancies(url, search, filter_experience, 15)
db.create_table()
db.write_table(vacs)


