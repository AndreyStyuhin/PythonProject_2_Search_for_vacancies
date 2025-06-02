import pytest
from src.hh import VacancyManager, Vacancy

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

class InMemoryStorage:
    def __init__(self):
        self.vacancies = []

    def add_vacancy(self, vacancy):
        self.vacancies.append(vacancy)

    def get_vacancies(self, criteria):
        return self.vacancies

    def delete_vacancy(self, criteria):
        self.vacancies.clear()

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
