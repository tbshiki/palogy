import logging
import os
import sys
import traceback
import requests
from pathlib import Path
import time
from datetime import datetime, timedelta, timezone

LOGGER_WAIT_SEC = 1

JST = timezone(timedelta(hours=+9), "JST")


class GoogleSheetsHandler(logging.Handler):
    def __init__(self, worksheet, max_rows=1000):
        logging.Handler.__init__(self)
        self.worksheet = worksheet
        self.max_rows = max_rows

    def emit(self, record):
        log_entry = self.format(record)
        self.worksheet.insert_row([log_entry], 2)  # ログを2行目に挿入
        time.sleep(LOGGER_WAIT_SEC / 2)

        num_rows = self.worksheet.row_count  # シートの総行数を取得
        if (
            num_rows > self.max_rows + 1
        ):  # 行数が最大行数を超えた場合、1002行目以降を削除
            self.worksheet.delete_rows(self.max_rows + 2, num_rows)
            time.sleep(LOGGER_WAIT_SEC / 2)
        time.sleep(LOGGER_WAIT_SEC)  # スプレッドシートAPIのリクエスト制限のため、待機


class ExcelHandler(logging.Handler):
    def __init__(self, excel_sheet, max_rows=1000):
        logging.Handler.__init__(self)
        self.excel_sheet = excel_sheet
        self.max_rows = max_rows

    def emit(self, record):
        log_entry = self.format(record)
        sheet = self.excel_sheet

        # シートの2行目に新しい行を挿入
        sheet.range("2:2").api.EntireRow.Insert()
        sheet.range("A2").value = log_entry

        # シートの総行数を取得
        num_rows = sheet.cells.last_cell.row

        # 行数が最大行数を超えた場合、超過分の行を削除
        if num_rows > self.max_rows + 1:
            sheet.api.Rows(f"{self.max_rows + 2}:{num_rows}").Delete()


def send_image_line_notify(
    message_text: str, driver, tmp_dir: str, line_notify_token: str
):
    now_time = datetime.now(JST).strftime("%Y%m%d%H%M%S%f")
    save_screenshot_path = os.path.join(tmp_dir, "result" + str(now_time) + ".png")
    driver.save_screenshot(save_screenshot_path)

    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + line_notify_token}
    message = {"message": message_text}
    files = {"imageFile": open(save_screenshot_path, "rb")}

    line_notify = requests.post(
        line_notify_api, headers=headers, data=message, files=files
    )
    return line_notify.status_code


def send_line_notify(message_text: str, line_notify_token: str):
    line_notify_api = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": "Bearer " + line_notify_token}
    message = {"message": message_text}

    line_notify = requests.post(line_notify_api, headers=headers, data=message)
    return line_notify.status_code


def clear_existing_handlers(logger):
    while logger.handlers:
        handler = logger.handlers[0]
        logger.removeHandler(handler)
        handler.close()


def setup_mylogger(
    module_name,
    worksheet=None,
    excel_sheet=None,
    LINE_NOTIFY=False,
    line_notify_token=None,
    driver=None,
    tmp_dir=None,
):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    clear_existing_handlers(logger)  # 既存のハンドラをクリア

    sh_log = logging.StreamHandler()
    sh_log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s"
    )
    sh_log.setFormatter(formatter)
    logger.addHandler(sh_log)

    path_file_dir: str = str(Path(__file__).resolve().parents[1])
    log_folder = os.path.join(path_file_dir, "logs")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    log_file = os.path.join(
        log_folder, str(datetime.now(JST).strftime("%Y-%m-%d")) + "_logger.log"
    )
    if not os.path.exists(log_file):
        with open(log_file, "w") as f:
            pass

    fh_log = logging.FileHandler(log_file, encoding="utf-8")
    fh_log.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter(
        "%(asctime)s:%(name)s:%(lineno)d:%(levelname)s:%(message)s"
    )
    fh_log.setFormatter(fh_formatter)
    logger.addHandler(fh_log)

    if worksheet:
        gh_log = GoogleSheetsHandler(worksheet)
        gh_log.setLevel(logging.DEBUG)
        gh_log.setFormatter(formatter)
        logger.addHandler(gh_log)

    if excel_sheet:
        eh_log = ExcelHandler(excel_sheet)
        eh_log.setLevel(logging.DEBUG)
        eh_log.setFormatter(formatter)
        logger.addHandler(eh_log)

    def log_exception(exc_type, exc_value, exc_traceback):
        """カスタムの例外ハンドラ"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_str = "".join(tb_lines)
        filename = exc_traceback.tb_frame.f_code.co_filename
        lineno = exc_traceback.tb_lineno

        error_message = f"Uncaught exception in file {filename}, line {lineno}"
        logger.error(error_message)
        logger.error(tb_str)

        if line_notify_token:
            line_message = f"{error_message}\n{exc_value}"
            if LINE_NOTIFY and driver and tmp_dir:
                send_image_line_notify(line_message, driver, tmp_dir, line_notify_token)
            else:
                send_line_notify(line_message, line_notify_token)

    sys.excepthook = log_exception

    return logger


if __name__ == "__main__":
    pass
