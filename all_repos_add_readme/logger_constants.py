import os
import colorama
from enum import Enum
from time import time

# local modules
from all_repos_add_readme.constants import Constants


class LoggerConstants:
    # log constants
    TOOL_LOGGER_NAME = 'logger'
    TOOL_DEFAULT_LOGFILE_DIR = os.path.join(Constants.BASE_DIR, 'logs')
    if not os.path.isdir(TOOL_DEFAULT_LOGFILE_DIR):  # pragma: no cover
        os.mkdir(TOOL_DEFAULT_LOGFILE_DIR)

    ROTATING_FILE_HANDLER_BACKUP_COUNT = 5

    @property
    def tool_default_logfile_name(self) -> str:
        return f'logfile_{round(time())}.log'


class LoggerColoring(Enum):
    colorama.init()
    GREEN = colorama.Fore.GREEN
    RESET_SEQ = colorama.Style.RESET_ALL
