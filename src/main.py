from bd.base import DataBase
from methods.http import Parse

import asyncio

import json


def read_json_config(file_path="config.json"):
    """Чтение конфигурации из JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        exit(1)
    except json.JSONDecodeError:
        print(f"Ошибка в формате файла {file_path}")
        exit(1)

async def main():
    
    config = read_json_config()

    search = config.get("search", "")
    search = search.replace(" ", "+")
    search = "&text="+search

    filter_experience = config.get("filter_experience", 1)
    match filter_experience:
        case 2:
            filter_experience = "&experience=noExperience"
        case 3:
            filter_experience = "&experience=between1And3"
        case 4:
            filter_experience = "&experience=between3And6"
        case 5:
            filter_experience = "&experience=moreThan6"
        case _:
            filter_experience = ""

    start_url = config.get("url", "https://hh.ru/search/vacancy")

    url = start_url + search + filter_experience

    parser = Parse(url)
    db = DataBase()

    try:
        vacs = await parser.get_all_vacancies(10,4)
    except Exception as e:
        print(f"Something went wrong: {e}")

    
    db.create_table()
    db.write_table(vacs)

asyncio.run(main())


