from src.api import HHVacancyAPI
from src.storage import (
    JSONVacancyStorage,
    CSVVacancyStorage,
    ExcelVacancyStorage,
    TXTVacancyStorage
)
from src.managers import VacancyManager
import os


def user_interaction() -> None:
    """Функция для взаимодействия с пользователем."""
    print("Добро пожаловать в программу для работы с вакансиями hh.ru!")

    # Создаем папку data, если её нет
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Выбор хранилища
    print("\nВыберите формат для сохранения вакансий:")
    print("1. JSON")
    print("2. CSV")
    print("3. Excel")
    print("4. TXT")
    storage_choice = input("Введите номер варианта (1-4): ")

    storage_map = {
        "1": ("JSON", os.path.join(data_dir, "vacancies.json")),
        "2": ("CSV", os.path.join(data_dir, "vacancies.csv")),
        "3": ("Excel", os.path.join(data_dir, "vacancies.xlsx")),
        "4": ("TXT", os.path.join(data_dir, "vacancies.txt")),
    }

    if storage_choice not in storage_map:
        print("Неверный выбор. Используется JSON по умолчанию.")
        storage_choice = "1"

    storage_type, file_path = storage_map[storage_choice]
    print(f"Используется {storage_type} хранилище: {file_path}")

    # Создание экземпляров API и хранилища
    api = HHVacancyAPI()

    # Создание хранилища в зависимости от выбора пользователя
    storage = _create_storage(storage_type, file_path)

    # Создание менеджера вакансий
    manager = VacancyManager(api, storage)

    # Основной цикл взаимодействия с пользователем
    _main_menu_loop(manager)


def _create_storage(storage_type: str, file_path: str):
    """Создает экземпляр хранилища в зависимости от типа."""
    storage_classes = {
        "JSON": JSONVacancyStorage,
        "CSV": CSVVacancyStorage,
        "Excel": ExcelVacancyStorage,
        "TXT": TXTVacancyStorage
    }

    storage_class = storage_classes.get(storage_type, JSONVacancyStorage)
    return storage_class(file_path)


def _main_menu_loop(manager: VacancyManager) -> None:
    """Основной цикл меню программы."""
    while True:
        _display_menu()
        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            _handle_search_vacancies(manager)
        elif choice == "2":
            _handle_top_vacancies(manager)
        elif choice == "3":
            _handle_keyword_search(manager)
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")


def _display_menu() -> None:
    """Отображает главное меню."""
    print("\nМеню:")
    print("1. Поиск вакансий на hh.ru")
    print("2. Показать топ N вакансий по зарплате")
    print("3. Поиск вакансий по ключевому слову в описании")
    print("4. Выход")


def _handle_search_vacancies(manager: VacancyManager) -> None:
    """Обрабатывает поиск и сохранение вакансий."""
    search_query = input("Введите поисковый запрос (например: Python разработчик): ")
    try:
        manager.fetch_and_store_vacancies(search_query)
        print(f"Вакансии по запросу '{search_query}' успешно сохранены.")
    except Exception as e:
        print(f"Ошибка при получении вакансий: {e}")


def _handle_top_vacancies(manager: VacancyManager) -> None:
    """Обрабатывает показ топ вакансий по зарплате."""
    try:
        n = int(input("Введите количество вакансий для отображения (N): "))
        top_vacancies = manager.get_top_vacancies_by_salary(n)
        _display_vacancies(top_vacancies, f"Топ {n} вакансий по зарплате")
    except ValueError:
        print("Пожалуйста, введите корректное число.")


def _handle_keyword_search(manager: VacancyManager) -> None:
    """Обрабатывает поиск вакансий по ключевому слову."""
    keyword = input("Введите ключевое слово для поиска в описании: ")
    vacancies = manager.get_vacancies_with_keyword(keyword)
    _display_vacancies(vacancies, f"Найдено {len(vacancies)} вакансий с ключевым словом '{keyword}'")


def _display_vacancies(vacancies, title: str) -> None:
    """Отображает список вакансий."""
    print(f"\n{title}:")

    if not vacancies:
        print("Вакансии не найдены.")
        return

    for i, vacancy in enumerate(vacancies, 1):
        salary = vacancy.get_salary()
        salary_str = f"{salary} RUB" if salary else "Зарплата не указана"

        print(f"{i}. {vacancy.title}")
        print(f"   Ссылка: {vacancy.link}")
        print(f"   Зарплата: {salary_str}")
        print(f"   Описание: {_truncate_text(vacancy.description, 100)}")
        print(f"   Требования: {_truncate_text(vacancy.requirements, 100)}")
        print()


def _truncate_text(text: str, max_length: int) -> str:
    """Обрезает текст до указанной длины."""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."


if __name__ == "__main__":
    user_interaction()
