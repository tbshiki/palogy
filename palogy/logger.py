import logging
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone
import sys
import traceback

from .google_sheets_handler import GoogleSheetsHandler
from .excel_handler import ExcelHandler

JST = timezone(timedelta(hours=+9), "JST")


def clear_existing_handlers(logger):
    while logger.handlers:
        handler = logger.handlers[0]
        logger.removeHandler(handler)
        handler.close()


def setup_mylogger(module_name, worksheet=None, excel_sheet=None):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    clear_existing_handlers(logger)

    sh_log = logging.StreamHandler()
    sh_log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s"
    )
    sh_log.setFormatter(formatter)
    logger.addHandler(sh_log)

    # ファイルロガーの設定
    path_file_dir: str = str(Path(__file__).resolve().parents[1])
    log_folder = os.path.join(path_file_dir, "logs")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(
        log_folder, str(datetime.now(JST).strftime("%Y-%m-%d")) + "_logger.log"
    )
    fh_log = logging.FileHandler(log_file, encoding="utf-8")
    fh_log.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s"
    )
    fh_log.setFormatter(fh_formatter)
    logger.addHandler(fh_log)

    # Google Sheets ハンドラ
    if worksheet:
        gh_log = GoogleSheetsHandler(worksheet)
        gh_log.setLevel(logging.DEBUG)
        gh_log.setFormatter(formatter)
        logger.addHandler(gh_log)

    # Excel ハンドラ
    if excel_sheet:
        eh_log = ExcelHandler(excel_sheet)
        eh_log.setLevel(logging.DEBUG)
        eh_log.setFormatter(formatter)
        logger.addHandler(eh_log)

    return logger
