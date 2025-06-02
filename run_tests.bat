@echo off
REM Активация виртуального окружения
call .venv\Scripts\activate

REM Установка PYTHONPATH (чтобы модуль src был виден)
set PYTHONPATH=%PYTHONPATH%;src

REM Запуск тестов с покрытием и отчётом
pytest --cov=src --cov-report=term --cov-report=html

REM Открытие HTML отчёта в браузере (опционально)
start htmlcov\index.html

pause