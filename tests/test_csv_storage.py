import csv
from src.storage.csv_storage import CSVVacancyStorage


def test_csv_storage_file_creation(tmp_path):
    file_path = tmp_path / "vacancies.csv"
    storage = CSVVacancyStorage(str(file_path))
    assert file_path.exists()

    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        headers = next(reader)
        assert headers == ["title", "link", "salary", "description", "requirements"]
