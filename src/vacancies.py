from typing import Dict, List, Any


class VacancyParser:
    """
    Класс для обработки данных о вакансиях, полученных с hh.ru.
    """
    def __init__(self, vacancies: list):
        """
        :param vacancies: список вакансий, полученных из API или JSON
        """
        self.raw_vacancies = vacancies

    @staticmethod
    def parse_vacancies(raw_data: list) -> List[Dict[str, Any]]:
        """
        Преобразует список вакансий (от API) в удобный для записи в БД формат.
        :param raw_data: список словарей с вакансиями
        :return: список словарей с унифицированными данными по вакансиям
        """
        parsed_vacancies = []

        for item in raw_data:
            salary_info = item.get("salary") or {}
            # employer может быть dict или строкой или None
            employer = item.get("employer")
            if isinstance(employer, dict):
                company_name = employer.get("name") or "Unknown"
            elif isinstance(employer, str):
                company_name = employer
            else:
                # иногда employer может быть None
                company_name = "Unknown"

            parsed_vacancies.append({
                "company_name": company_name,
                "vacancy_name": item.get("name"),
                "salary_from": salary_info.get("from"),
                "salary_to": salary_info.get("to"),
                "currency": salary_info.get("currency"),
                "vacancy_url": item.get("alternate_url"),
            })

        return parsed_vacancies

    @staticmethod
    def extract_companies(parsed_vacancies: List[Dict[str, Any]]) -> List[str]:
        """
        Извлекает список уникальных компаний из данных о вакансиях.
        :param parsed_vacancies: список словарей с вакансиями
        :return: список уникальных названий компаний
        """
        companies = set()
        for v in parsed_vacancies:
            if not isinstance(v, dict):
                continue
            name = v.get("company_name")
            if isinstance(name, str) and name.strip():
                companies.add(name.strip())
        return list(companies)
