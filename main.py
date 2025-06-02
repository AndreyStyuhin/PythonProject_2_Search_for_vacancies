from src.hh import (
    HHVacancyAPI,
    JSONVacancyStorage,
    CSVVacancyStorage,
    ExcelVacancyStorage,
    TXTVacancyStorage,
    VacancyManager
)
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

    if storage_type == "JSON":
        storage = JSONVacancyStorage(file_path)
    elif storage_type == "CSV":
        storage = CSVVacancyStorage(file_path)
    elif storage_type == "Excel":
        storage = ExcelVacancyStorage(file_path)
    else:
        storage = TXTVacancyStorage(file_path)

    manager = VacancyManager(api, storage)

    while True:
        print("\nМеню:")
        print("1. Поиск вакансий на hh.ru")
        print("2. Показать топ N вакансий по зарплате")
        print("3. Поиск вакансий по ключевому слову в описании")
        print("4. Выход")

        choice = input("Выберите действие (1-4): ")

        if choice == "1":
            search_query = input("Введите поисковый запрос (например: Python разработчик): ")
            try:
                manager.fetch_and_store_vacancies(search_query)
                print(f"Вакансии по запросу '{search_query}' успешно сохранены.")
            except Exception as e:
                print(f"Ошибка при получении вакансий: {e}")

        elif choice == "2":
            try:
                n = int(input("Введите количество вакансий для отображения (N): "))
                top_vacancies = manager.get_top_vacancies_by_salary(n)
                print(f"\nТоп {n} вакансий по зарплате:")
                for i, vacancy in enumerate(top_vacancies, 1):
                    salary = vacancy.get_salary()
                    salary_str = f"{salary} RUB" if salary else "Зарплата не указана"
                    print(f"{i}. {vacancy.title}")
                    print(f"   Ссылка: {vacancy.link}")
                    print(f"   Зарплата: {salary_str}")
                    print(f"   Описание: {vacancy.description[:100]}...")
                    print(f"   Требования: {vacancy.requirements[:100]}...\n")
            except ValueError:
                print("Пожалуйста, введите корректное число.")

        elif choice == "3":
            keyword = input("Введите ключевое слово для поиска в описании: ")
            vacancies = manager.get_vacancies_with_keyword(keyword)
            print(f"\nНайдено {len(vacancies)} вакансий с ключевым словом '{keyword}':")
            for i, vacancy in enumerate(vacancies, 1):
                salary = vacancy.get_salary()
                salary_str = f"{salary} RUB" if salary else "Зарплата не указана"
                print(f"{i}. {vacancy.title}")
                print(f"   Ссылка: {vacancy.link}")
                print(f"   Зарплата: {salary_str}")
                print(f"   Описание: {vacancy.description[:100]}...")
                print(f"   Требования: {vacancy.requirements[:100]}...\n")

        elif choice == "4":
            print("До свидания!")
            break

        else:
            print("Неверный выбор. Пожалуйста, введите число от 1 до 4.")


if __name__ == "__main__":
    user_interaction()
