import pytest

from src.vacancies import VacancyParser


@pytest.fixture
def raw_vacancies():
    """Пример сырых данных от API hh.ru"""
    return [
        {
            "name": "Python Developer",
            "salary": {"from": 100000, "to": 150000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/1",
            "employer": {"name": "Яндекс"},
        },
        {
            "name": "Backend Engineer",
            "salary": {"from": 120000, "to": 180000, "currency": "RUR"},
            "alternate_url": "https://hh.ru/vacancy/2",
            "employer": "Tinkoff",
        },
        {
            "name": "Junior Python Developer",
            "salary": None,
            "alternate_url": "https://hh.ru/vacancy/3",
            "employer": None,
        },
    ]


def test_parse_vacancies_returns_correct_structure(raw_vacancies):
    """Проверяет, что метод возвращает список словарей с нужными ключами"""
    parsed = VacancyParser.parse_vacancies(raw_vacancies)

    assert isinstance(parsed, list)
    assert len(parsed) == 3

    expected_keys = {
        "company_name",
        "vacancy_name",
        "salary_from",
        "salary_to",
        "currency",
        "vacancy_url",
    }

    for v in parsed:
        assert set(v.keys()) == expected_keys


def test_parse_vacancies_handles_employer_types(raw_vacancies):
    """Проверяет обработку employer в виде dict, str и None"""
    parsed = VacancyParser.parse_vacancies(raw_vacancies)

    assert parsed[0]["company_name"] == "Яндекс"  # dict
    assert parsed[1]["company_name"] == "Tinkoff"  # str
    assert parsed[2]["company_name"] == "Unknown"  # None


def test_parse_vacancies_handles_missing_salary(raw_vacancies):
    """Проверяет корректность работы при отсутствии данных о зарплате"""
    parsed = VacancyParser.parse_vacancies(raw_vacancies)
    last = parsed[2]

    assert last["salary_from"] is None
    assert last["salary_to"] is None
    assert last["currency"] is None


def test_extract_companies_returns_unique_list():
    """Проверяет, что список компаний уникализируется и очищается"""
    parsed = [
        {"company_name": "Яндекс"},
        {"company_name": "Tinkoff"},
        {"company_name": "Tinkoff "},  # с пробелом
        {"company_name": " "},  # пустая строка
        {"company_name": None},
    ]

    result = VacancyParser.extract_companies(parsed)
    assert sorted(result) == ["Tinkoff", "Яндекс"]
    assert len(result) == 2


def test_extract_companies_ignores_non_dicts():
    """Проверяет, что функция игнорирует элементы, не являющиеся dict"""
    parsed = [
        {"company_name": "Ozon"},
        "Not a dict",
        123,
        None,
    ]

    result = VacancyParser.extract_companies(parsed)
    assert result == ["Ozon"]
