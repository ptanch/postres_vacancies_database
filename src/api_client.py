import os

import requests
from dotenv import load_dotenv

load_dotenv()


class HeadHunterAPI:
    """
    Класс для работы с API hh.ru.
    Позволяет искать вакансии по названию компаний.
    """

    BASE_URL = "https://api.hh.ru/vacancies"

    def __init__(self, token: str = None):
        self.token = token or os.getenv("HH_TOKEN")
        self.headers = {"User-Agent": "hh_jobs_project"}
        if self.token:
            self.headers["Authorization"] = f"Bearer {self.token}"

    def fetch_vacancies(
        self, company_name: str, keyword: str = "Python", per_page: int = 50, pages: int = 1
    ) -> list:
        """
        Получает список вакансий по ключевому слову и названию компании.
        Пример: text="company_name:(Tinkoff) AND Python"
        """
        all_vacancies = []
        for page in range(pages):
            params = {
                "text": f"company_name:({company_name}) AND {keyword}",
                "per_page": per_page,
                "page": page,
                "only_with_salary": True,
            }

            response = requests.get(self.BASE_URL, headers=self.headers, params=params)
            response.raise_for_status()

            data = response.json()
            items = data.get("items", [])
            if not items:
                break

            all_vacancies.extend(items)

        return all_vacancies
