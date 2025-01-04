import logging
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

from .google_sheet_handler import GoogleSheetsHandler
from .excel_handler import ExcelHandler

JST = timezone(timedelta(hours=+9), "JST")


def setup_mylogger(module_name, worksheet=None, excel_sheet=None):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # ハンドラーが既に設定されている場合は何もしない
    if logger.handlers:
        return logger

    # StreamHandler の設定
    sh_log = logging.StreamHandler()
    sh_log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s"
    )
    sh_log.setFormatter(formatter)
    logger.addHandler(sh_log)

    # ファイルロガーの設定
    path_file_dir = Path(__file__).resolve().parents[1]
    log_folder = path_file_dir / "logs"
    log_folder.mkdir(exist_ok=True)  # フォルダが存在しない場合は作成
    log_file = log_folder / f"{module_name}_{datetime.now(JST).strftime('%Y%m%d')}.log"
    fh_log = logging.FileHandler(log_file, encoding="utf-8")
    fh_log.setLevel(logging.DEBUG)
    fh_log.setFormatter(formatter)
    logger.addHandler(fh_log)

    # Google Sheets ハンドラーの設定
    if worksheet:
        gs_handler = GoogleSheetsHandler(worksheet)
        gs_handler.setLevel(logging.ERROR)  # 必要に応じてレベルを調整
        logger.addHandler(gs_handler)

    # Excel ハンドラーの設定
    if excel_sheet:
        excel_handler = ExcelHandler(excel_sheet)
        excel_handler.setLevel(logging.WARNING)  # 必要に応じてレベルを調整
        logger.addHandler(excel_handler)

    return logger
