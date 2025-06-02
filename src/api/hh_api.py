import requests
from typing import List, Dict, Any
from .base import VacancyAPI


class HHVacancyAPI(VacancyAPI):
    """Класс для работы с API hh.ru."""

    def __init__(self):
        self.base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получает вакансии с hh.ru по поисковому запросу."""
        params = {
            "text": search_query,
            "area": 113,  # Россия
            "per_page": 100,  # Количество вакансий на странице
        }
        response = requests.get(self.base_url, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
