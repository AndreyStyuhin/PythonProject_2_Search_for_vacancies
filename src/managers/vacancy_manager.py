from typing import List
from ..api import VacancyAPI
from ..storage import VacancyStorage
from ..models import Vacancy


class VacancyManager:
    """Класс для управления вакансиями."""

    def __init__(self, api: VacancyAPI, storage: VacancyStorage):
        self.api = api
        self.storage = storage

    def fetch_and_store_vacancies(self, search_query: str) -> None:
        """Получает вакансии по API и сохраняет их в хранилище."""
        vacancies_data = self.api.get_vacancies(search_query)
        for data in vacancies_data:
            try:
                vacancy = Vacancy.validate_and_create(data)
                self.storage.add_vacancy(vacancy)
            except ValueError as e:
                print(f"Ошибка при создании вакансии: {e}")

    def get_top_vacancies_by_salary(self, n: int) -> List[Vacancy]:
        """Возвращает топ N вакансий по зарплате."""
        vacancies = self.storage.get_vacancies({})
        vacancies.sort(reverse=True)
        return vacancies[:n]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Vacancy]:
        """Возвращает вакансии, содержащие ключевое слово в описании."""
        return self.storage.get_vacancies({"keyword": keyword})
