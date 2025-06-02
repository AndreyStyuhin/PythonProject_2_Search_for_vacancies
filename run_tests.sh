
# Активировать виртуальное окружение
source .venv/bin/activate

# Установить PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Запуск тестов с покрытием
pytest tests/ --cov=src --cov-report=html --cov-report=term

