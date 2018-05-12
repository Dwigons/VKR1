import json
from pathlib import Path

import xlwt
import xlrd
from xlutils.copy import copy as copy_excel

# PEP8 - прочитать

XLS_FILE_PATH = 'Arrays.xls'


def read_xls_from_file(file_path):
    result = {}

    with xlrd.open_workbook(file_path) as file:
        sheets = file.sheets()

        for sheet in sheets:
            sheet_name = sheet.name
            result[sheet_name] = []
            for row_i in range(sheet.nrows):
                row_data = [cell.value for cell in sheet.row(row_i)]
                result[sheet_name].append(row_data)

    return result


def prettify_table_data(add_data, data):
    """ function """
    if len(add_data) != len(data):
        raise ValueError

    result = [
        [param_name] + param_values
        for param_name, param_values in zip(add_data, data)
    ]
    return result
def prettify_matrix_data(data, json_file_path):
    file = 0
    file = json.load(open(json_file_path))
    i = 0
    for row in data:
        data[i].append(file[i][0])
        i = i + 1
    print(file)
    return data

def my_func(sheet_name, sheet_data, XLS_FILE_PATH):
    if Path(XLS_FILE_PATH).is_file():
        # print('1')
        book = xlrd.open_workbook(XLS_FILE_PATH)
        print(sheet_name)
        if any(map(lambda v: v in sheet_name, book.sheet_names())):#Check exists of list in file
            book = copy_excel(book)
            edited_sheet = book.get_sheet(sheet_name)
        else:#Create list if not in file
            book = copy_excel(book)
            edited_sheet = book.add_sheet(sheet_name)
    else:
        book = xlwt.Workbook()
        edited_sheet = book.add_sheet(sheet_name)

    for row_i, row in enumerate(sheet_data):
        for column_i, value in enumerate(row):
            edited_sheet.write(row_i, column_i, value)


    # print('2')
    book.save(XLS_FILE_PATH)


if __name__ == '__main__':
    print('Hello')
    # sys.exit(app.exec_())
    # file_data = read_xls_from_file('meow.xls')
    # print(list(file_data.keys()))
    # print(file_data['TM2'])
    # file = json.load(open('dataset.json'))
    # data = json.loads(obj)
#     my_func(file)
