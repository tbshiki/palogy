import logging


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
