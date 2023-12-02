import os.path

import pytest
from src.views import get_exel
from data.config import PATH_XLS_FILE_WITH_OPERATION, PATH_XLS_FILE_WITH_REPORTS
import pandas as pd
from src.reports import spending_by_category, func
from unittest.mock import patch
from typing import Any


@pytest.fixture()
def bank_data() -> pd.DataFrame:
    return get_exel(PATH_XLS_FILE_WITH_OPERATION)


def test_spending_by_category(bank_data: pd.DataFrame) -> None:
    result = spending_by_category(bank_data, category="Переводы", date="25.11.2019").to_dict(orient="records")
    assert len([i["Категория"] for i in result]) == 27
    result = spending_by_category(bank_data, category="Переводы").to_dict(orient="records")
    assert [i["Категория"] for i in result] == []


def test_report() -> None:
    if func:
        assert os.path.exists(PATH_XLS_FILE_WITH_REPORTS) is True
