import os
import pathlib
from pathlib import Path
from typing import Any

import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv

from data.config import PATH_XLS_FILE_WITH_OPERATION
from src.logger import setup_logger

logger = setup_logger("views")


def read_xls_file(any_path: Path) -> Any:
    """
    Генератор чтения таблицы
    :param any_path: Путь до эксель таблицы
    :return: генератор
    """
    operation_data = pd.read_excel(any_path, index_col=0)
    for i in operation_data.iterrows():
        logger.debug("Выводим словарь с данными по транзакциям")
        yield i[1].to_dict()


def get_stock_data(stock_exchange_shares: list) -> list:
    """Функция, которая получает стоимость акции, по названию акции"""
    # stock_exchange_shares = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    if not find_dotenv():
        logger.error("Нет .env файла, завершаем программу")
        exit("Переменные окружения не загружены, т.к. отсутствует файл .env")
    else:
        load_dotenv()
        stocks_info = []
        API_KEY = os.getenv("API_KEY")
    try:
        for stock in stock_exchange_shares:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={API_KEY}"
            if url is not None:
                response = requests.get(url)
                response.raise_for_status()
                response_data = response.json()
                stock_price = response_data["c"]
                info = {"stock": stock, "price": stock_price}
                stocks_info.append(info)
        logger.debug("Функция отработала")
        return stocks_info
    except (requests.exceptions.HTTPError, ValueError, KeyError) as e:
        logger.error(f"Ошибка {e}")
        raise ValueError("Что-то пошло не так")


def currency_rates(currencies: list) -> Any:
    """
    Функция отправляет запрос на сайт ЦБ РФ и получает курс валют в формате JSON
    :param url: строка с адресом
    :return: ничего не возвращаем
    """
    if not find_dotenv():
        logger.error("нет .env файла завершаем программу")
        exit("Переменные окружения не загружены, т.к. отсутствует файл .env")
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
        logger.debug("Функция отработала")
        return rates_info


def get_exel(any_path: str) -> Any:
    """Загрузка данных из эксель файла"""
    try:
        if str(any_path).endswith(".xls"):
            return pd.read_excel(any_path, index_col=0)
        else:
            logger.error("Эксель файл не найден")
            raise ValueError("Файл не найден")
    except ValueError as e:
        logger.error(f"Ошибка {e}")
        return "Файл не найден"
