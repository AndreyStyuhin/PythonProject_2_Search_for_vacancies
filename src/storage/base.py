import abc
from typing import List, Dict, Any
from ..models import Vacancy


class VacancyStorage(abc.ABC):
    """Абстрактный класс для работы с хранилищем вакансий."""

    @abc.abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище."""
        pass

    @abc.abstractmethod
    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        """Получает вакансии по критериям."""
        pass

    @abc.abstractmethod
    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """Удаляет вакансии по критериям."""
        pass

    def _filter_vacancies(self, vacancies: List[Vacancy], criteria: Dict[str, Any]) -> List[Vacancy]:
        """Базовая реализация фильтрации вакансий."""
        if not criteria:
            return vacancies

        filtered = []
        for vacancy in vacancies:
            matches = True
            for key, value in criteria.items():
                if key == "keyword":
                    keyword_lower = value.lower()
                    title_match = keyword_lower in vacancy.title.lower()
                    desc_match = keyword_lower in vacancy.description.lower()
                    req_match = keyword_lower in vacancy.requirements.lower()

                    if not (title_match or desc_match or req_match):
                        matches = False
                        break
                elif key == "min_salary":
                    if vacancy.get_salary() < value:
                        matches = False
                        break
                elif getattr(vacancy, key, None) != value:
                    matches = False
                    break
            if matches:
                filtered.append(vacancy)
        return filtered

    def _matches_criteria(self, vacancy: Vacancy, criteria: Dict[str, Any]) -> bool:
        """Проверяет, соответствует ли вакансия критериям."""
        for key, value in criteria.items():
            if key == "keyword":
                keyword_lower = value.lower()
                title_match = keyword_lower in vacancy.title.lower()
                desc_match = keyword_lower in vacancy.description.lower()
                req_match = keyword_lower in vacancy.requirements.lower()

                if not (title_match or desc_match or req_match):
                    return False
            elif key == "min_salary":
                if vacancy.get_salary() < value:
                    return False
            elif getattr(vacancy, key, None) != value:
                return False
        return True
