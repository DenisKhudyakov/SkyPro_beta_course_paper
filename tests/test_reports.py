import os.path
import pathlib
from typing import Any
from unittest.mock import patch

import pandas as pd
import pytest

from data.config import PATH_XLS_FILE_WITH_OPERATION, PATH_XLS_FILE_WITH_REPORTS
from src.reports import func, spending_by_category
from src.views import get_exel


@pytest.fixture()
def bank_data() -> Any:
    return get_exel(str(PATH_XLS_FILE_WITH_OPERATION))


def test_spending_by_category(bank_data: Any) -> None:
    result = spending_by_category(bank_data, category="Переводы", date="25.11.2019").to_dict(orient="records")
    assert len([i["Категория"] for i in result]) == 27
    result = spending_by_category(bank_data, category="Переводы").to_dict(orient="records")
    assert [i["Категория"] for i in result] == []


def test_report() -> None:
    if func:
        assert os.path.exists(PATH_XLS_FILE_WITH_REPORTS) is True
