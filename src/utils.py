import logging

import pandas as pd
import datetime

from config import LOGS_PATH

logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{LOGS_PATH}/logs_utils.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_data_info(path: str) -> pd.DataFrame:
    """Функция получаят на входе путь до файла "operations.xlsx" и возвращает датафрейм"""
    logger.info("Формируем датафрейм из файла")
    df = pd.read_excel(path)
    return df


def get_greeting_user() -> str:
    """Функция приветствия пользователя возвращает: Доброе утро/Добрый день/Добрый вечер/Доброй ночи"""

    logger.info("Определяет текущее время")
    current_data_time = datetime.datetime.now()
    hour = int(current_data_time.hour) // 6
    logger.info("Возвращает приветствие исзодя из того сколько времени")
    if hour == 0:
        return 'Доброе утро'
    elif hour == 1:
        return 'Добрый день'
    elif hour == 2:
        return 'Добрый вечер'
    elif hour == 3:
        return 'Доброй ночи'


def sort_by_date(df: pd.DataFrame, date: str) -> pd.DataFrame:
    """Функция сортирует датафрейм по интервалу дат"""
    logger.info("Определяет интервалы времени")
    end_date = datetime.datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date.replace(year=end_date.year, month=end_date.month, day=1)
    df["Дата платежа"] = pd.to_datetime(df["Дата платежа"], dayfirst=True)
    sort_by_data_df = df.loc[(df["Дата платежа"] >= start_date) & (df["Дата платежа"] <= end_date)]
    logger.info("Выводит осортированый по диапазону даты список")
    return sort_by_data_df


def top_five_transactions(df: pd.DataFrame) -> list[dict]:
    """Функция получает на входе фрейм и выводит топ 5 транзакций по сумме платежа"""

    top_trans = []
    logger.info("Определяет первые пять записей отсортированых по сумме операции")
    ff_2 = df.sort_values('Сумма операции').iloc[:5, ].to_dict('records')
    for i in ff_2:
        top_trans.append(
            {
                "date": i["Дата операции"],
                "amount": i["Сумма операции"],
                "category": i["Категория"],
                "description": i["Описание"]}
        )
    logger.info("Выводит осортированый списки в новом формате")
    return top_trans


def sorted_cards(df: pd.DataFrame) -> list[dict]:
    """Функция принемаемая датафрейм и возвращает список сгруппированый по номерам карт и посчитаной суммой операций
    и кэшбек"""
    logger.info("Групирует списеи по номеру карты")
    group_cards = df.groupby("Номер карты")
    logger.info("Производит агрегацию по сумме операции")
    aggregated = group_cards.agg({'Сумма операции с округлением': 'sum'}).to_dict()
    res = []
    for i in aggregated.values():
        for key, value in i.items():
            cashback = round(float(value / 100), 2)
            res.append(
                {
                    'last_digits': str(key[-4:]),
                    'total_spent': value,
                    'cashback': cashback
                })
    logger.info("Выводит осортированый списки в новом формате")
    return res


# if __name__ == "__main__":
#     path_df = os.path.join(DATA_PATH, "operations.xlsx")
#     df_all = get_data_info(path_df)  # получаем общий датафрейм
#     print(sorted_cards(df_all))