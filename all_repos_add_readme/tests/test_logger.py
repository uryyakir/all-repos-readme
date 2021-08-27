import tempfile
import logging
import os
import re
# local modules
from all_repos_add_readme._logger import setup_logger
from all_repos_add_readme._logger import shutdown_logging
from all_repos_add_readme.constants import LoggerConstants
from all_repos_add_readme.github_utils import github_api
from conftest import Constants


def test_logger_auto_generated_namings(constants: Constants) -> None:
    with tempfile.TemporaryDirectory(dir=LoggerConstants.TOOL_DEFAULT_LOGFILE_DIR) as tmpdir:
        for _ in range(constants.LOGFILES_ITERATION_COUNTER):
            setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=False, log_file_name=LoggerConstants().tool_default_logfile_name, logs_directory=tmpdir)
            github_api.main(user_input=None, dry_run=True, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)

        assert len(os.listdir(tmpdir)) == constants.LOGFILES_ITERATION_COUNTER  # check total files created
        assert len(
            set(
                map(
                    lambda text: re.search(r'\d+', text).group(0),  # type: ignore
                    os.listdir(tmpdir),
                ),
            ),
        ) == constants.LOGFILES_ITERATION_COUNTER  # check total unique timestamps

        shutdown_logging()


def test_logger_custom_log_namings(constants: Constants) -> None:
    with tempfile.TemporaryDirectory(dir=LoggerConstants.TOOL_DEFAULT_LOGFILE_DIR) as tmpdir:
        for _ in range(constants.LOGFILES_ITERATION_COUNTER):
            setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=False, log_file_name=constants.CUSTOM_LOGFILE_NAME, logs_directory=tmpdir)
            github_api.main(user_input=None, dry_run=True, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
            shutdown_logging()

        assert len(os.listdir(tmpdir)) == constants.LOGFILES_ITERATION_COUNTER  # check total files created
        assert sorted(os.listdir(tmpdir)) == sorted([constants.CUSTOM_LOGFILE_NAME, f'{constants.CUSTOM_LOGFILE_NAME}.1'])  # check that suffix is properly added as file extension


def test_rotating_file_handler_backup_count_overflow(constants: Constants) -> None:
    with tempfile.TemporaryDirectory(dir=LoggerConstants.TOOL_DEFAULT_LOGFILE_DIR) as tmpdir:
        for _ in range(LoggerConstants.ROTATING_FILE_HANDLER_BACKUP_COUNT + 5):
            setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=False, log_file_name=constants.CUSTOM_LOGFILE_NAME, logs_directory=tmpdir)
            github_api.main(user_input=None, dry_run=True, _test_patterns_lst=constants.ONLY_TEST_AGAINST_REPO_FILTER)
            shutdown_logging()

        assert len(os.listdir(tmpdir)) == LoggerConstants.ROTATING_FILE_HANDLER_BACKUP_COUNT + 1  # check total files created, should be equal to total backups + 1 (original)
        # assert the all of the numbers from 1 to `LoggerConstants.ROTATING_FILE_HANDLER_BACKUP_COUNT` appear as file extension suffixes
        assert sorted(
            list(
                map(
                    lambda text: re.search(r'\d$', text).group(0),  # type: ignore
                    [file_ for file_ in os.listdir(tmpdir) if file_ != constants.CUSTOM_LOGFILE_NAME],
                ),
            ),
        ) == list(
            map(
                str,
                sorted(
                    range(1, LoggerConstants.ROTATING_FILE_HANDLER_BACKUP_COUNT + 1),
                ),
            ),
        )


def test_verbose_changes_logger_level(constants: Constants) -> None:
    with tempfile.TemporaryDirectory(dir=LoggerConstants.TOOL_DEFAULT_LOGFILE_DIR) as tmpdir:
        setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=False, log_file_name=constants.CUSTOM_LOGFILE_NAME, logs_directory=tmpdir)
        logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)
        verbose_false_logging_level = logger.level
        shutdown_logging()
        setup_logger(logger_name=LoggerConstants.TOOL_LOGGER_NAME, verbose=True, log_file_name=constants.CUSTOM_LOGFILE_NAME, logs_directory=tmpdir)
        logger = logging.getLogger(LoggerConstants.TOOL_LOGGER_NAME)
        verbose_true_logging_level = logger.level

        assert verbose_false_logging_level > verbose_true_logging_level
        shutdown_logging()
