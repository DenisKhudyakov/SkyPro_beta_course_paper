import os

import pandas as pd
from pathlib import Path
from data.config import PATH_XLS_FILE_WITH_OPERATION
from typing import Any
from datetime import datetime
import requests
import re
import json
from dotenv import load_dotenv, find_dotenv


def read_xls_file(any_path: Path) -> dict:
    """
    Генератор чтения таблицы
    :param any_path: Путь до эксель таблицы
    :return: генератор
    """
    operation_data = pd.read_excel(any_path, index_col=0)
    for i in operation_data.iterrows():
        yield i[1].to_dict()



def get_stock_data():
    """Функция, которая получает стоимость акции, по названию акции"""
    stock_exchange_shares = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    if not find_dotenv():
        exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
    else:
        load_dotenv()
        stocks_info = []
    API_KEY = os.getenv('API_KEY')
    try:
        for stock in stock_exchange_shares:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={API_KEY}"
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()
            stock_price = response_data["c"]
            info = {"stock": stock,
                    "price": stock_price
            }
            stocks_info.append(info)
        return stocks_info
    except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
            print(e)

def currency_rates(currencies: list) -> dict:
    """
    Функция отправляет запрос на сайт ЦБ РФ и получает курс валют в формате JSON
    :param url: строка с адресом
    :return: ничего не возвращаем
    """
    if not find_dotenv():
        exit('Переменные окружения не загружены, т.к. отсутствует файл .env')
    else:
        load_dotenv()
        url_api = os.getenv("URL")
    if url_api is not None:
        response = requests.get(url_api)
        data_dict = response.json()
        rates_info = []
        for currency in currencies:
            cbr_data = data_dict["Valute"][currency]["Value"]
            info = {"currency": currency, "rate": round(cbr_data, 2)}
            rates_info.append(info)
        return rates_info


