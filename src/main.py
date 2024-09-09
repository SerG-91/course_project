import os
import re

from config import DATA_PATH
from src.utils import sort_by_date, get_data_info, get_greeting_user, top_five_transactions, sorted_cards

if __name__ == '__main__':
    print(get_greeting_user())
    path_df = os.path.join(DATA_PATH, "operations.xlsx")
    result = {}

    df = get_data_info(path_df)  # получаем общий датафрейм
    sort_date_finish = input("Введите дату в формате: ДД.ММ.ГГГГ\n")  # Ввод пользователем даты
    while True:
        if re.search(r'\w{2}\.\w{2}\.\w{4}', sort_date_finish):
            sort_by_date_df = sort_by_date(df, str(sort_date_finish))
            break
        else:
            sort_date_finish = input("Введите дату в формате: ДД.ММ.ГГГГ\n")
    res_1 = get_greeting_user()
    res_2 = top_five_transactions(sort_by_date_df)
    res_3 = sorted_cards(sort_by_date_df)

    result["greeting"] = res_1
    result["top_transactions"] = res_2
    result["cards"] = res_3

    print(result)
