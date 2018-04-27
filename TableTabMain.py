from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout
from PyQt5.QtCore import QSize, Qt, QRect
import json
import Initialisation




# Наследуемся от QMainWindow
class Tab_Widget(QMainWindow):
    XLS_FILE_PATH = 'default.xls'
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        super(Tab_Widget,self).__init__()
        self.tabUI = TabUI(self)
        # self.secondWin = SecondWindow()

        self.setMinimumSize(QSize(1100, 1000))  # Устанавливаем размеры
        self.setWindowTitle("Заполнение матриц")  # Устанавливаем заголовок окна

        BXlayout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        newM = QAction("New", self)
        file.addAction(newM)

        loadM = QAction("Load", self)
        file.addAction(loadM)

        file.triggered[QAction].connect(self.processtrigger)
        self.setLayout(BXlayout)

        self.setCentralWidget(self.tabUI)  # Устанавливаем центральный виджет



    # def InitialisationAlertWindow(self, q):



    def processtrigger(self,q):
        if q.text() == 'New':
            a = True
            while a:
                fname = QFileDialog.getExistingDirectory(self, 'Select directory')
                if fname != '':
                    fname += '/'
                    text, ok = QInputDialog.getText(self, fname,
                                                    'Enter file name:')
                    text = fname + text +'.xls'
                    if ok:
                        buttonReply = QMessageBox.question(self, 'Success', "File path: "+text,
                                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        if buttonReply == QMessageBox.Yes:
                            Initialisation.defineArrays(text)
                            Tab_Widget.XLS_FILE_PATH = text
                            a = False
                        elif buttonReply == QMessageBox.No:
                            a = False
                    else:
                        a = False
                else:
                    a = False

        if q.text() == "Load":

            fname = QFileDialog.getOpenFileName(self, 'Open file',
                                                '', "Excel files (*.xls) ")  #Создаем окно выбора файла
            if fname != ('',''):
                print(fname)
                Tab_Widget.XLS_FILE_PATH = fname[0]
                Array = Initialisation.ExcelSaveLoad.read_xls_from_file(fname[0])
                Tm1 = Array['TM1']
                #TabUI.updateTM1(Tm1)

                for i in range(len(Tm1)):
                    TabUI.table.setItem(i, 1, QTableWidgetItem(str(round(int(Tm1[i][0]), 0))))

            else:
                pass







class TabUI(QTabWidget):

    def __init__(self, parent):
        # Обязательно нужно вызвать метод супер класса
        super(TabUI,self).__init__(parent)

        self.initUI()

    def initUI(self):



        self.tab = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.addTab(self.tab1, "TM1")
        self.addTab(self.tab2, "TM2")
        self.addTab(self.tab3, "TM3")

        self.tab1f()
        self.tab2f()
        self.tab3f()

    def updateTM1(Tm1):
        for i in range(len(Tm1)):
            TabUI.table.setItem(i, 1, QTableWidgetItem(int(Tm1[i][0])))
        print ('upd')

    def tab1f(self):
        # arrr = Initialisation.ExcelSaveLoad.read_xls_from_file('KUKISH.xls')
        # print
        TabUI.aba= 154
        grid_layout = QGridLayout()  # Создаём QGridLayout
        # central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        TabUI.table = QTableWidget(self)  # Создаём таблицу
        # self.table.setGeometry(0,0,960,1000)
        self.table.setColumnCount(3)  # Устанавливаем три колонки
        self.table.setRowCount(32)  # и одну строку в таблице

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(["Имя парметра", "Значение", "Примечание"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("Column 1 ")
        self.table.horizontalHeaderItem(1).setToolTip("Column 2 ")
        self.table.horizontalHeaderItem(2).setToolTip("Column 3 ")

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        self.table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.table.horizontalHeaderItem(2).setTextAlignment(Qt.AlignRight)

        # заполняем первый столбец

        file = json.load(open('Dataset/TM1.json'))
        for i in range(len(file)):
            self.table.setItem(i, 0, QTableWidgetItem(str(file[i][0])))

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

        grid_layout.addWidget(self.table, 0, 0)  # Добавляем таблицу в сетку


        self.saveb = QPushButton('Сохранить', self)
        self.proba = QPushButton('Проба', self)
        self.proba.setCheckable(False)
        self.saveb.setCheckable(False)
        self.saveb.move(980, 950)
        self.proba.move(980, 900)

        # self.saveb.setGeometry(1000, 1000, 20, 25)
        grid_layout.addWidget(self.saveb,80, 60)
        grid_layout.addWidget(self.proba, 100, 60)

        self.saveb.clicked.connect(self.getData)

        self.setTabText(0, "TM1")
        self.tab1.setLayout(grid_layout)


    def tab2f(self):

        # tabTM2 = QTabWidget()
        # tabTM21 = QWidget()
        # tabTM22 = QWidget()
        #
        # tabTM2.addTab(tabTM21, "1")
        # tabTM2.addTab(tabTM22, "2")
        # tablayout = QVBoxLayout()
        # tabTM2.setLayout(tablayout)
        # tabTM2.setLayout(tablayout)

        # TabUI.tabTM21f()
        # TabUI.tabTM22f()

    # def tabTM21f():

        r = QRect(0, 0,130,130)

        layout = QGridLayout()
        Vlayout = QVBoxLayout()
        Hlay = QHBoxLayout()
        Hlay2 = QHBoxLayout()

        D = QLabel('Диаметр')
        P = QLabel('Посадка')
        HTO = QLabel('Химико-термическая обработка')
        # for i in range(9):
        #     layout.setColumnStretcn(0,i)
        layout.setGeometry(r)
        layout.addWidget(D, 0, 29, Qt.AlignRight|Qt.AlignTop)
        layout.addWidget(QLineEdit(), 0, 30, Qt.AlignRight|Qt.AlignTop)
        layout.addWidget(P, 1,29, Qt.AlignRight|Qt.AlignTop)
        layout.addWidget(QLineEdit(),1,30, Qt.AlignRight|Qt.AlignTop)
        layout.addWidget(HTO, 2, 29, Qt.AlignRight|Qt.AlignTop)
        layout.addWidget(QLineEdit(),2, 30, Qt.AlignRight|Qt.AlignTop)
        layout.setSpacing(0)
        # layout.addWidget(Hlay)


        # layout.addWidget(QLabel("Name"))
        # layout.addWidget(QLineEdit())
        # layout.addWidget(QLabel("Address"))
        # layout.addWidget(QLineEdit())
        # Hlay.addWidget(QLineEdit())
        # Hlay.addLayout(Vlayout)
        # Hlay2.addLayout(Vlayout)
        # Vlayout.addLayout(layout)
        # Vlayout.addLayout(layout)
        # Hlay.addLayout(layout)
        # Hlay2.addLayout(layout)

        # tabTM21.setLayout(layout)
        self.tab2.setLayout(layout)

    # def tabTM22f():
    #     layout = QFormLayout()
    #     layout.addRow("Пиши тут", QLineEdit())
    #     layout.addRow("и тут", QLineEdit())
    #     # TabUI.setTabText(2, "TM3")
    #     TabUI.tabTM22.setLayout(layout)
    #
    def tab3f(self):

        layout = QFormLayout()
        layout.addRow("Пиши тут", QLineEdit())
        layout.addRow("и тут", QLineEdit())
        self.setTabText(2, "TM3")
        self.tab3.setLayout(layout)

#выводим данные из таблицы

    def getData(self):
        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(1,cols-1):
                try:
                    tmp.append(self.table.item(row, col).text())
                except:
                    tmp.append(0)
            data.append(tmp)
        # for i in data: data[i] = int(data[i])
        print(Tab_Widget.XLS_FILE_PATH)
        Initialisation.ExcelSaveLoad.my_func('TM1', data, Tab_Widget.XLS_FILE_PATH)
        print(data)
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())