from datetime import datetime
from typing import Any
from src.views import read_xls_file
from data.config import PATH_XLS_FILE_WITH_OPERATION
from src.logger import setup_logger

logger = setup_logger("utils")


def greeting() -> str:
    """
    Функция приветствие, вывод зависит от времени в сутках
    :return: строковое значение списка
    """
    time_list = ["Доброе утро", "Добрый день", "Добрый вечер"]
    current_time = datetime.now().time().hour
    logger.debug("Выполняется функция приветствия")
    return time_list[0] if current_time < 12 else time_list[1] if current_time < 18 else time_list[2]


def last_digits(card_number: str) -> str:
    """
    Функция преобразования номера карты, в последние четыре цифры
    :param card_number:
    :return: последние 4 цифры карты
    """
    logger.debug("Выполняется функция преобразования номера карты")
    return card_number[-4:]


def filter_operation(generator_obj: Any, date_: str = None) -> list[Any]:
    """
    Функция генератор, фильтрующая данные операции от начала месяца до указанной даты
    :param date_: указанная дата
    :param generator_obj: итерируемые данные по банковским операциям
    :return: новый генератор операций, которые удовлетворяют условиям диапазона.
    """

    def in_the_range(dict_: dict) -> bool:
        end_date = datetime.strptime(date_, "%d.%m.%Y").date()
        start_date = datetime.strptime("01" + date_[2:], "%d.%m.%Y").date()
        range_date = [start_date, end_date]
        current_date = datetime.strptime(dict_["Дата платежа"], "%d.%m.%Y").date()
        return True if current_date in range_date else False

    for i in generator_obj:
        try:
            if in_the_range(i):
                logger.debug("Операция отфильтрована")
                yield i
        except TypeError:
            continue


def top_five_transactions(generator_obj: Any) -> list:
    """
    Функция, которая выводит 5 наибольших транзакций, по сумме платежа
    :param generator_obj: Генератор тразнакций
    :return: Список словарей с банковскими операциями
    """
    transactions = []
    top_five = list(sorted(generator_obj, key=lambda x: abs(x["Сумма платежа"]), reverse=True))[:5]
    for i in top_five:
        date = datetime.strptime(i["Дата платежа"], "%d.%m.%Y").strftime("%d.%m.%Y")
        info = {"date": date, "amount": i["Сумма операции"], "category": i["Категория"], "description": i["Описание"]}
        transactions.append(info)
        logger.debug("Список наибольших транзакций сформирован")
    return transactions


def get_cash_back_and_expenses(generator_obj: Any) -> list[dict]:
    """
    Функция анализирующая расходы пользователя карты
    :param generator_obj: банковские данные
    :return: отструктурированный словарь с данными
    """
    card_info = []
    bank_data = tuple(generator_obj)
    cards = tuple(set([i["Номер карты"] for i in bank_data if str(i["Номер карты"]) != "nan"]))
    for card in cards:
        spending = -sum([i["Сумма операции"] for i in bank_data if i["Сумма операции"] < 0 and i["Номер карты"] == card])
        cashback = sum([i["Кэшбэк"] for i in bank_data if str(i["Кэшбэк"] != "nan") and i["Номер карты"] == card])
        info = {"last_digits": last_digits(card), "total_spent": spending, "cashback": cashback}
        card_info.append(info)
        logger.debug("Получен список всех трат и кэшбэка по указанной карте")
    return card_info


if __name__ == '__main__':
    print(next(filter_operation(read_xls_file(PATH_XLS_FILE_WITH_OPERATION), '31.12.2021')))
    print(list(top_five_transactions(filter_operation(read_xls_file(PATH_XLS_FILE_WITH_OPERATION), '31.12.2021'))))
    print(next(read_xls_file(PATH_XLS_FILE_WITH_OPERATION)))
