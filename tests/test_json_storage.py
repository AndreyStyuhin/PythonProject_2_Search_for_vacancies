import tempfile
import os
from src.storage.json_storage import Vacancy, JSONVacancyStorage

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


def test_json_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONVacancyStorage(str(file_path))
    assert file_path.exists()


def test_json_storage_corrupted_file(tmp_path):
    file_path = tmp_path / "vacancies.json"
    file_path.write_text("{invalid json}")

    storage = JSONVacancyStorage(str(file_path))
    # Должен создать новый файл при ошибке чтения
    assert storage.get_vacancies({}) == []


def test_json_storage_filter_min_salary(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONVacancyStorage(str(file_path))

    # Добавляем вакансии с разными зарплатами
    vacancies = [
        Vacancy("Low", "link", {"from": 50_000}, "desc", "req"),
        Vacancy("High", "link", {"from": 150_000}, "desc", "req"),
    ]

    for v in vacancies:
        storage.add_vacancy(v)

    filtered = storage.get_vacancies({"min_salary": 100_000})
    assert len(filtered) == 1
    assert filtered[0].title == "High"

def test_json_storage_delete_vacancy(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONVacancyStorage(str(file_path))

    v1 = Vacancy("Dev1", "link", {"from": 100000}, "desc", "req")
    v2 = Vacancy("Dev2", "link", {"from": 150000}, "desc", "req")
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)

    storage.delete_vacancy({"title": "Dev1"})
    results = storage.get_vacancies({})
    assert len(results) == 1
    assert results[0].title == "Dev2"
