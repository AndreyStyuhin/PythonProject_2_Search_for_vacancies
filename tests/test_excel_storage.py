import openpyxl

from src.storage.excel_storage import ExcelVacancyStorage


def test_excel_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.xlsx"
    storage = ExcelVacancyStorage(str(file_path))
    assert file_path.exists()

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    assert sheet["A1"].value == "title"
    workbook.close()