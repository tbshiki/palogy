import unittest
from unittest.mock import MagicMock
from palogy.google_sheets_handler import GoogleSheetsHandler
import logging


class TestGoogleSheetsHandler(unittest.TestCase):

    def setUp(self):
        # Google Sheetsのモックオブジェクトを作成
        self.mock_worksheet = MagicMock()
        self.handler = GoogleSheetsHandler(self.mock_worksheet, max_rows=1000)
        self.logger = logging.getLogger("test_google_sheets_logger")
        self.logger.addHandler(self.handler)

    def test_emit(self):
        # ログメッセージをGoogle Sheetsに挿入するテスト
        self.logger.info("Test log for Google Sheets")

        # insert_rowが呼び出されたか確認
        self.mock_worksheet.insert_row.assert_called_once()
        args = self.mock_worksheet.insert_row.call_args[0]
        self.assertIn("Test log for Google Sheets", args[0][0])

    def test_delete_rows_when_exceeds_max(self):
        # シートの総行数が制限を超えた時の動作をテスト
        self.mock_worksheet.row_count = 1005  # シートが最大行数を超えていると仮定
        self.logger.info("Log to trigger row deletion")

        # delete_rowsが呼び出されたことを確認
        self.mock_worksheet.delete_rows.assert_called_with(1002, 1005)


if __name__ == "__main__":
    unittest.main()
