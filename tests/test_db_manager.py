import pytest
from unittest.mock import patch, MagicMock
from src.db_manager import DBManager


@pytest.fixture
def db_manager():
    """Фикстура с тестовым экземпляром DBManager."""
    return DBManager(db_name="test_db")


#     ТЕСТЫ НА SELECT-ЗАПРОСЫ

@patch("psycopg2.connect")
def test_execute_query_returns_data(mock_connect, db_manager):
    """Проверяет, что _execute_query возвращает корректные данные."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [("Яндекс", 5)]
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    result = db_manager._execute_query("SELECT * FROM test;")

    assert result == [("Яндекс", 5)]
    mock_cursor.execute.assert_called_once()


@patch("psycopg2.connect")
def test_execute_query_handles_exception(mock_connect, db_manager):
    """Проверяет, что при ошибке подключения возвращается пустой список."""
    mock_connect.side_effect = Exception("Connection error")
    result = db_manager._execute_query("SELECT * FROM test;")
    assert result == []


@patch.object(DBManager, "_execute_query")
def test_get_companies_and_vacancies_count(mock_exec, db_manager):
    mock_exec.return_value = [("Tinkoff", 10)]
    result = db_manager.get_companies_and_vacancies_count()

    assert result == [("Tinkoff", 10)]
    mock_exec.assert_called_once()
    assert "SELECT" in mock_exec.call_args[0][0]


@patch.object(DBManager, "_execute_query")
def test_get_all_vacancies(mock_exec, db_manager):
    mock_exec.return_value = [("Яндекс", "Python Dev", 100000, 150000, "RUR", "url")]
    result = db_manager.get_all_vacancies()

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0][0] == "Яндекс"


@patch.object(DBManager, "_execute_query")
def test_get_avg_salary(mock_exec, db_manager):
    mock_exec.return_value = [(120000.0,)]
    assert db_manager.get_avg_salary() == 120000.0

    mock_exec.return_value = []
    assert db_manager.get_avg_salary() == 0.0


@patch.object(DBManager, "_execute_query")
@patch.object(DBManager, "get_avg_salary")
def test_get_vacancies_with_higher_salary(mock_avg, mock_exec, db_manager):
    mock_avg.return_value = 100000
    mock_exec.return_value = [("Ozon", "Python Dev", 150000.0, "url")]

    result = db_manager.get_vacancies_with_higher_salary()
    assert result == [("Ozon", "Python Dev", 150000.0, "url")]
    mock_exec.assert_called_once()


@patch.object(DBManager, "_execute_query")
def test_get_vacancies_with_keyword(mock_exec, db_manager):
    mock_exec.return_value = [("Сбер", "Python Engineer", "url")]
    result = db_manager.get_vacancies_with_keyword("python")

    assert len(result) == 1
    assert "python" in mock_exec.call_args[0][1][0].lower()


#     ТЕСТЫ НА INSERT

@patch("psycopg2.connect")
def test_insert_companies_calls_execute(mock_connect, db_manager):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    db_manager.insert_companies(["Яндекс", "Ozon"])
    assert mock_cursor.execute.call_count == 2


@patch("psycopg2.connect")
def test_insert_vacancies_calls_execute(mock_connect, db_manager):
    mock_cursor = MagicMock()
    mock_connect.return_value.__enter__.return_value.cursor.return_value.__enter__.return_value = mock_cursor

    vacancies = [
        {
            "company_name": "Tinkoff",
            "vacancy_name": "Backend Dev",
            "salary_from": 100000,
            "salary_to": 150000,
            "currency": "RUR",
            "vacancy_url": "url1",
        }
    ]

    db_manager.insert_vacancies(vacancies)
    mock_cursor.execute.assert_called_once()
    assert "INSERT INTO vacancies" in mock_cursor.execute.call_args[0][0]
