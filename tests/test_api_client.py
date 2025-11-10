import pytest
from unittest.mock import patch, MagicMock
from src.api_client import HeadHunterAPI


@pytest.fixture
def hh_api():
    """Фикстура для создания экземпляра API"""
    return HeadHunterAPI(token="fake_token")


@patch("src.api_client.requests.get")
def test_fetch_vacancies_returns_list(mock_get, hh_api):
    """Проверяет, что метод возвращает список вакансий"""
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "items": [{"id": "1", "name": "Python Developer"}]
    }
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    result = hh_api.fetch_vacancies("Tinkoff", keyword="Python")

    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["name"] == "Python Developer"


@patch("src.api_client.requests.get")
def test_fetch_vacancies_multiple_pages(mock_get, hh_api):
    """Проверяет, что вакансии собираются с нескольких страниц"""
    # первая страница с 1 вакансией
    mock_response_1 = MagicMock()
    mock_response_1.json.return_value = {"items": [{"id": "1"}]}
    mock_response_1.raise_for_status = MagicMock()

    # вторая страница пустая (чтобы цикл завершился)
    mock_response_2 = MagicMock()
    mock_response_2.json.return_value = {"items": []}
    mock_response_2.raise_for_status = MagicMock()

    mock_get.side_effect = [mock_response_1, mock_response_2]

    result = hh_api.fetch_vacancies("Авито", pages=2)

    assert len(result) == 1
    assert mock_get.call_count == 2  # два вызова API


@patch("src.api_client.requests.get")
def test_fetch_vacancies_handles_request_error(mock_get, hh_api):
    """Проверяет, что выбрасывается ошибка при сбое запроса"""
    mock_get.side_effect = Exception("Network error")

    with pytest.raises(Exception):
        hh_api.fetch_vacancies("Яндекс")


@patch("src.api_client.requests.get")
def test_fetch_vacancies_builds_correct_query(mock_get, hh_api):
    """Проверяет корректность формируемого запроса к API"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"items": []}
    mock_response.raise_for_status = MagicMock()
    mock_get.return_value = mock_response

    hh_api.fetch_vacancies("Сбер", keyword="Python")

    args, kwargs = mock_get.call_args
    params = kwargs["params"]

    assert "company_name:(Сбер)" in params["text"]
    assert "Python" in params["text"]
    assert params["only_with_salary"] is True
