import logging
import time


class GoogleSheetsHandler(logging.Handler):
    def __init__(self, worksheet, max_rows=1000):
        logging.Handler.__init__(self)
        self.worksheet = worksheet
        self.max_rows = max_rows

    def emit(self, record):
        log_entry = self.format(record)
        self.worksheet.insert_row([log_entry], 2)  # ログを2行目に挿入
        time.sleep(1)  # スプレッドシートAPIのリクエスト制限のため、待機

        num_rows = self.worksheet.row_count  # シートの総行数を取得
        if (
            num_rows > self.max_rows + 1
        ):  # 行数が最大行数を超えた場合、1002行目以降を削除
            self.worksheet.delete_rows(self.max_rows + 2, num_rows)
            time.sleep(1)
