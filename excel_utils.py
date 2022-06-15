import pandas as pd
import xlrd
import xlwt
from xlutils.copy import copy


class WriteExcel(object):
    def __init__(self):
        self.workbook = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.workbook.add_sheet('sheet1')

    def add(self, start_row, end_row, start_col, end_col, data):
        self.sheet.write_merge(start_row, end_row, start_col, end_col, data)

    def save(self, file_name):
        self.workbook.save(file_name)


class ChangeExcel(object):
    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.old_book = xlrd.open_workbook(excel_path, formatting_info=True)
        self.new_excel = copy(self.old_book)
        self.ws = self.new_excel.get_sheet(0)

    def change(self, row, col, data):
        self.ws.write(row, col, data)

    def save(self, file_name=None):
        file_name = file_name or self.excel_path
        self.new_excel.save(file_name)


def excel_to_list_ffill(excel_path):
    old_excel_data = pd.read_excel(excel_path, dtype=str, sheet_name=0)
    old_excel_data.replace('\n', '', regex=True, inplace=True)
    old_excel_data.fillna(method='ffill', inplace=True)
    old_excel_data_list = old_excel_data.values.tolist()
    return old_excel_data_list
