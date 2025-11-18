import json
from pathlib import Path
from typing import Any, Dict, List

DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)


class FileManager:
    """
    Класс для сохранения и загрузки данных о вакансиях в/из JSON файлов.
    """

    @staticmethod
    def save_to_json(data: Dict[str, List[Dict[str, Any]]], filename: str) -> None:
        """
        Сохраняет словарь с вакансиями в JSON файл.
        :param data: Словарь с вакансиями по компаниям
        :param filename: Имя файла (например, 'vacancies.json')
        """
        file_path = DATA_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Данные сохранены в файл: {file_path}")

    @staticmethod
    def load_from_json(filename: str) -> Dict[str, Any]:
        """
        Загружает данные из JSON файла.
        :param filename: Имя файла для загрузки (например, 'vacancies.json')
        :return: Данные в виде словаря
        """
        file_path = DATA_DIR / filename
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def save_to_txt(lines: List[str], filename: str) -> None:
        """
        Сохраняет список строк в текстовый файл (например, отчёты).
        :param lines: Список строк
        :param filename: Имя текстового файла
        """
        file_path = DATA_DIR / filename
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"Результаты сохранены в: {file_path}")
