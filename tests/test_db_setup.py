import pytest
from unittest.mock import patch, MagicMock
from src import db_setup


@pytest.fixture
def mock_connect():
    """Создает мок для psycopg2.connect, который подходит для обоих случаев"""
    with patch("src.db_setup.psycopg2.connect") as mock_conn:
        conn = MagicMock()
        cursor = MagicMock()
        # Поведение курсора и для обычного вызова, и для контекстного менеджера
        conn.cursor.return_value = cursor
        conn.cursor.return_value.__enter__.return_value = cursor
        mock_conn.return_value = conn
        yield mock_conn, conn, cursor


def test_create_database_creates_new_db(mock_connect, capsys):
    mock_conn, conn, cursor = mock_connect
    cursor.fetchone.return_value = None  # базы нет

    db_setup.create_database("test_db")

    # Проверяем, что запрос SELECT выполнялся
    executed_queries = [call[0][0] for call in cursor.execute.call_args_list]
    assert any("SELECT 1 FROM pg_database" in q for q in executed_queries)
    assert any("CREATE DATABASE test_db" in q for q in executed_queries)

    captured = capsys.readouterr()
    assert "успешно создана" in captured.out


def test_create_database_already_exists(mock_connect, capsys):
    mock_conn, conn, cursor = mock_connect
    cursor.fetchone.return_value = (1,)  # база уже есть

    db_setup.create_database("test_db")

    executed_queries = [call[0][0] for call in cursor.execute.call_args_list]
    assert any("SELECT 1 FROM pg_database" in q for q in executed_queries)
    # CREATE DATABASE не должен выполняться
    assert not any("CREATE DATABASE test_db" in q for q in executed_queries)

    captured = capsys.readouterr()
    assert "уже существует" in captured.out


def test_create_database_handles_exception(mock_connect, capsys):
    mock_conn, conn, cursor = mock_connect
    mock_conn.side_effect = Exception("connection error")

    db_setup.create_database("test_db")

    captured = capsys.readouterr()
    assert "Ошибка при создании базы данных" in captured.out


def test_create_tables_exception(mock_connect, capsys):
    mock_conn, conn, cursor = mock_connect
    mock_conn.side_effect = Exception("connection error")

    db_setup.create_tables("test_db")

    captured = capsys.readouterr()
    assert "Ошибка при создании таблиц" in captured.out
