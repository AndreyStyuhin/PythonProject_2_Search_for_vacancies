from .base import VacancyStorage
from .json_storage import JSONVacancyStorage
from .excel_storage import ExcelVacancyStorage
from .csv_storage import CSVVacancyStorage
from .txt_storage import TXTVacancyStorage

__all__ = ['VacancyStorage', 'JSONVacancyStorage', 'ExcelVacancyStorage', 'CSVVacancyStorage', 'TXTVacancyStorage']

