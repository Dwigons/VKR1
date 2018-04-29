from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap
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

        self.setMinimumSize(QSize(1100, 700))  # Устанавливаем размеры
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


        layout = QGridLayout()
        r = QRect(0,0,5,30)
        layout.setGeometry(r)

        self.l = QLabel()
        self.e1 = QLineEdit()
        self.D =  QLabel('Номинальный диаметр')
        self.e2 = QLineEdit()
        self.P = QLabel('Посадка')
        self.e3 = QLineEdit()
        self.K = QLabel('Номер квалитета')
        self.ES = QFormLayout()
        self.e4 = QLineEdit()
        self.ES = QLabel('Верхнее отклонение')
        self.e5 = QLineEdit()
        self.EI = QLabel('Нижнее отклонение')
        self.e6 = QLineEdit()
        self.SH = QLabel('Величина параметра шероховатость')
        self.e7 = QLineEdit()
        self.OT = QLabel('Особые требования')
        self.e8 = QLineEdit()
        self.HTO = QLabel('Химико-термическая обработка')
        self.e9 = QLineEdit()
        self.Pok = QLabel('Покрытие')
        self.e10 = QLineEdit()
        self.TVR = QLabel('Требование на взаимное положение')
        self.e11 = QLineEdit()
        self.VV = QLabel('Вид и величина требований взаимного положения')
        self.e12 = QLineEdit()
        self.R = QLabel('Радиус при переходе от элемента вращения\n к ограничивающей его плоскости')
        self.e13 = QLineEdit()
        self.Bur = QLabel('Шероховатость плоскости,\nограничивающий элемент вращения')
        self.e14 = QLineEdit()
        self.TVRPL = QLabel('Требование на взаимное расположение\n плоскости, ограничивающей элемент первого уровня')
        self.e15 = QLineEdit()
        self.VVPL = QLabel('Вид и величина этих требований')
        self.e16 = QLineEdit()
        self.Kol2 = QLabel('Количество элементов 2-ого уровня на элементе')
        self.e17 = QLineEdit()
        self.Sum2 = QLabel('Сумма элементов 2-ого уровня на детали в нарастающем порядке')
        self.e18 = QLineEdit()
        self.DZ = QLabel('Диаметр элемента в заготовке')
        self.e19 = QLineEdit()
        self.ESZ = QLabel('Верхнее отклонение в заготовке')
        self.e20 = QLineEdit()
        self.EIZ = QLabel('Нижнее отклонение в заготовке')
        self.e21 = QLineEdit()
        self.Obr = QLabel('Окончательная обработка')
        self.e22 = QLineEdit()
        self.rezerv = QLabel('Резерв')
        self.e23 = QLineEdit()
        self.Marsh = QLabel('Маршрут обработки плоскостей')
        self.e24 = QLineEdit()
        self.Kanav = QLabel('Наличие канавки у буртика')
        self.e25 = QLineEdit()
        self.MEV = QLabel('Маршрут элементов вращение')
        self.e26 = QLineEdit()
        self.Sum3 = QLabel('Суммарное количество элементов 3-его уровня на элементе')
        self.e27 = QLineEdit()
        self.LG = QLabel('Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня слева')
        self.e28 = QLineEdit()
        self.PG = QLabel('Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня справа')
        self.e29 = QLineEdit()
        self.Priz = QLabel('Признак обработки элементов вращения')
        self.e30 = QLineEdit()
        self.TS = QLabel('Тип станка для окончательной обработки\nэлемента 1-ого уровня и указание о\nнеобходимости проведения этой\nобработки до и после термообработки')
        layout.addWidget(self.l, 10, 0, 10, 1)
        layout.addWidget(self.D, 0,1, Qt.AlignRight)
        layout.addWidget(self.P, 1, 1, Qt.AlignRight)
        layout.addWidget(self.K, 2, 1, Qt.AlignRight)
        layout.addWidget(self.ES, 3, 1, Qt.AlignRight)
        layout.addWidget(self.EI, 4, 1, Qt.AlignRight)
        layout.addWidget(self.SH, 5, 1, Qt.AlignRight)
        layout.addWidget(self.OT, 6, 1, Qt.AlignRight)
        layout.addWidget(self.HTO, 7, 1, Qt.AlignRight)
        layout.addWidget(self.Pok, 8, 1, Qt.AlignRight)
        layout.addWidget(self.TVR, 9, 1, Qt.AlignRight)
        layout.addWidget(self.VV, 10, 1, Qt.AlignRight)
        layout.addWidget(self.R, 11, 1, Qt.AlignRight)
        layout.addWidget(self.Bur, 12, 1, Qt.AlignRight)
        layout.addWidget(self.TVRPL, 13, 1, Qt.AlignRight)
        layout.addWidget(self.VVPL, 14, 1, Qt.AlignRight)
        layout.addWidget(self.Kol2, 15, 1, Qt.AlignRight)
        layout.addWidget(self.Sum2, 16, 1, Qt.AlignRight)
        layout.addWidget(self.DZ, 17, 1, Qt.AlignRight)
        layout.addWidget(self.ESZ, 18, 1, Qt.AlignRight)
        layout.addWidget(self.EIZ, 19, 1, Qt.AlignRight)
        layout.addWidget(self.Obr, 20, 1, Qt.AlignRight)
        layout.addWidget(self.rezerv, 21, 1, Qt.AlignRight)
        layout.addWidget(self.Marsh, 22, 1, Qt.AlignRight)
        layout.addWidget(self.Kanav, 23, 1, Qt.AlignRight)
        layout.addWidget(self.MEV, 24, 1, Qt.AlignRight)
        layout.addWidget(self.Sum3, 25, 1, Qt.AlignRight)
        layout.addWidget(self.LG, 26, 1, Qt.AlignRight)
        layout.addWidget(self.PG, 27, 1, Qt.AlignRight)
        layout.addWidget(self.Priz, 28, 1, Qt.AlignRight)
        layout.addWidget(self.TS, 29, 1, Qt.AlignRight)

        self.B1 = QPushButton('1 поверхность', self)
        self.B1.clicked.connect(self.Pic)

        self.B2 = QPushButton('2 поверхность')
        self.B2.clicked.connect(self.Pic)

        self.B3 = QPushButton('3 поверхность')
        self.B3.clicked.connect(self.Pic)

        self.B4 = QPushButton('4 поверхность')
        self.B4.clicked.connect(self.Pic)

        self.B5 = QPushButton('5 поверхность')
        self.B5.clicked.connect(self.Pic)

        self.B6 = QPushButton('6 поверхность')
        self.B6.clicked.connect(self.Pic)

        self.B7 = QPushButton('7 поверхность')
        self.B7.clicked.connect(self.Pic)

        self.B8 = QPushButton('8 поверхность')
        self.B8.clicked.connect(self.Pic)

        self.B9 = QPushButton('9 поверхность')
        self.B9.clicked.connect(self.Pic)

        self.B10 = QPushButton('10 поверхность')
        self.B10.clicked.connect(self.Pic)

        self.B11 = QPushButton('11 поверхность')
        self.B11.clicked.connect(self.Pic)

        self.B12 = QPushButton('12 поверхность')
        self.B12.clicked.connect(self.Pic)

        self.B13 = QPushButton('13 поверхность')
        self.B13.clicked.connect(self.Pic)

        self.B14 = QPushButton('14 поверхность')
        self.B14.clicked.connect(self.Pic)

        self.B15 = QPushButton('15 поверхность')
        self.B15.clicked.connect(self.Pic)

        for eq in range(30):
            layout.addWidget(QLabel('='),eq,3, Qt.AlignHCenter)

        layout.addWidget(self.e1, 0, 4)
        layout.addWidget(self.e2, 1, 4)
        layout.addWidget(self.e3, 2, 4)
        layout.addWidget(self.e4, 3, 4)
        layout.addWidget(self.e5, 4, 4)
        layout.addWidget(self.e6, 5, 4)
        layout.addWidget(self.e7, 6, 4)
        layout.addWidget(self.e8, 7, 4)
        layout.addWidget(self.e9, 8, 4)
        layout.addWidget(self.e10, 9, 4)
        layout.addWidget(self.e11, 10, 4)
        layout.addWidget(self.e12, 11, 4)
        layout.addWidget(self.e13, 12, 4)
        layout.addWidget(self.e14, 13, 4)
        layout.addWidget(self.e15, 14, 4)
        layout.addWidget(self.e16, 15, 4)
        layout.addWidget(self.e17, 16, 4)
        layout.addWidget(self.e18, 17, 4)
        layout.addWidget(self.e19, 18, 4)
        layout.addWidget(self.e20, 19, 4)
        layout.addWidget(self.e21, 20, 4)
        layout.addWidget(self.e22, 21, 4)
        layout.addWidget(self.e23, 22, 4)
        layout.addWidget(self.e24, 23, 4)
        layout.addWidget(self.e25, 24, 4)
        layout.addWidget(self.e26, 25, 4)
        layout.addWidget(self.e27, 26, 4)
        layout.addWidget(self.e28, 27, 4)
        layout.addWidget(self.e29, 28, 4)
        layout.addWidget(self.e30, 29, 4)

        layout.addWidget(self.B1, 0, 5, 2, 1)
        layout.addWidget(self.B2, 2, 5, 2, 1)
        layout.addWidget(self.B3, 4, 5, 2, 1)
        layout.addWidget(self.B4, 6, 5, 2, 1)
        layout.addWidget(self.B5, 8, 5, 2, 1)
        layout.addWidget(self.B6, 10, 5, 2, 1)
        layout.addWidget(self.B7, 12, 5, 2, 1)
        layout.addWidget(self.B8, 14, 5, 2, 1)
        layout.addWidget(self.B9, 16, 5, 2, 1)
        layout.addWidget(self.B10, 18, 5, 2, 1)
        layout.addWidget(self.B11, 20, 5, 2, 1)
        layout.addWidget(self.B12, 22, 5, 2, 1)
        layout.addWidget(self.B13, 24, 5, 2, 1)
        layout.addWidget(self.B14, 26, 5, 2, 1)
        layout.addWidget(self.B15, 28, 5, 2, 1)

        self.setTabText(1,"TM2")
        self.tab2.setLayout(layout)


    def tab3f(self):

        layout = QFormLayout()
        layout.addRow("Пиши тут", QLineEdit())
        layout.addRow("и тут", QLineEdit())
        self.setTabText(2, "TM3")
        self.tab3.setLayout(layout)

    def enabl(self):

        self.B15.setEnabled(True)
        self.B14.setEnabled(True)
        self.B13.setEnabled(True)
        self.B12.setEnabled(True)
        self.B11.setEnabled(True)
        self.B10.setEnabled(True)
        self.B9.setEnabled(True)
        self.B8.setEnabled(True)
        self.B7.setEnabled(True)
        self.B6.setEnabled(True)
        self.B5.setEnabled(True)
        self.B4.setEnabled(True)

        hmp = 3
        for t in range(3,len(TabUI.image)):
            if TabUI.image[t] == 0:
                break
            else:
                hmp+=1
        print(hmp)
        if hmp < 15:
            self.B15.setEnabled(False)
            if hmp < 14:
                self.B14.setEnabled(False)
                if hmp < 13:
                    self.B13.setEnabled(False)
                    if hmp < 12:
                        self.B12.setEnabled(False)
                        if hmp < 11:
                            self.B11.setEnabled(False)
                            if hmp < 10:
                                self.B10.setEnabled(False)
                                if hmp < 9:
                                    self.B9.setEnabled(False)
                                    if hmp < 8:
                                        self.B8.setEnabled(False)
                                        if hmp < 7:
                                            self.B7.setEnabled(False)
                                            if hmp < 6:
                                                self.B6.setEnabled(False)
                                                if hmp < 5:
                                                    self.B5.setEnabled(False)
                                                    if hmp < 4:
                                                        self.B4.setEnabled(False)

    def Message(self):
        buttonReply = QMessageBox.warning(self, 'Failed', "You must enter data in the table",
                                          QMessageBox.Close, QMessageBox.Close)

    # выводим данные из таблицы
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
            TabUI.image = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in range(1, sum):
                print(ChoosePic.ChoosePic(data, i))
                TabUI.image[i-1] = ChoosePic.ChoosePic(data, i)
            print(data)
            print(TabUI.image)
            self.enabl()

        except:
            self.Message()

    def Pic(self):

        sender = self.sender()
        t = sender.text()
        if t == '1 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[0])))
        elif t == '2 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[1])))
        elif t == '3 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[2])))
        elif t == '4 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[3])))
        elif t == '5 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[4])))
        elif t == '6 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[5])))
        elif t == '7 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[6])))
        elif t == '8 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[7])))
        elif t == '9 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[8])))
        elif t == '10 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[9])))
        elif t == '11 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[10])))
        elif t == '12 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[11])))
        elif t == '13 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[12])))
        elif t == '14 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[13])))
        elif t == '15 поверхность':
            self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[14])))

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())