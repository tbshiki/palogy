import logging
import time
import requests


class GoogleSheetsHandler(logging.Handler):
    def __init__(
        self, worksheet=None, max_rows=1000, use_webhook=False, webhook_url=None
    ):
        logging.Handler.__init__(self)
        self.worksheet = worksheet
        self.max_rows = max_rows
        self.use_webhook = use_webhook
        self.webhook_url = webhook_url

    def emit(self, record):
        log_entry = self.format(record)

        if self.use_webhook and self.webhook_url:
            # Webhook経由でログを送信
            try:
                params = {
                    "functionName": "appendLogToSheet",  # GASで定義した関数名
                    "sheetName": "log",  # 変更可能、GASで定義したシート名
                    "logEntry": log_entry,
                    "maxRows": self.max_rows,
                }
                response = requests.post(self.webhook_url, data=params)

                # レスポンスのステータスコードと内容をデバッグ出力
                if response.status_code != 200:
                    print(f"Webhook failed: {response.status_code}, {response.text}")
                else:
                    print(f"Webhook success: {response.status_code}, {response.text}")

            except Exception as e:
                print(f"Failed to send log via webhook: {e}")
        elif self.worksheet:
            # Google Sheets API経由で直接ログを挿入
            self.worksheet.insert_row([log_entry], 2)  # ログを2行目に挿入
            time.sleep(1)

            num_rows = self.worksheet.row_count  # シートの総行数を取得
            time.sleep(1)

            if (
                num_rows > self.max_rows + 1
            ):  # 行数が最大行数を超えた場合、1002行目以降を削除
                try:
                    self.worksheet.delete_rows(self.max_rows + 2, num_rows)
                    time.sleep(1)
                except Exception as e:
                    print(f"Failed to delete rows: {e}")

            time.sleep(1)  # スプレッドシートAPIのリクエスト制限のため、待機
        else:
            print("No worksheet or webhook URL specified.")
