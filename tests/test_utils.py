from datetime import datetime
from unittest.mock import patch

import pytest

from data.config import PATH_XLS_FILE_WITH_OPERATION
from src.utils import filter_operation, get_cash_back_and_expenses, greeting, last_digits, top_five_transactions
from src.views import read_xls_file


@pytest.mark.parametrize(
    "data, result",
    [
        (datetime(2023, 12, 2, 8, 00, 00, 00000), "Доброе утро"),
        (datetime(2023, 12, 2, 15, 00, 00, 00000), "Добрый день"),
        (datetime(2023, 12, 2, 22, 00, 00, 00000), "Добрый вечер"),
    ],
)
@patch("src.utils.datetime")
def test_greeting(mock_get, data, result) -> None:
    """
    Тестирование функции приветствия
    :param mock_get: пропатченная переменная datetime в модуле utils
    :param data: дата
    :param result: ожидаемый результат
    :return: Ничего
    """
    mock_get.now.return_value = data
    assert greeting() == result


def test_last_digits():
    """
    Тест функции преобразования номера карты
    :return: Ничего
    """
    assert last_digits("*5555") == "5555"


@pytest.fixture()
def bank_data_on_month():
    return {
        "Дата платежа": "31.12.2021",
        "Номер карты": "*7197",
        "Статус": "OK",
        "Сумма операции": -160.89,
        "Валюта операции": "RUB",
        "Сумма платежа": -160.89,
        "Валюта платежа": "RUB",
        "Кэшбэк": 12,
        "Категория": "Супермаркеты",
        "MCC": 5411.0,
        "Описание": "Колхоз",
        "Бонусы (включая кэшбэк)": 3,
        "Округление на инвесткопилку": 0,
        "Сумма операции с округлением": 160.89,
    }


def test_filter_operation():
    """Тестирование функции, по фильтрации операций"""
    assert next(filter_operation(read_xls_file(PATH_XLS_FILE_WITH_OPERATION), "31.12.2021"))["Категория"] == "Супермаркеты"


def test_top_five_transactions():
    """Тестирование функции, которая выводит 5 транзакций"""
    assert len(list(top_five_transactions(filter_operation(read_xls_file(PATH_XLS_FILE_WITH_OPERATION), "31.12.2021")))) == 5
    assert top_five_transactions([]) == []


def test_get_cash_back_and_expenses(bank_data_on_month):
    """Тестирование функции по выводу данныех по расхожу и кэшбэку"""
    assert get_cash_back_and_expenses([bank_data_on_month]) == [{"last_digits": "7197", "total_spent": 160.89, "cashback": 12}]
