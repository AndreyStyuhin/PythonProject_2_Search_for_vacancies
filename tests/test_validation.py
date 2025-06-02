import pytest
from src.models.vacancy import Vacancy

def test_validate_and_create_invalid_salary():
    bad_data = {
        "name": "Broken Vacancy",
        "alternate_url": "http://example.com",
        "salary": "100000",  # Некорректный тип (строка вместо словаря)
        "description": "Bad data",
        "snippet": {"requirement": "None"},
    }

    with pytest.raises(ValueError, match="Salary must be a dictionary or None"):
        Vacancy.validate_and_create(bad_data)

def test_validate_and_create_missing_fields():
    minimal_data = {
        "name": "No Salary",
        "alternate_url": "http://example.com",
        "description": "No salary provided",
        "snippet": {"requirement": ""},
    }

    vacancy = Vacancy.validate_and_create(minimal_data)
    assert vacancy.title == "No Salary"
    assert vacancy.salary is None
    assert vacancy.get_salary() == 0

def test_validate_and_create_missing_title():
    data = {
        "alternate_url": "http://example.com",
        "description": "No title",
        "snippet": {"requirement": ""},
    }
    with pytest.raises(ValueError):
        Vacancy.validate_and_create(data)

def test_validate_and_create_invalid_salary_structure():
    data = {
        "name": "Invalid Salary",
        "alternate_url": "http://example.com",
        "salary": {"amount": 100000},  # Неправильная структура
        "description": "Test",
        "snippet": {"requirement": ""},
    }
    with pytest.raises(ValueError):
        Vacancy.validate_and_create(data)