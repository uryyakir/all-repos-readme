from typing import Optional
import os
import sys
import logging
import logging.handlers
# local modules
from all_repos_add_readme.constants import TOOL_DEFAULT_LOGFILE_DIR


def setup_logger(logger_name: str, verbose: bool, log_file_name: Optional[str]) -> None:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    if log_file_name:
        # user requested the logger to log to a file
        _log_filename = os.path.join(TOOL_DEFAULT_LOGFILE_DIR, log_file_name)
        _should_rollover = os.path.isfile(_log_filename)
        logger_handler = logging.handlers.RotatingFileHandler(
            filename=_log_filename,
            maxBytes=5*1024*1024,
            mode='w',
            backupCount=10,
        )
        if _should_rollover:
            logger_handler.doRollover()

    else:
        logger_handler = logging.StreamHandler(sys.stderr)

    formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger_handler.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.addHandler(logger_handler)
