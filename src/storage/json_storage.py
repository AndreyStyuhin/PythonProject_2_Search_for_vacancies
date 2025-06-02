import json
import os
from typing import List, Dict, Any
from .base import VacancyStorage
from ..models import Vacancy


class JSONVacancyStorage(VacancyStorage):
    """Класс для сохранения вакансий в JSON-файл."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """Создает файл, если он не существует."""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "r", encoding="utf-8") as file:
                pass
        except FileNotFoundError:
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump([], file)
        except Exception as e:
            print(f"Ошибка при создании файла {self.file_path}: {e}")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в JSON файл."""
        vacancies = self._load_vacancies()
        if not isinstance(vacancies, list):
            vacancies = []
        vacancies.append(vacancy.to_dict())
        self._save_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict[str, Any]) -> List[Vacancy]:
        """Получает вакансии из JSON файла по критериям."""
        vacancies_data = self._load_vacancies()
        if not isinstance(vacancies_data, list):
            vacancies_data = []
        vacancies = [Vacancy.validate_and_create(data) for data in vacancies_data]
        return self._filter_vacancies(vacancies, criteria)

    def delete_vacancy(self, criteria: Dict[str, Any]) -> None:
        """Удаляет вакансии из JSON файла по критериям."""
        vacancies_data = self._load_vacancies()
        if not isinstance(vacancies_data, list):
            vacancies_data = []
        vacancies = [Vacancy.validate_and_create(data) for data in vacancies_data]
        filtered_vacancies = [
            v for v in vacancies if not self._matches_criteria(v, criteria)
        ]
        self._save_vacancies([v.to_dict() for v in filtered_vacancies])

    def _load_vacancies(self) -> List[Dict[str, Any]]:
        """Загружает вакансии из JSON файла."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
                else:
                    print(f"Предупреждение: файл {self.file_path} содержит некорректные данные.")
                    return []
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Файл {self.file_path} не найден или поврежден. Создается новый файл.")
            return []

    def _save_vacancies(self, vacancies: List[Dict[str, Any]]) -> None:
        """Сохраняет вакансии в JSON файл."""
        try:
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            with open(self.file_path, "w", encoding="utf-8") as file:
                json.dump(vacancies, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка при сохранении файла {self.file_path}: {e}")
