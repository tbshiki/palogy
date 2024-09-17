import unittest
import logging
from palogy.logger import setup_mylogger, GoogleSheetsHandler, ExcelHandler
from unittest.mock import MagicMock


class TestPalogyLogger(unittest.TestCase):

    def setUp(self):
        """テスト前のセットアップ処理"""
        # Google SheetsやExcelシートのモックを作成
        self.mock_worksheet = MagicMock()
        self.mock_excel_sheet = MagicMock()

        # テスト用のロガーをセットアップ
        self.logger = setup_mylogger(
            "test_logger",
            worksheet=self.mock_worksheet,
            excel_sheet=self.mock_excel_sheet,
            LINE_NOTIFY=False,
        )

    def test_google_sheets_handler(self):
        """Google Sheets Handlerへのログ挿入をテスト"""
        self.logger.info("This is a test log for Google Sheets")

        # Google Sheetsにログが挿入されているか確認
        self.mock_worksheet.insert_row.assert_called_once()

    def test_excel_handler(self):
        """Excel Handlerへのログ挿入をテスト"""
        self.logger.debug("This is a test log for Excel")

        # Excelシートにログが挿入されているか確認
        self.mock_excel_sheet.range().api.EntireRow.Insert.assert_called_once()
        self.mock_excel_sheet.range().value = "This is a test log for Excel"

    def test_file_logging(self):
        """ファイルロギングのテスト"""
        with self.assertLogs(self.logger, level="DEBUG") as log:
            self.logger.debug("Test log for file")

        # ログメッセージが出力されたか確認
        self.assertIn("Test log for file", log.output[0])

    def test_stream_logging(self):
        """標準出力へのロギングをテスト"""
        with self.assertLogs(self.logger, level="INFO") as log:
            self.logger.info("Stream log test")

        # ログメッセージが出力されたか確認
        self.assertIn("Stream log test", log.output[0])

    def test_exception_logging(self):
        """例外処理のロギングテスト"""
        try:
            raise ValueError("Test exception")
        except Exception as e:
            self.logger.exception("Exception occurred")

        # ファイルまたは標準出力に例外ログが記録されているか確認
        with self.assertLogs(self.logger, level="ERROR") as log:
            self.logger.error("Exception occurred")

        self.assertIn("Exception occurred", log.output[0])


if __name__ == "__main__":
    unittest.main()
