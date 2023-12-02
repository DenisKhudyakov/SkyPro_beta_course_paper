from unittest.mock import patch

import pandas as pd
import pytest
import requests

from data.config import PATH_XLS_FILE_WITH_OPERATION
from src.views import currency_rates, get_exel, get_stock_data, read_xls_file


def test_read_xls_file():
    assert str(type(read_xls_file(PATH_XLS_FILE_WITH_OPERATION))) == "<class 'generator'>"


@patch("src.views.pd.read_excel")
def test_get_exel(mock_get):
    mock_get.return_value = pd.DataFrame()
    result = get_exel("empty.xls")
    assert result.equals(mock_get.return_value)
    assert get_exel("empty.csv") == "Файл не найден"


@patch("src.views.os.getenv")
def test_get_stock_data_env_is_empty(mock_get):
    mock_get.return_value = None
    with pytest.raises(ValueError):
        assert get_stock_data(["AAPL"]) == "Что-то пошло не так"


@patch("requests.get")
def test_stock_rates(mock_get):
    mock_get.return_value.json.return_value = {"c": 200000}
    assert get_stock_data(["AAPL"]) == [{"stock": "AAPL", "price": 200000}]


@pytest.mark.parametrize("error", [KeyError, ValueError, requests.exceptions.HTTPError])
@patch("requests.get")
def test_stock_rates_errors(mock_get, error):
    mock_get.side_effect = error
    with pytest.raises(ValueError):
        assert get_stock_data(["mock"]) == "Что-то пошло не так"


@patch("src.views.os.getenv")
def test_currency_rates_is_empty(mock_get):
    mock_get.return_value = None
    assert currency_rates(["USD"]) is None


@patch("requests.get")
def test_currency_rates(mock_get):
    """Данный тест творит АД, он делает курс доллара 10 млн рублей и тесты проходят"""
    mock_get.return_value.json.return_value = {"Valute": {"USD": {"Value": 10_000_000}}}
    assert currency_rates(["USD"]) == [{"currency": "USD", "rate": 10000000}]
