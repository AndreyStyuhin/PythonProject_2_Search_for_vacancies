import openpyxl

from src.models import Vacancy
from src.storage.excel_storage import ExcelVacancyStorage


def test_excel_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.xlsx"
    storage = ExcelVacancyStorage(str(file_path))
    assert file_path.exists()

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    assert sheet["A1"].value == "title"
    workbook.close()

def test_excel_add_get_filter(tmp_path):
    file_path = tmp_path / "vac.xlsx"
    storage = ExcelVacancyStorage(str(file_path))
    v1 = Vacancy("A", "url", {"from": 100000}, "desc", "req")
    v2 = Vacancy("B", "url", {"from": 40000}, "desc", "req")
    storage.add_vacancy(v1)
    storage.add_vacancy(v2)

    result = storage.get_vacancies({"min_salary": 60000})
    assert len(result) == 1
    assert result[0].title == "A"

def test_excel_delete_vacancy(tmp_path):
    file_path = tmp_path / "vac.xlsx"
    storage = ExcelVacancyStorage(str(file_path))
    v = Vacancy("X", "url", {"from": 100000}, "desc", "req")
    storage.add_vacancy(v)
    storage.delete_vacancy({"title": "X"})
    assert storage.get_vacancies({}) == []