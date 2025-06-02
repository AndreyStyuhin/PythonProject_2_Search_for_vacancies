import json
from typing import List, Dict, Any
from .base import VacancyStorage
from ..models import Vacancy


class TXTVacancyStorage(VacancyStorage):
    """Класс для сохранения вакансий в TXT-файл."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def add_vacancy(self, vacancy: Vacancy) -> None:
        with open(self.file_path, "a", encoding="utf-8") as file:
            file.write(
                f"{vacancy.title}\t{vacancy.link}\t"
                f"{json.dumps(vacancy.salary) if vacancy.salary else ''}\t"
                f"{vacancy.description}\t{vacancy.requirements}\n"
            )

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        vacancies = []
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split("\t")
                    if len(parts) != 5:
                        continue
                    title, link, salary_str, description, requirements = parts
                    salary = json.loads(salary_str) if salary_str else None
                    vacancy = Vacancy(
                        title=title,
                        link=link,
                        salary=salary,
                        description=description,
                        requirements=requirements,
                    )
                    vacancies.append(vacancy)
        except FileNotFoundError:
            pass
        return self._filter_vacancies(vacancies, criteria)

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        vacancies = self.get_vacancies({})
        filtered_vacancies = [v for v in vacancies if not self._matches_criteria(v, criteria)]
        self._save_all_vacancies(filtered_vacancies)

    def _save_all_vacancies(self, vacancies: List[Vacancy]) -> None:
        with open(self.file_path, "w", encoding="utf-8") as file:
            for vacancy in vacancies:
                file.write(
                    f"{vacancy.title}\t{vacancy.link}\t"
                    f"{json.dumps(vacancy.salary) if vacancy.salary else ''}\t"
                    f"{vacancy.description}\t{vacancy.requirements}\n"
                )

    def _filter_vacancies(
        self, vacancies: List[Vacancy], criteria: Dict[str, Any]
    ) -> List[Vacancy]:
        filtered = []
        for vacancy in vacancies:
            matches = True
            for key, value in criteria.items():
                if key == "keyword":
                    if value.lower() not in vacancy.description.lower() and value.lower() not in vacancy.requirements.lower():
                        matches = False
                        break
                elif key == "min_salary":
                    if vacancy.get_salary() < value:
                        matches = False
                        break
                elif getattr(vacancy, key, None) != value:
                    matches = False
                    break
            if matches:
                filtered.append(vacancy)
        return filtered

    def _matches_criteria(self, vacancy_data: Dict[str, Any], criteria: Dict[str, Any]) -> bool:
        for key, value in criteria.items():
            if key == "keyword":
                description = vacancy_data.get("description", "").lower()
                requirements = vacancy_data.get("requirements", "").lower()
                title = vacancy_data.get("title", "").lower()
                if (value.lower() not in description and
                        value.lower() not in requirements and
                        value.lower() not in title):
                    return False
            elif key == "min_salary":
                vacancy = Vacancy.validate_and_create(vacancy_data)
                if vacancy.get_salary() < value:
                    return False
            elif getattr(vacancy_data, key, None) != value:
                return False
        return True