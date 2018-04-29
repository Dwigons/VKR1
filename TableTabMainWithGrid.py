from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout, QScroller, QScrollArea
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap
import json
import Initialisation, ChoosePic




# Наследуемся от QMainWindow
class Tab_Widget(QMainWindow):
    XLS_FILE_PATH = 'default.xls'
    # Переопределяем конструктор класса
    def __init__(self, parent = None):
        # Обязательно нужно вызвать метод супер класса
        super().__init__(parent)
        self.tabUI = TabUI(self)
        # self.secondWin = SecondWindow()

        # self.setMinimumSize(QSize(1100, 600))  # Устанавливаем размеры
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



        scroll_area = QScrollArea()
        layout = QGridLayout(self)
        layout.addWidget(scroll_area)
        scroll_widget = QWidget()
        scroll_area.setWidget(self.setCentralWidget(self.tabUI))
        self.setCentralWidget(self.tabUI)  # Устанавливаем центральный виджет

        QScroller.grabGesture(
            scroll_area.viewport(), QScroller.LeftMouseButtonGesture
        )

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
        shapka = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array = QScrollArea()
        scroll_area_array.setMaximumWidth(800)
        scroll_area_tab_improvisation = QScrollArea()
        scroll_area_tab_improvisation.setMaximumHeight(62)


        set_widget1= QWidget()
        set_widget2 = QWidget()
        scroll_layout1 = QGridLayout(set_widget1)
        H_layout = QHBoxLayout(set_widget1)

        # scroll_layout1 = QFormLayout(set_widget1)
        # scroll_layout1.labelAlignment = 0x0040
        scroll_layout2 = QFormLayout(set_widget2)

        window_tab2 = QWidget()
        window_tab22 = QWidget()
        ALlInV = QVBoxLayout(window_tab2)
        layout = QHBoxLayout(window_tab2)
        layout2 = QHBoxLayout(set_widget2)
        layout3 = QHBoxLayout()
        Vlayout = QVBoxLayout(window_tab2)
        V2layout = QVBoxLayout(window_tab2)

        V2layout.addWidget(shapka)


        self.l = QLabel()

        self.e1 = QLineEdit()
        self.le1 = QLabel('Номинальный диаметр: ')

        self.e2 = QLineEdit()
        self.le2 = QLabel('Посадка: ')

        self.e3 = QLineEdit()
        self.le3 = QLabel('Номер квалитета: ')

        self.e4 = QLineEdit()
        self.le4 = QLabel('Верхнее отклонение: ')

        self.e5 = QLineEdit()
        self.le5 = QLabel('Нижнее отклонение: ')

        self.e6 = QLineEdit()
        self.le6 = QLabel('Величина параметра шероховатость: ')

        self.e7 = QLineEdit()
        self.le7 = QLabel('Особые требования: ')

        self.e8 = QLineEdit()
        self.le8 = QLabel('Химико-термическая обработка: ')

        self.e9 = QLineEdit()
        self.le9 = QLabel('Покрытие: ')

        self.e10 = QLineEdit()
        self.le10 = QLabel('Требование на взаимное положение: ')

        self.e11 = QLineEdit()
        self.le11 = QLabel('Вид и величина требований взаимного положения: ')

        self.e12 = QLineEdit()
        self.le12 = QLabel('Радиус при переходе от элемента вращения\n к ограничивающей его плоскости: ')

        self.e13 = QLineEdit()
        self.le13 = QLabel('Шероховатость плоскости,\nограничивающий элемент вращения: ')

        self.e14 = QLineEdit()
        self.le14 = QLabel('Требование на взаимное расположение плоскости,\nограничивающей элемент первого уровня: ')

        self.e15 = QLineEdit()
        self.le15 = QLabel('Вид и величина этих требований: ')

        self.e16 = QLineEdit()
        self.le16 = QLabel('Количество элементов 2-ого уровня на элементе: ')

        self.e17 = QLineEdit()
        self.le17 = QLabel('Сумма элементов 2-ого уровня на детали в нарастающем порядке: ')

        self.e18 = QLineEdit()
        self.le18 = QLabel('Диаметр элемента в заготовке: ')

        self.e19 = QLineEdit()
        self.le19 = QLabel('Верхнее отклонение в заготовке: ')

        self.e20 = QLineEdit()
        self.le20 = QLabel('Нижнее отклонение в заготовке: ')

        self.e21 = QLineEdit()
        self.le21 = QLabel('Окончательная обработка: ')

        self.e22 = QLineEdit()
        self.le22 = QLabel('Резерв: ')

        self.e23 = QLineEdit()
        self.le23 = QLabel('Маршрут обработки плоскостей: ')

        self.e24 = QLineEdit()
        self.le24 = QLabel('Наличие канавки у буртика: ')

        self.e25 = QLineEdit()
        self.le25 = QLabel('Маршрут элементов вращение: ')

        self.e26 = QLineEdit()
        self.le26 = QLabel('Суммарное количество элементов 3-его уровня на элементе: ')

        self.e27 = QLineEdit()
        self.le27 = QLabel('Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня слева: ')

        self.e28 = QLineEdit()
        self.le28 = QLabel('Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня справа: ')

        self.e29 = QLineEdit()
        self.le29 = QLabel('Признак обработки элементов вращения: ')

        self.e30 = QLineEdit()
        self.le30 = QLabel('Тип станка для окончательной обработки элемента 1-ого уровня и\nуказание о необходимости проведения этой обработки до и после термообработки: ')

       
        scroll_layout1.addWidget(self.le1, 0, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le2, 1, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le3, 2, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le4, 3, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le5, 4, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le6, 5, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le7, 6, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le8, 7, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le9, 8, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le10, 9, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le11, 10, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le12, 11, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le13, 12, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le14, 13, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le15, 14, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le16, 15, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le17, 16, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le18, 17, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le19, 18, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le20, 19, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le21, 20, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le22, 21, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le23, 22, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le24, 23, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le25, 24, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le26, 25, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le27, 26, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le28, 27, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le29, 28, 0, Qt.AlignRight)
        scroll_layout1.addWidget(self.le30, 29, 0, Qt.AlignRight)

        scroll_layout1.addWidget(self.e1, 0, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e2, 1, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e3, 2, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e4, 3, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e5, 4, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e6, 5, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e7, 6, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e8, 7, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e9, 8, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e10, 9, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e11, 10, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e12, 11, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e13, 12, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e14, 13, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e15, 14, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e16, 15, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e17, 16, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e18, 17, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e19, 18, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e20, 19, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e21, 20, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e22, 21, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e23, 22, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e24, 23, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e25, 24, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e26, 25, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e27, 26, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e28, 27, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e29, 28, 1, Qt.AlignCenter)
        scroll_layout1.addWidget(self.e30, 29, 1, Qt.AlignCenter)


        layout.addLayout(V2layout)
        # layout.addLayout(layout2)
        #Добавляю скрол эреа на слой
        scroll_area_array.setWidget(set_widget1)
        H_layout.addWidget(scroll_area_array)
        H_layout.addWidget(self.l)

        self.B1 = QPushButton('1 поверхность', self)
        self.B1.clicked.connect(self.Pic)
        # self.B1.setCheckable(True)

        self.B2 = QPushButton('2 поверхность')
        self.B2.clicked.connect(self.Pic)
        # self.B2.setCheckable(True)

        self.B3 = QPushButton('3 поверхность')
        self.B3.clicked.connect(self.Pic)
        # self.B3.setCheckable(True)

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



        layout2.addWidget(self.B1)
        layout2.addWidget(self.B2)
        layout2.addWidget(self.B3)
        layout2.addWidget(self.B4)
        layout2.addWidget(self.B5)
        layout2.addWidget(self.B6)
        layout2.addWidget(self.B7)
        layout2.addWidget(self.B8)
        layout2.addWidget(self.B9)
        layout2.addWidget(self.B10)
        layout2.addWidget(self.B11)
        layout2.addWidget(self.B12)
        layout2.addWidget(self.B13)
        layout2.addWidget(self.B14)
        layout2.addWidget(self.B15)
        scroll_layout2.insertRow(1,layout2)
        scroll_area_tab_improvisation.setWidget(set_widget2)
        V2layout.addWidget(scroll_area_tab_improvisation)

        # layout.addWidget(self.l)

        # V2layout.addWidget(scroll_area_array)
        V2layout.addLayout(H_layout)



        #
        # Vlayout.addStretch(1)
        # layout.addStretch(1)
        # layout.addLayout(Vlayout)

        # sobaka.addLayout(window_tab2)

        self.setTabText(1,"TM2")
        self.tab2.setLayout(layout)
        # self.tab2.setLayout(sobaka)


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