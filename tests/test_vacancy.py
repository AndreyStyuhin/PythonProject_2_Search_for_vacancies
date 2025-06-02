import pytest
from src.hh import Vacancy

def test_vacancy_salary_calculation():
    vacancy1 = Vacancy("Dev", "link", {"from": 100000, "to": 200000}, "desc", "req")
    assert vacancy1.get_salary() == 150000

    vacancy2 = Vacancy("Dev", "link", {"from": 120000, "to": None}, "desc", "req")
    assert vacancy2.get_salary() == 120000

    vacancy3 = Vacancy("Dev", "link", {"from": None, "to": 90000}, "desc", "req")
    assert vacancy3.get_salary() == 90000

    vacancy4 = Vacancy("Dev", "link", None, "desc", "req")
    assert vacancy4.get_salary() == 0

def test_vacancy_comparison():
    v1 = Vacancy("Dev1", "link1", {"from": 100000}, "desc", "req")
    v2 = Vacancy("Dev2", "link2", {"from": 120000}, "desc", "req")
    assert v2 > v1
    assert v1 < v2
    assert v1 != v2

def test_validate_and_create_valid_data():
    data = {
        "name": "Backend Developer",
        "alternate_url": "https://example.com",
        "salary": {"from": 100000, "to": 150000},
        "description": "Great job opportunity",
        "snippet": {"requirement": "Experience with Django"},
    }
    vacancy = Vacancy.validate_and_create(data)
    assert vacancy.title == "Backend Developer"
    assert vacancy.get_salary() == 125000
    assert "Django" in vacancy.requirements
