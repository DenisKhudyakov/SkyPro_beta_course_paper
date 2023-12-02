import logging
from typing import Any

from data.config import PATH_LOGS


def setup_logger(name: str) -> Any:
    """Конфигурация логов"""
    logging.basicConfig(
        filename=PATH_LOGS, filemode="w+", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger(name)
