import os
import tempfile
from src.storage.txt_storage import TXTVacancyStorage
from src.models.vacancy import Vacancy

def test_txt_storage_add_and_get():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        path = tmp.name

    try:
        storage = TXTVacancyStorage(path)
        vacancy = Vacancy("QA", "http://link", {"from": 50000}, "desc", "req")
        storage.add_vacancy(vacancy)

        results = storage.get_vacancies({"min_salary": 40000})
        assert len(results) == 1
        assert results[0].title == "QA"
    finally:
        os.remove(path)


def test_txt_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.txt"
    storage = TXTVacancyStorage(str(file_path))

    # Принудительно создадим файл через add_vacancy
    vacancy = Vacancy("Dev", "link", None, "desc", "req")
    storage.add_vacancy(vacancy)

    assert file_path.exists()

def test_txt_filter_min_salary(tmp_path):
    file_path = tmp_path / "vac.txt"
    storage = TXTVacancyStorage(str(file_path))
    v1 = Vacancy("A", "url", {"from": 100000}, "desc", "req")
    v2 = Vacancy("B", "url", {"from": 20000}, "desc", "req")
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)

    result = storage.get_vacancies({"min_salary": 80000})
    assert len(result) == 1
    assert result[0].title == "A"

def test_txt_delete_vacancy(tmp_path):
    file_path = tmp_path / "vac.txt"
    storage = TXTVacancyStorage(str(file_path))
    v = Vacancy("Dev", "url", {"from": 100000}, "desc", "req")
    storage.add_vacancy(v)
    storage.delete_vacancy({"title": "Dev"})
    assert storage.get_vacancies({}) == []
