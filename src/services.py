import json
import re
from datetime import datetime
from typing import Any

from data.config import PATH_XLS_FILE_WITH_OPERATION
from src.logger import setup_logger
from src.views import read_xls_file

logger = setup_logger("services")


def search_phone_number(generator_obj: Any) -> str:
    """
    функция поиска транзакций для по номеру телефона
    :param generator_obj: банковские данные
    :return: Обработанные данные
    """
    phone_number_pattern = r"(\+7|8)[- .]?\d{1,3}[- .]?\d{1,3}[- .]?\d{1,4}"
    transactions = [i for i in generator_obj if re.search(phone_number_pattern, i["Описание"])]
    list_ = []
    for i in transactions:
        date = datetime.strptime(i["Дата платежа"], "%d.%m.%Y").strftime("%d.%m.%Y")
        info = {"date": date, "amount": i["Сумма операции"], "category": i["Категория"], "description": i["Описание"]}
        list_.append(info)
    transactions_data = json.dumps(list_, ensure_ascii=False, indent=4)
    logger.debug("Сформирована структура данных, где есть номер телефона")
    return transactions_data


if __name__ == "__main__":
    print(search_phone_number(list(read_xls_file(PATH_XLS_FILE_WITH_OPERATION))[255:260]))
