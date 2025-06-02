import pytest
from src.hh import HHVacancyAPI

def test_hh_api_get_vacancies(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Mock Dev",
                "alternate_url": "http://example.com",
                "salary": {"from": 100000, "to": 150000},
                "description": "Test desc",
                "snippet": {"requirement": "Mock framework"}
            }
        ]
    }
    mock_response.raise_for_status = mocker.Mock()

    # Мокаем requests.get
    mocker.patch("src.hh.requests.get", return_value=mock_response)

    api = HHVacancyAPI()
    results = api.get_vacancies("Python")

    assert isinstance(results, list)
    assert results[0]["name"] == "Mock Dev"
    assert results[0]["salary"]["from"] == 100000
