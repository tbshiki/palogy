import unittest
from unittest.mock import MagicMock
from palogy.excel_handler import ExcelHandler
import logging


class TestExcelHandler(unittest.TestCase):

    def setUp(self):
        # Excelのモックオブジェクトを作成
        self.mock_excel_sheet = MagicMock()
        self.handler = ExcelHandler(self.mock_excel_sheet, max_rows=1000)
        self.logger = logging.getLogger("test_excel_logger")
        self.logger.addHandler(self.handler)

    def test_emit(self):
        # ログメッセージをExcelシートに挿入するテスト
        self.logger.info("Test log for Excel")

        # Excelシートへの挿入が正しく行われたか確認
        self.mock_excel_sheet.range().api.EntireRow.Insert.assert_called_once()
        self.mock_excel_sheet.range("A2").value = "Test log for Excel"

    def test_delete_rows_when_exceeds_max(self):
        # 行数が最大を超えた時の行削除をテスト
        self.mock_excel_sheet.cells.last_cell.row = 1005  # 最大行数を超えていると仮定
        self.logger.info("Log to trigger row deletion")
