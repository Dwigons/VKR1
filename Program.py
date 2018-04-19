#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

#import xlwt
from PyQt5.QtWidgets import * #QWidget, QCheckBox, QApplication
from PyQt5.QtCore import Qt
import json
import itertools

import TM1
import ExcelSave
import ExcelSaveLoad
#nso = int
nso = 0
# TM_1 = []
# TM_2 = [[]]
abraham = 0




class Example(QWidget):
    def createMas(self,a):
        ListToExtend = []
        i = 0
        while i < a:
            ListToExtend.append(0)
            i=i+1
        return (ListToExtend)
    def createMatrix(self, a, b):
        MatrixToCreate = [[0]*b for i in range(a)]
        return (MatrixToCreate)

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        cb = QCheckBox('Сквозное отверстие присутствует', self)
        cb.move(20, 20)
       # cb.toggle()
        #cb.isChecked(self.defineArrays)
        cb.stateChanged.connect(self.changeTitle)
        #cb.stateChanged.connect(self.defineArrays)

        self.setGeometry(300, 300, 800, 600)
        #self.setWindowTitle('')
        self.show()

    def defineArrays(self):
        TM_1 = self.createMatrix(32,1)
        TM_2 = self.createMatrix(30, 15)
        TM_3 = self.createMatrix(30, 15)
        TM_4 = self.createMatrix(30, 15)
        TMD = self.createMatrix(15,30)
        TMI = self.createMatrix(30,30)
        file = json.load(open('TM1.json'))
        #print(file)
        TM_1 = ExcelSaveLoad.prettify_table_data(TM_1,file)
        print (TM_1)
        ExcelSaveLoad.my_func('TM1',TM1)

       # file = json.load(open('TM2.json'))
       # TM_2 = ExcelSaveLoad.prettify_table_data(TM_2,file)
       # ExcelSaveLoad.my_func('TM2',TM2, 'TestArrays.xls')

    def listmerge(lstlst):
        all = []
        for lst in lstlst:
            all.extend(lst)
        return all
    def changeTitle(self, state):
        global nso
        if state == Qt.Checked:
            #print(TM_1)
            # TM_1=self.createMas(32)
            TM_1 = self.createMatrix(32,1)
            TM_2 = self.createMatrix(30,15)
            print(TM_2)
            print (TM_1)
           # TM_2=self.createMatrix(30)
            #TM_2[1][5] = 155
           #  file = json.load(open('TM1.json'))
           #  #print(file)
           #  #data = loads(obj)
           # # print(list(data))
           #  i=0
           #  for row in TM_1:
           #      TM_1[i].append(file[i][0])
           #      i = i+1
            # file.close()
           # TM_1 = ExcelSaveLoad.prettify_table_data(TM_1,file)
            TM_1 = ExcelSaveLoad.prettify_matrix_data(TM_1,'TM1.json')
            for index, value in enumerate(TM_1):
                print(f'{index}: {value}')

            TM_2 = ExcelSaveLoad.prettify_matrix_data(TM_2, 'TM2.json')
            for row_i, row in enumerate(TM_2):
                for column_i, value in enumerate(row):
                    print(row_i, column_i, value)

            ExcelSaveLoad.my_func('TM1',TM_1)
            ExcelSaveLoad.my_func('TM2',TM_2)
            print(TM_2)
            print(TM_1)
            #print(str(TM_1).encode('cp1251'))
            #TM_1=str(TM_1).encode('cp1251')
            print(len(TM_1))

            #read_data = ExcelSaveLoad.read_xls_from_file("ExcelSaveLoad.xls")
            #a=read_data['TM1']
            #a[18][0] = 15
            #print(a)
           # print(TM_2)
            #print(ExcelSave.ExportExcel.saveTM1(TM_1))
            #print(ExcelSave.ExportExcel.saveTM2(TM_2))
            #abraham = self.createMas(182)
            #print(len(abraham), abraham  )

            #print(TM1.algoritm(nso))
            nso = TM1.algoritm(nso)
            self.setWindowTitle(str(nso))



        else:
            nso = TM1.algoritm(nso)
            self.setWindowTitle(str(nso))


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())