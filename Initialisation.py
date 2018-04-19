import sys
import ExcelSaveLoad


def createMatrix(a, b): #Создание массива а - строки, б- столбцы
    MatrixToCreate = [[0] * b for i in range(a)]
    return (MatrixToCreate)

def defineArrays(XLS_FILE_PATH): #Инициализация всех массивов
    TM_A = createMatrix(4,1)
    TM_1 = createMatrix(32, 1)
    TM_2 = createMatrix(30, 15)
    TM_3 = createMatrix(30, 15)
    TM_4 = createMatrix(30, 15)
    TMD = createMatrix(15, 30)
    TMI = createMatrix(30, 30)

    TM_A = ExcelSaveLoad.prettify_matrix_data(TM_A, 'Dataset/TMA.json')
    TM_1 = ExcelSaveLoad.prettify_matrix_data(TM_1, 'Dataset/TM1.json')
    TM_2 = ExcelSaveLoad.prettify_matrix_data(TM_2, 'Dataset/TM2.json')
    TM_3 = ExcelSaveLoad.prettify_matrix_data(TM_3, 'Dataset/TM3.json')
    TM_4 = ExcelSaveLoad.prettify_matrix_data(TM_4, 'Dataset/TM4.json')
    TMD = ExcelSaveLoad.prettify_matrix_data(TMD, 'Dataset/TMD.json')
    TMI = ExcelSaveLoad.prettify_matrix_data(TMI, 'Dataset/TMI.json')

    ExcelSaveLoad.my_func('TMA', TM_A, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TM1', TM_1, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TM2', TM_2, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TM3', TM_3, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TM4', TM_4, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TMD', TMD, XLS_FILE_PATH)
    ExcelSaveLoad.my_func('TMI', TMI, XLS_FILE_PATH)

    # ExcelSaveLoad.my_func('TM1', TM_3)


if __name__ == '__main__':
    defineArrays('arr2.xls')
    sys.exit()
