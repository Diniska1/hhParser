from bd.base import DataBase
from methods.http import Parse

import asyncio

async def main():
    

    search = "Ml engineer"
    search = search.replace(" ", "+")
    search = "&text="+search

    filter_experience = \
    ""
    # "&experience=noExperience"
    # "&experience=between3And6"
    # "&experience=between1And3"
    # "&experience=between3And6"
    # "&experience=moreThan6"


    url = 'https://hh.ru/search/vacancy?from=suggest_post&clickedSuggestId=b79c31ab-471f-4a35-95e9-a7fe296deb98&area=1&hhtmFrom=main&hhtmFromLabel=vacancy_search_line' + search + filter_experience
    # print(url)

    parser = Parse(url)
    db = DataBase()

    try:
        vacs = await parser.get_all_vacancies(10,4)
    except Exception as e:
        print(f"Something went wrong: {e}")

    
    db.create_table()
    db.write_table(vacs)

asyncio.run(main())


