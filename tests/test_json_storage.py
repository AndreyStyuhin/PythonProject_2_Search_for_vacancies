import tempfile
import os
from src.hh import Vacancy, JSONVacancyStorage

def test_add_and_get_vacancy():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
        path = tmp.name

    try:
        storage = JSONVacancyStorage(path)
        vacancy = Vacancy(
            title="Tester",
            link="http://test.com",
            salary={"from": 70_000, "to": 90_000},
            description="Testing apps",
            requirements="Automation",
        )
        storage.add_vacancy(vacancy)
        results = storage.get_vacancies({"min_salary": 60_000})
        assert len(results) == 1
        assert results[0].title == "Tester"
    finally:
        os.remove(path)
