import sys
import logging


def setup_logger(logger_name: str, verbose: bool) -> None:
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger_handler = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('%(asctime)s: %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(formatter)
    logger.addHandler(logger_handler)
