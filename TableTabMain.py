from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout
from PyQt5.QtCore import QSize, Qt, QRect
import json
import Initialisation, ChoosePic




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


                for i in range(len(Tm1)):
                    TabUI.table.setItem(i, 1, QTableWidgetItem(str(round(int(Tm1[i][0]), 0))))

            else:
                pass

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()






class TabUI(QTabWidget):

    image = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

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


    def tab1f(self):

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


        self.saveb = QPushButton('Далее', self)
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


        layout = QHBoxLayout()
        Vlayout = QVBoxLayout()

        a = 'Работает'
        l = QLabel()
        l.setText(a)
        layout.addWidget(l)

        self.B1 = QPushButton('1 слой', self)
        self.B1.clicked.connect(self.Pic)
        print(a)

        # l.setIcon()

        self.B2 = QPushButton('2 слой')
        # self.B2.clicked.connect(self.Pic(2))

        self.B3 = QPushButton('3 слой')
        # self.B3.clicked.connect(self.Pic(3))

        self.B4 = QPushButton('4 слой')
        self.B5 = QPushButton('5 слой')
        self.B6 = QPushButton('6 слой')
        self.B7 = QPushButton('7 слой')
        self.B8 = QPushButton('8 слой')
        self.B9 = QPushButton('9 слой')
        self.B10 = QPushButton('10 слой')
        self.B11 = QPushButton('11 слой')
        self.B12 = QPushButton('12 слой')
        self.B13 = QPushButton('13 слой')
        self.B14 = QPushButton('14 слой')
        self.B15 = QPushButton('15 слой')

        Vlayout.addWidget(self.B1)
        Vlayout.addWidget(self.B2)
        Vlayout.addWidget(self.B3)
        Vlayout.addWidget(self.B4)
        Vlayout.addWidget(self.B5)
        Vlayout.addWidget(self.B6)
        Vlayout.addWidget(self.B7)
        Vlayout.addWidget(self.B8)
        Vlayout.addWidget(self.B9)
        Vlayout.addWidget(self.B10)
        Vlayout.addWidget(self.B11)
        Vlayout.addWidget(self.B12)
        Vlayout.addWidget(self.B13)
        Vlayout.addWidget(self.B14)
        Vlayout.addWidget(self.B15)



        Vlayout.addStretch(1)
        layout.addStretch(1)
        layout.addLayout(Vlayout)



        self.setTabText(1,"TM2")
        self.tab2.setLayout(layout)


    def tab3f(self):

        layout = QFormLayout()
        layout.addRow("Пиши тут", QLineEdit())
        layout.addRow("и тут", QLineEdit())
        self.setTabText(2, "TM3")
        self.tab3.setLayout(layout)

    #выводим данные из таблицы
    def Message(self):
        buttonReply = QMessageBox.warning(self, 'Failed', "You must enter data in the table",
                                          QMessageBox.Close, QMessageBox.Close)

    def getData(self):
        if Tab_Widget.XLS_FILE_PATH == 'default.xls':
            text, ok = QInputDialog.getText(self, 'Save file',
                                            'Enter file name:')
            Tab_Widget.XLS_FILE_PATH = text + '.xls'
            Initialisation.defineArrays(Tab_Widget.XLS_FILE_PATH)
            if not ok:
                Tab_Widget.XLS_FILE_PATH = 'default.xls'



        rows = self.table.rowCount()
        cols = self.table.columnCount()
        data = []
        for row in range(rows):
            tmp = []
            for col in range(1,cols-1):
                try:
                    tmp.append(self.table.item(row, col).text())
                except:
                    tmp.append('0')
            data.append(tmp)
        Initialisation.ExcelSaveLoad.my_func('TM1', data, Tab_Widget.XLS_FILE_PATH)
        try:
            sum = int(self.table.item(12, 1).text())+int(self.table.item(13, 1).text())+int(self.table.item(14, 1).text())+int(self.table.item(15, 1).text())+2
            if self.table.item(18, 1).text() == '1':
                sum += 1
            print(sum)

            for i in range(1, sum):
                print(ChoosePic.ChoosePic(data, i))
                TabUI.image[i-1] = ChoosePic.ChoosePic(data, i)
            print(data)
            print(TabUI.image)

        except:
            self.Message()

    def Pic(self):

        sender = self.sender()
        t = sender.text()
        if t == '1 слой':
            print(TabUI.image[0])
            return TabUI.image[0]
        elif t == '2':
            return TabUI.image[1]
        elif t == '3':
            return TabUI.image[2]
        elif t == 4:
            return TabUI.image[3]
        elif t == 5:
            return TabUI.image[4]
        elif t == 6:
            return TabUI.image[5]
        elif t == 7:
            return TabUI.image[6]
        elif t == 8:
            return TabUI.image[7]
        elif t == 9:
            return TabUI.image[8]
        elif t == 10:
            return TabUI.image[9]
        elif t == 11:
            return TabUI.image[10]
        elif t == 12:
            return TabUI.image[11]
        elif t == 13:
            return TabUI.image[12]
        elif t == 14:
            return TabUI.image[13]
        elif t == 15:
            return TabUI.image[14]

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())