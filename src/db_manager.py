import psycopg2
import os
from typing import List, Tuple, Any
from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """
    Класс для работы с базой данных PostgreSQL.
    Содержит методы получения данных о компаниях и вакансиях.
    """

    def __init__(self, db_name: str):
        self.db_name = db_name
        self.params = {
            "dbname": db_name,
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
        }

    def _execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """
        Универсальный метод для выполнения SQL-запросов SELECT.
        Возвращает результат в виде списка кортежей.
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    cur.execute(query, params)
                    return cur.fetchall()
        except Exception as e:
            print(f"Ошибка выполнения запроса: {e}")
            return []

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получает список всех компаний и количество вакансий у каждой компании.
        """
        query = """
        SELECT c.company_name, COUNT(v.vacancy_id) AS vacancies_count
        FROM companies c
        LEFT JOIN vacancies v ON c.company_id = v.company_id
        GROUP BY c.company_name
        ORDER BY vacancies_count DESC;
        """
        return self._execute_query(query)

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str, str]]:
        """
        Получает список всех вакансий с указанием:
        - названия компании
        - названия вакансии
        - диапазона зарплат
        - валюты
        - ссылки на вакансию
        """
        query = """
        SELECT c.company_name, v.vacancy_name, v.salary_from, v.salary_to, v.currency, v.vacancy_url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        ORDER BY c.company_name;
        """
        return self._execute_query(query)

    def get_avg_salary(self) -> float:
        """
        Получает среднюю зарплату по всем вакансиям.
        """
        query = """
        SELECT AVG((COALESCE(salary_from, 0) + COALESCE(salary_to, 0)) / 2.0)
        FROM vacancies
        WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
        """
        result = self._execute_query(query)
        return result[0][0] if result and result[0][0] is not None else 0.0

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, float, str]]:
        """
        Получает список вакансий, у которых средняя зарплата выше средней по всем вакансиям.
        """
        avg_salary = self.get_avg_salary()
        query = """
        SELECT c.company_name,
               v.vacancy_name,
               (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2.0 AS avg_vac_salary,
               v.vacancy_url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        WHERE (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2.0 > %s
        ORDER BY avg_vac_salary DESC;
        """
        return self._execute_query(query, (avg_salary,))

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, str]]:
        """
        Получает список всех вакансий, в названии которых содержится переданное слово.
        Например, keyword='python'
        """
        query = """
        SELECT c.company_name, v.vacancy_name, v.vacancy_url
        FROM vacancies v
        JOIN companies c ON v.company_id = c.company_id
        WHERE LOWER(v.vacancy_name) LIKE LOWER(%s)
        ORDER BY c.company_name;
        """
        return self._execute_query(query, (f"%{keyword}%",))

    def insert_companies(self, companies: list):
        """
        Вставляет список компаний в таблицу companies.
        :param companies: список названий компаний
        """
        query = "INSERT INTO companies (company_name) VALUES (%s) ON CONFLICT (company_name) DO NOTHING;"
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    for company in companies:
                        cur.execute(query, (company,))
                conn.commit()
        except Exception as e:
            print(f"Ошибка вставки компаний: {e}")

    def insert_vacancies(self, vacancies: list):
        """
        Вставляет список вакансий в таблицу vacancies.
        :param vacancies: список словарей с ключами:
            company_name, vacancy_name, salary_from, salary_to, currency, vacancy_url
        """
        query = """
        INSERT INTO vacancies (company_id, vacancy_name, salary_from, salary_to, currency, vacancy_url)
        VALUES ((SELECT company_id FROM companies WHERE company_name=%s), %s, %s, %s, %s, %s)
        ON CONFLICT (vacancy_url) DO NOTHING;
        """
        try:
            with psycopg2.connect(**self.params) as conn:
                with conn.cursor() as cur:
                    for vac in vacancies:
                        cur.execute(query, (
                            vac["company_name"],
                            vac["vacancy_name"],
                            vac.get("salary_from"),
                            vac.get("salary_to"),
                            vac.get("currency"),
                            vac.get("vacancy_url"),
                        ))
                conn.commit()
        except Exception as e:
            print(f"Ошибка вставки вакансий: {e}")
