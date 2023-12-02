import pandas as pd
from typing import Any, Callable, Optional
import functools
from datetime import datetime, timedelta
from src.views import get_exel
from data.config import PATH_XLS_FILE_WITH_OPERATION



def spending_by_category(transactions: pd.DataFrame,
                         category: str =None,
                         date: Optional[str] = None) -> pd.DataFrame:
    """Функция, фильтрующая данные по дате и по категориям"""
    if not date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%d.%m.%Y")
    start_date = end_date - timedelta(weeks=12)
    start_date_formatted = pd.to_datetime(start_date, dayfirst=True)
    end_date_formatted = pd.to_datetime(end_date, dayfirst=True)
    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    filtered_df = transactions[(transactions['Дата платежа'] <= end_date_formatted) & (transactions['Дата платежа'] >= start_date_formatted)]
    filtered_df_with_category = filtered_df[(filtered_df["Категория"] == category)]
    return filtered_df_with_category
