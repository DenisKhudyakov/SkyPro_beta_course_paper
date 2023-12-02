import pandas as pd
from typing import Any, Callable, Optional
import functools
from datetime import datetime, timedelta
from src.views import get_exel
from data.config import PATH_XLS_FILE_WITH_OPERATION, PATH_XLS_FILE_WITH_REPORTS
from src.logger import setup_logger
import json

logger = setup_logger("reports")


def report(*, filename: str = PATH_XLS_FILE_WITH_REPORTS) -> Callable:
    """Записывает в файл результат, который возвращает функция, формирующая отчет"""

    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        def inner(*args: Optional[Any], **kwargs: Optional[Any]) -> Optional[Any]:
            try:
                result = func(*args, **kwargs)
                with open(filename, "w", encoding="UTF-8"):
                    result.to_excel(filename, index=False)
                    logger.debug(f"Данные записаны в файл {filename}")
            except Exception as e:
                logger.error(e)
            return result

        return inner

    return wrapper


@report()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция, фильтрующая данные по дате и по категориям"""
    if not date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date - timedelta(weeks=12)
    start_date_formatted = pd.to_datetime(start_date, dayfirst=True)
    end_date_formatted = pd.to_datetime(end_date, dayfirst=True)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    filtered_df = transactions[
        (transactions["Дата платежа"] <= end_date_formatted) & (transactions["Дата платежа"] >= start_date_formatted)
    ]
    filtered_df_with_category = filtered_df[(filtered_df["Категория"] == category)]
    logger.debug("Отфильтрованы данные по операциям")
    return filtered_df_with_category


@report()
def func():
    return True


if __name__ == "__main__":
    with open("test.json", "w", encoding="UTF-8") as f:
        json_object = spending_by_category(
            get_exel(PATH_XLS_FILE_WITH_OPERATION), category="Переводы", date="25.11.2019"
        ).to_dict(orient="records")
        print(json_object)
