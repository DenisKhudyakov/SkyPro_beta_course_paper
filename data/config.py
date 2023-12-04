from pathlib import Path

ROOT_PATH = Path(__file__).parent
PATH_XLS_FILE_WITH_OPERATION = ROOT_PATH.joinpath("operations.xls")
PATH_XLS_FILE_WITH_REPORTS = ROOT_PATH.joinpath("reports.xls")
PATH_LOGS = ROOT_PATH.joinpath("logs.log")
USER_SETTINGS = ROOT_PATH.joinpath("user_settings.json")
