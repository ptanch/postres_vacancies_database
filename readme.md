# 💼 HeadHunter Vacancies Database

Этот проект предназначен для сбора, хранения и анализа вакансий с сайта [hh.ru](https://hh.ru).  
Данные автоматически загружаются через API hh.ru, сохраняются в базу данных PostgreSQL и могут быть экспортированы в JSON и TXT файлы.

---

## 🚀 Основные возможности

- Подключение к API HeadHunter и загрузка вакансий по ключевым словам и компаниям  
- Создание базы данных PostgreSQL и таблиц для работодателей и вакансий  
- Сохранение данных в JSON и TXT файлы  
- Выполнение SQL-запросов для анализа данных  
- Тестовое покрытие ключевых модулей проекта с помощью `pytest`

---

## 🧱 Структура проекта
```commandline
project_root/
├── src/
│ ├── api.py # Работа с API hh.ru
│ ├── db_manager.py # Класс для работы с PostgreSQL
│ ├── db_setup.py # Создание базы и таблиц
│ ├── file_utils.py # Сохранение и загрузка JSON/TXT файлов
│ └── vacancies.py # Обработка данных о вакансиях
│
├── tests/ # Unit-тесты для каждого модуля
│ ├── test_api.py
│ ├── test_db_manager.py
│ ├── test_db_setup.py
│ ├── test_file_utils.py
│ └── test_vacancies.py
│
├── pyproject.toml # Конфигурация Poetry
├── poetry.lock
├── .gitignore
├── .env.example # Пример файла с переменными окружения
├── main.py # Точка входа в приложение
└── README.md
```

## ⚙️ Установка и настройка

### 1. Клонирование проекта

```bash
git clone https://github.com/username/hh_vacancies_db.git
cd hh_vacancies_d
```

### 2. Установка зависимостей

Проект использует Poetry — удобный менеджер зависимостей.

`poetry install`

### 3. Настройка переменных окружения

Создайте файл `.env` на основе примера:

`cp src/.env.example src/.env`

Внутри `.env` укажите параметры подключения к PostgreSQL:

```
DB_NAME=vacancies_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## 🧠 Использование

1. Создание базы данных и таблиц
`poetry run python src/main.py`

Программа создаст базу данных (если её нет) и таблицы employers и vacancies.

2. Загрузка вакансий

Вы можете задать ключевое слово и список компаний прямо в коде main.py:

```
keyword = "Python developer"
companies = ["Тинькофф", "Яндекс", "Сбер"]
```

После запуска данные загрузятся и сохранятся в PostgreSQL.

## 📊 Работа с файлами

Модуль `file_utils.py` позволяет:

- сохранять данные в JSON:
`FileManager.save_to_json(vacancies_data, "vacancies.json")`

- загружать данные из JSON:
`data = FileManager.load_from_json("vacancies.json")`

- сохранять отчёты в TXT:
`FileManager.save_to_txt(["Top 10 компаний по количеству вакансий"], "report.txt")`

## 🧪 Тестирование

Проект покрыт модульными тестами с использованием `pytest`.

Запуск тестов:

`poetry run pytest -v`

Создание отчёта о покрытии тестами:

`poetry run pytest --cov=src --cov-report=term-missing`

## 💾 Кэширование и оптимизация

В проекте используется кэширование запросов API (через requests_cache или аналогичные решения),
что позволяет избежать повторных обращений к hh.ru при тестировании и разработке.

## 🧰 Зависимости

Основные библиотеки проекта:

```
requests — HTTP-запросы к API hh.ru
psycopg2 — подключение к PostgreSQL
python-dotenv — загрузка переменных окружения
pytest — тестирование
pytest-cov — отчёт о покрытии
```

(опционально) requests-cache — кэширование запросов API