from typing import Dict, Any, Optional


class Vacancy:
    """Класс для представления вакансии."""

    def __init__(
            self,
            title: str,
            link: str,
            salary: Optional[Dict[str, Optional[int]]],
            description: str,
            requirements: str,
    ):
        self.title = title
        self.link = link
        self.salary = salary
        self.description = description
        self.requirements = requirements

    def __repr__(self):
        return (
            f"Vacancy(title='{self.title}', link='{self.link}', "
            f"salary={self.salary}, description='{self.description[:50]}...', "
            f"requirements='{self.requirements[:50]}...')"
        )

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return False
        return self.get_salary() == other.get_salary()

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary() < other.get_salary()

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary() <= other.get_salary()

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary() > other.get_salary()

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.get_salary() >= other.get_salary()

    def get_salary(self) -> int:
        """Возвращает среднюю зарплату или 0, если зарплата не указана."""
        if not self.salary:
            return 0
        from_salary = self.salary.get("from")
        to_salary = self.salary.get("to")
        if from_salary and to_salary:
            return (from_salary + to_salary) // 2
        elif from_salary:
            return from_salary
        elif to_salary:
            return to_salary
        else:
            return 0

    def to_dict(self) -> Dict[str, Any]:
        """Преобразует объект Vacancy в словарь."""
        return {
            "title": self.title,
            "link": self.link,
            "salary": self.salary,
            "description": self.description,
            "requirements": self.requirements
        }

    @classmethod
    def validate_and_create(cls, data: Dict[str, Any]) -> "Vacancy":
        """Валидирует данные и создает экземпляр Vacancy."""
        # Проверяем наличие обязательных полей
        title = data.get("title") or data.get("name", "")
        if not title:
            raise ValueError("Title/name is required")

        salary = data.get("salary")
        if salary is not None:
            if not isinstance(salary, dict):
                raise ValueError("Salary must be a dictionary or None")
            # Проверяем структуру зарплаты
            valid_keys = {"from", "to", "currency"}
            if not any(key in valid_keys for key in salary.keys()):
                raise ValueError("Invalid salary structure")

        return cls(
            title=title,
            link=data.get("alternate_url", "") or data.get("link", ""),
            salary=salary,
            description=data.get("description", ""),
            requirements=data.get("snippet", {}).get("requirement", "") if isinstance(data.get("snippet"),
                                                                                      dict) else data.get(
                "requirements", ""),
        )
