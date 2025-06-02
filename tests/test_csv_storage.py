import csv
from src.models import Vacancy
from src.storage.csv_storage import CSVVacancyStorage
import json


def test_csv_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.csv"
    storage = CSVVacancyStorage(str(file_path))
    assert file_path.exists()

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == ["title", "link", "salary", "description", "requirements"]

def test_csv_add_get_filter(tmp_path):
    file_path = tmp_path / "vac.csv"
    storage = CSVVacancyStorage(str(file_path))

    v1 = Vacancy("Dev1", "url1", {"from": 100000}, "desc", "req")
    v2 = Vacancy("Dev2", "url2", {"from": 50000}, "desc", "req")
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)

    result = storage.get_vacancies({"min_salary": 60000})
    assert len(result) == 1
    assert result[0].title == "Dev1"

def test_csv_delete_vacancy(tmp_path):
    file_path = tmp_path / "vac.csv"
    storage = CSVVacancyStorage(str(file_path))

    v = Vacancy("Dev", "url", {"from": 100000}, "desc", "req")
    storage.add_vacancy(v)
    storage.delete_vacancy({"title": "Dev"})
    result = storage.get_vacancies({})
    assert len(result) == 0