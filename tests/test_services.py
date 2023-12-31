import json
from typing import Any

import pytest

from src.services import search_phone_number


@pytest.fixture
def bank_data() -> list:
    return [
        {
            "Дата платежа": "19.11.2021",
            "Номер карты": "*5091",
            "Статус": "OK",
            "Сумма операции": -4.2,
            "Валюта операции": "RUB",
            "Сумма платежа": -4.2,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Каршеринг",
            "MCC": 7512.0,
            "Описание": "Ситидрайв",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 4.2,
        },
        {
            "Дата платежа": "19.11.2021",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -14.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -14.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Детские товары",
            "MCC": 5641.0,
            "Описание": "Детки",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 14.0,
        },
        {
            "Дата платежа": "19.11.2021",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -271.4,
            "Валюта операции": "RUB",
            "Сумма платежа": -271.4,
            "Валюта платежа": "RUB",
            "Кэшбэк": 2.0,
            "Категория": "Косметика",
            "MCC": 5977.0,
            "Описание": "Подружка",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 271.4,
        },
        {
            "Дата платежа": "19.11.2021",
            "Номер карты": "*4556",
            "Статус": "OK",
            "Сумма операции": -1620.27,
            "Валюта операции": "RUB",
            "Сумма платежа": -1620.27,
            "Валюта платежа": "RUB",
            "Кэшбэк": 81.0,
            "Категория": "Супермаркеты",
            "MCC": 5411.0,
            "Описание": "Перекрёсток",
            "Бонусы (включая кэшбэк)": 81,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 1620.27,
        },
        {
            "Дата платежа": "19.11.2021",
            "Номер карты": "nan",
            "Статус": "OK",
            "Сумма операции": -200.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -200.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Мобильная связь",
            "MCC": "nan",
            "Описание": "Тинькофф Мобайл +7 995 555-55-55",
            "Бонусы (включая кэшбэк)": 2,
            "Округление на инвесткопилку": 0,
            "Сумма операции с округлением": 200.0,
        },
    ]


def test_search_phone_number(bank_data: Any) -> None:
    assert search_phone_number(bank_data).__eq__(
        [
            {
                "date": "19.11.2021",
                "amount": -200.0,
                "category": "Мобильная связь",
                "description": "Тинькофф Мобайл +7 995 555-55-55",
            }
        ]
    )
