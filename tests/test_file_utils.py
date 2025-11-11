import json

from src import file_utils
from src.file_utils import FileManager


def test_save_to_json_creates_file(tmp_path, capsys, monkeypatch):
    data = {"TestCompany": [{"title": "Backend Developer"}]}
    filename = "vacancies_test.json"

    # Подменяем DATA_DIR в модуле file_utils на временную папку tmp_path/data
    test_dir = tmp_path / "data"
    test_dir.mkdir()
    monkeypatch.setattr(file_utils, "DATA_DIR", test_dir)

    FileManager.save_to_json(data, filename)

    file_path = test_dir / filename

    # Проверка, что файл создан
    assert file_path.exists()

    # Проверка содержимого
    with open(file_path, "r", encoding="utf-8") as f:
        content = json.load(f)
    assert content == data

    # Проверка вывод в консоль
    captured = capsys.readouterr()
    assert "Данные сохранены в файл" in captured.out


def test_load_from_json_reads_data(tmp_path, monkeypatch):
    #  Временный JSON-файл
    test_dir = tmp_path / "data"
    test_dir.mkdir()
    file_path = test_dir / "test_vac.json"
    expected = {"Company": [{"title": "Python Dev"}]}
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(expected, f, ensure_ascii=False, indent=4)

    # Подмена DATA_DIR
    monkeypatch.setattr(file_utils, "DATA_DIR", test_dir)

    result = FileManager.load_from_json(file_path.name)
    assert result == expected


def test_save_to_txt_creates_file(tmp_path, capsys, monkeypatch):
    lines = ["Line 1", "Line 2", "Line 3"]
    filename = "output_test.txt"

    test_dir = tmp_path / "data"
    test_dir.mkdir()
    monkeypatch.setattr(file_utils, "DATA_DIR", test_dir)

    FileManager.save_to_txt(lines, filename)
    file_path = test_dir / filename

    # Проверка, что файл создан и содержит нужные строки
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().splitlines()
    assert content == lines

    # Проверка вывода
    captured = capsys.readouterr()
    assert "Результаты сохранены в" in captured.out
