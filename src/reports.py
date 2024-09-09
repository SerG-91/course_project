import datetime
import os
from typing import Optional
import logging
import pandas as pd
from config import DATA_PATH, LOGS_PATH
from src.utils import get_data_info


logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{LOGS_PATH}/logs_reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция принимает фрейм, категорию и дату и возвращает отсортированый фрейм на 3месяца по категории"""

    logger.info("Старт программы")
    if date == '':
        end_date = datetime.datetime.now()
        start_date = end_date.replace(year=end_date.year, month=end_date.month - 2, day=end_date.day)
    else:
        end_date = datetime.datetime.strptime(date, "%d.%m.%Y")
        start_date = end_date.replace(year=end_date.year, month=end_date.month - 2, day=end_date.day)
    logger.info("Получили даты интервала сортировки")
    transactions["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    sort_by_data: pd.DataFrame = transactions.loc[
            (transactions["Дата платежа"] >= start_date) & (transactions["Дата платежа"] <= end_date)]
    logger.info("Отсортировани по заданному интервалу")
    sort_by_category: pd.DataFrame = sort_by_data.loc[sort_by_data["Категория"] == category]
    sort_by_category.sort_values(by='Описание')
    logger.info("Конец программы")
    return sort_by_category


if __name__ == '__main__':
    path_df = os.path.join(DATA_PATH, "operations.xlsx")
    df = get_data_info(path_df)
    need_date = input('Ведите дату в формате дд.мм.гггг\n')
    print(spending_by_category(df, 'Фастфуд', need_date))

