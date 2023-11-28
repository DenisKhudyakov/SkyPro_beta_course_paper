import pandas as pd
from pathlib import Path
from data.config import PATH_XLS_FILE_WITH_OPERATION
from typing import Any
from datetime import datetime
import requests
import re
import json


API_KEY = 'f069fd48b23c4ff6819b137bb51c9c94'

def read_xls_file(any_path: Path) -> dict:
    """
    Генератор чтения таблицы
    :param any_path: Путь до эксель таблицы
    :return: генератор
    """
    operation_data = pd.read_excel(any_path, index_col=0)
    for i in operation_data.iterrows():
        yield i[1].to_dict()



def get_api():
    response = requests.get('https://ru.tradingview.com/symbols/SPX/components/')
    text = re.findall(r'"response_json":.+</script></div>', response.text)[0][:-15]
    print(response.text)
    new_text = re.findall(r'\{(?:.*?)\}\]\}', text)
    return json.loads(*new_text)

def filter_stock_data(_dict: dict) -> list:
    stock_exchange_shares = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    return list(filter(lambda x: x['d'][0] in stock_exchange_shares, _dict['data']))

get_api()

