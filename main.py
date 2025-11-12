from src.api_client import HeadHunterAPI
from src.vacancies import VacancyParser
from src.db_manager import DBManager
from src.file_utils import FileManager
from src.db_setup import create_tables

import os
from dotenv import load_dotenv

db_name = "hh_vacancies_db"


def main():
    #  Создание таблиц в базе
    try:
        create_tables(db_name)
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")

    #  Загрузка вакансий с hh.ru
    print("\nЗагружаем вакансии с hh.ru...")
    api = HeadHunterAPI()
    keyword = "Python"

    #  Загрузка компании из .env
    load_dotenv()
    companies_str = os.getenv("COMPANIES", "")
    companies = [c.strip() for c in companies_str.split(",") if c.strip()]

    if not companies:
        print("Не удалось загрузить список компаний из .env.")
        return

    all_vacancies = []
    for company in companies:
        print(f"Обрабатываем компанию: {company}")
        try:
            company_vacancies = api.fetch_vacancies(company_name=company, keyword=keyword, per_page=50, pages=2)
            all_vacancies.extend(company_vacancies)
            print(f"Найдено {len(company_vacancies)} вакансий")
        except Exception as e:
            print(f"Ошибка при загрузке вакансий для {company}: {e}")

    print(f"\nВсего найдено {len(all_vacancies)} вакансий по {len(companies)} компаниям")

    if not all_vacancies:
        print("Не удалось найти вакансии по запросу.")
        return

    #  Сохранение вакансии в JSON
    FileManager.save_to_json({"vacancies": all_vacancies}, "vacancies.json")
    print("Вакансии сохранены в файл vacancies.json")

    #  Загрузка данных из JSON
    loaded_data = FileManager.load_from_json("vacancies.json")
    loaded_vacancies = loaded_data.get("vacancies", [])

    if not loaded_vacancies:
        print("Файл vacancies.json пуст или не содержит данных.")
        return

    #  Парсинг и обработка вакансий
    parser = VacancyParser(loaded_vacancies)
    parsed_vacancies = parser.parse_vacancies(parser.raw_vacancies)
    companies_data = parser.extract_companies(parsed_vacancies)

    #  Работа с базой данных
    db = DBManager(db_name)
    db.insert_companies(companies_data)
    db.insert_vacancies(parsed_vacancies)

    print("\nДанные успешно загружены в базу!")


if __name__ == "__main__":
    main()
