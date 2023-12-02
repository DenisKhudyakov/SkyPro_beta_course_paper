import json

from data.config import PATH_XLS_FILE_WITH_OPERATION, USER_SETTINGS
from src.utils import filter_operation, main_struct, read_xls_file

if __name__ == "__main__":
    with open(USER_SETTINGS) as f:
        result = json.load(f)
    print(main_struct(filter_operation(read_xls_file(PATH_XLS_FILE_WITH_OPERATION), date_="27.11.2019"), settings=result))
