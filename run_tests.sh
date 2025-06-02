#!/bin/bash

# Активировать виртуальное окружение
source .venv/bin/activate

# Установить PYTHONPATH
export PYTHONPATH=src

# Запуск тестов с покрытием
pytest --cov=src --cov-report=term --cov-report=html

# Открыть HTML-отчёт (если установлен xdg-open или open)
if command -v xdg-open &> /dev/null; then
    xdg-open htmlcov/index.html
elif command -v open &> /dev/null; then
    open htmlcov/index.html
fi
