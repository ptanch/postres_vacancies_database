import psycopg2
import os
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv

load_dotenv()


def create_database(db_name: str) -> None:
    """
    Создаёт новую базу данных PostgreSQL, если она ещё не существует.
    """
    params = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
    }

    try:
        # Подключение к postgres (основной БД)
        conn = psycopg2.connect(dbname="postgres", **params)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Проверка, есть ли база данных
        cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}';")
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {db_name};")
            print(f"База данных '{db_name}' успешно создана.")
        else:
            print(f"База данных '{db_name}' уже существует.")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"Ошибка при создании базы данных: {e}")


def create_tables(db_name: str) -> None:
    """
    Создаёт таблицы 'companies' и 'vacancies' в указанной базе данных.
    """
    params = {
        "dbname": db_name,
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
    }

    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                sql_script = """
                CREATE TABLE IF NOT EXISTS employers (
                    employer_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                );
                    
                CREATE TABLE IF NOT EXISTS vacancies (
                    vacancy_id SERIAL PRIMARY KEY,
                    title VARCHAR(255) NOT NULL,
                    salary INTEGER,
                    currency VARCHAR(10),
                    url TEXT,
                    employer_id INTEGER REFERENCES employers(employer_id)
                );
                """

                safe_sql = sql_script.encode("utf-8", errors="ignore").decode("utf-8")

                cur.execute(safe_sql)
                conn.commit()
                print("Таблицы успешно созданы.")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
