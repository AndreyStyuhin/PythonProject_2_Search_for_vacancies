import abc
from typing import List, Dict, Any


class VacancyAPI(abc.ABC):
    """Абстрактный класс для работы с API сервисов с вакансиями."""

    @abc.abstractmethod
    def get_vacancies(self, search_query: str) -> List[Dict[str, Any]]:
        """Получает список вакансий по поисковому запросу."""
        pass
