import unittest
from unittest.mock import MagicMock
from palogy.logger import setup_mylogger
import logging


class TestSetupMyLogger(unittest.TestCase):

    def setUp(self):
        # Google Sheets と Excel のモックオブジェクトを作成
        self.mock_worksheet = MagicMock()
        self.mock_excel_sheet = MagicMock()

    def test_logger_with_google_sheets(self):
        # Google Sheetsハンドラ付きのロガーをテスト
        logger = setup_mylogger("test_google_logger", worksheet=self.mock_worksheet)
        logger.info("Test Google Sheets logging")

        # Google Sheetsのinsert_rowが呼び出されたことを確認
        self.mock_worksheet.insert_row.assert_called_once()

    def test_logger_with_excel(self):
        # Excelハンドラ付きのロガーをテスト
        logger = setup_mylogger("test_excel_logger", excel_sheet=self.mock_excel_sheet)
        logger.debug("Test Excel logging")

        # Excelシートへの挿入が行われたことを確認
        self.mock_excel_sheet.range().api.EntireRow.Insert.assert_called_once()

    def test_file_logging(self):
        # ファイルロギングのテスト
        logger = setup_mylogger("test_file_logger")
        with self.assertLogs(logger, level="DEBUG") as log:
            logger.debug("Test log for file")

        # ファイルへのログ出力が正しく行われているか確認
        self.assertIn("Test log for file", log.output[0])

    def test_stream_logging(self):
        # 標準出力へのログ出力をテスト
        logger = setup_mylogger("test_stream_logger")
        with self.assertLogs(logger, level="INFO") as log:
            logger.info("Test stream logging")

        # 標準出力へのログ出力が行われているか確認
        self.assertIn("Test stream logging", log.output[0])


if __name__ == "__main__":
    unittest.main()
