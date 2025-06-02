import pytest
from src.managers.vacancy_manager import VacancyManager, Vacancy, VacancyStorage
from typing import Dict, Any, List


class FakeAPI:
    def get_vacancies(self, search_query):
        return [
            {
                "name": "Python Dev",
                "alternate_url": "http://example.com",
                "salary": {"from": 100000, "to": 150000},
                "description": "Python backend",
                "snippet": {"requirement": "Django"},
            },
            {
                "name": "Java Dev",
                "alternate_url": "http://example.com",
                "salary": {"from": 120000, "to": 160000},
                "description": "Java backend",
                "snippet": {"requirement": "Spring"},
            }
        ]


class InMemoryStorage(VacancyStorage):
    def __init__(self):
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy)

    def get_vacancies(self, criteria):
        return self._filter_vacancies(self.vacancies, criteria)

    def delete_vacancy(self, criteria):
        self.vacancies.clear()

    def _filter_vacancies(self, vacancies: List[Vacancy], criteria: Dict[str, Any]) -> List[Vacancy]:
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


def test_fetch_and_store_vacancies():
    manager = VacancyManager(api=FakeAPI(), storage=InMemoryStorage())
    manager.fetch_and_store_vacancies("Python")
    assert len(manager.storage.vacancies) == 2
    assert manager.storage.vacancies[0].title == "Python Dev"


def test_get_top_vacancies_by_salary():
    storage = InMemoryStorage()
    v1 = Vacancy("Low", "link", {"from": 50_000}, "desc", "req")
    v2 = Vacancy("High", "link", {"from": 150_000}, "desc", "req")
    v3 = Vacancy("Mid", "link", {"from": 100_000}, "desc", "req")
    for v in [v1, v2, v3]:
        storage.add_vacancy(v)
    manager = VacancyManager(api=None, storage=storage)

    top_vacancies = manager.get_top_vacancies_by_salary(2)
    assert [v.title for v in top_vacancies] == ["High", "Mid"]


def test_get_vacancies_with_keyword():
    storage = InMemoryStorage()
    v1 = Vacancy("Python", "link", None, "Python developer", "Python")
    v2 = Vacancy("Java", "link", None, "Java developer", "Java")
    storage.vacancies = [v1, v2]

    manager = VacancyManager(api=None, storage=storage)
    results = manager.get_vacancies_with_keyword("Python")
    assert len(results) == 1
    assert results[0].title == "Python"


def test_fetch_and_store_invalid_vacancy(mocker):
    class BrokenAPI:
        def get_vacancies(self, _):
            return [{"name": "Invalid", "salary": "not a dict"}]

    storage = InMemoryStorage()
    manager = VacancyManager(api=BrokenAPI(), storage=storage)

    # Подавим print() через мок
    mocker.patch("builtins.print")

    manager.fetch_and_store_vacancies("bad")
    assert len(storage.vacancies) == 0
