import logging
import os
import re

from config import DATA_PATH, LOGS_PATH
from src.utils import get_data_info

logger = logging.getLogger("__name__")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(f"{LOGS_PATH}/logs_services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def search_in_file(my_list: list[dict], search_str) -> list[dict]:
    """Функция поиска принемаемая список словарей и ключевое слово, а возвращает список транзакций выбраных по ключевом
    словам в 'категориях' и 'описании'"""

    logger.info("Старт программы")
    search_list = []
    logger.info("Проверка на пустые значения")
    for item in my_list:
        if (
            item['Категория'] is None or
            item['Категория'] == "nan" or
            item['Описание'] is None or
            item['Описание'] == "nan"
        ):
            item.clear()
        elif search_str in str(item['Категория']) or search_str in str(item['Описание']):
            search_list.append(item)
    logger.info("Формирования списка по критериям и конец программы")
    return search_list


def filter_by_name(my_list: list[dict]) -> list[dict]:
    """rgegsdrgd"""

    logger.info("Старт программы")
    search_list = []
    logger.info("Проверка на пустые значения")
    for item in my_list:
        if (
                item['Категория'] is None or
                item['Категория'] == "nan" or
                item['Описание'] is None or
                item['Описание'] == "nan"
        ):
            item.clear()
        elif 'Перевод' in str(item['Категория']) and re.search(r'\D+ \D\.', str(item['Описание'])):
            search_list.append(item)
    logger.info("Формирования списка по критериям и конец программы")
    return search_list


def filter_by_tel(my_list: list[dict]) -> list[dict]:
    """Функция принимает на вход список словарей, а возвращает только не у которых в описании есть номер телефона"""

    logger.info("Старт программы")
    search_list = []
    logger.info("Производим поиск по патерну")
    for item in my_list:

        if re.search(r'\+7 \S{3} \S{3}-\S{2}-\S{2}', str(item['Описание'])):
            search_list.append(item)
    logger.info("Формирования списка по критериям и конец программы")
    return search_list


if __name__ == '__main__':
    path_df = os.path.join(DATA_PATH, "operations.xlsx")
    df = get_data_info(path_df)
    convert_to_dict = df.to_dict('records')

    # search_str = input("Введите ключевое слово для потска\n")
    # res_search_list = search_in_file(convert_to_dict, search_str)
    # print(f'Список по ключу {search_str}\n{res_search_list}')

    list_tel = filter_by_tel(convert_to_dict)
    print(f'JSON данные с телефонами:\n{list_tel}')

    # filter_list_by_name = filter_by_name(convert_to_dict)
    # print(f'Отфильтрованый список переводов физлицу:\n{filter_list_by_name}')
