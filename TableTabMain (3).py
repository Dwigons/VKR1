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
                            Array = Initialisation.ExcelSaveLoad.read_xls_from_file(Tab_Widget.XLS_FILE_PATH)
                            TabUI.Tm2 = Array['TM2']

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
                TabUI.Tm2 = Array['TM2']


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
        self.tab4 = QWidget()
        self.tabD = QWidget()
        self.tabI = QWidget()
        self.tabA = QWidget()


        self.addTab(self.tab1, "TM1")
        self.addTab(self.tab2, "TM2")
        self.addTab(self.tab3, "TM3")
        self.addTab(self.tab4, "TM4")
        self.addTab(self.tabD, "TMD")
        self.addTab(self.tabI, "TMI")
        self.addTab(self.tabA, "TMA")

        self.tab1f()
        self.tab2f()
        self.tab3f()
        self.tab4f()
        self.tabDf()
        self.tabIf()
        self.tabAf()


    def tab1f(self):

        grid_layout = QGridLayout()  # Создаём QGridLayout
        # central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        TabUI.table = QTableWidget(self)  # Создаём таблицу
        # self.table.setMaximumWidth(1500)
        self.table.setMinimumWidth(950)
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

        grid_layout.addWidget(self.table, 0, 0,3,1,Qt.AlignLeft)  # Добавляем таблицу в сетку


        self.saveb = QPushButton('Next', self)
        self.saveb.setMaximumWidth(100)
        self.proba = QPushButton('Проба', self)
        self.proba.setMaximumWidth(100)
        self.proba.setCheckable(False)
        self.saveb.setCheckable(False)
        self.saveb.move(980, 950)
        self.proba.move(980, 900)

        # self.saveb.setGeometry(1000, 1000, 20, 25)
        grid_layout.addWidget(self.saveb,1,1, Qt.AlignLeft)
        grid_layout.addWidget(self.proba,2,1, Qt.AlignLeft)

        self.saveb.clicked.connect(self.getData)

        self.setTabText(0, "TM1")
        self.tab1.setLayout(grid_layout)


    def tab2f(self):
        shapka = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array = QScrollArea()
        scroll_area_tab_improvisation = QScrollArea()

        set_widget1= QWidget()
        set_widget2 = QWidget()

        scroll_area_tab_improvisation.setMaximumHeight(90)
        scroll_area_array.setMaximumWidth(800)
        # scroll_layout1 = QGridLayout(set_widget1)
        scroll_layout1 = QFormLayout(set_widget1)
        H_layout = QHBoxLayout(set_widget1)
        # scroll_layout1.labelAlignment = 0x0040
        scroll_layout2 = QFormLayout(set_widget2)

        window_tab2 = QWidget()
        window_tab22 = QWidget()
        ALlInV = QVBoxLayout(window_tab2)
        layout = QHBoxLayout(window_tab2)
        layout2 = QHBoxLayout(set_widget2)
        layout4 = QHBoxLayout(set_widget2)
        layout3 = QHBoxLayout()
        Vlayout = QVBoxLayout(window_tab2)
        V2layout = QVBoxLayout(window_tab2)

        V2layout.addWidget(shapka)

        self.l = QLabel()

        self.e1 = QLineEdit()
        scroll_layout1.addRow(QLabel('1 Номинальный диаметр '), self.e1)

        self.e2 = QLineEdit()
        scroll_layout1.addRow(QLabel('2 Посадка '), self.e2)

        self.e3 = QLineEdit()
        scroll_layout1.addRow(QLabel('3 Номер квалитета '), self.e3)

        self.e4 = QLineEdit()
        scroll_layout1.addRow(QLabel('4 Верхнее отклонение '), self.e4)

        self.e5 = QLineEdit()
        scroll_layout1.addRow(QLabel('5 Нижнее отклонение '), self.e5)

        self.e6 = QLineEdit()
        scroll_layout1.addRow(QLabel('6 Величина параметра шероховатость '), self.e6)

        self.e7 = QLineEdit()
        scroll_layout1.addRow(QLabel('7 Особые требования '), self.e7)

        self.e8 = QLineEdit()
        scroll_layout1.addRow(QLabel('8 Химико-термическая обработка '), self.e8)

        self.e9 = QLineEdit()
        scroll_layout1.addRow(QLabel('9 Покрытие '), self.e9)

        self.e10 = QLineEdit()
        scroll_layout1.addRow(QLabel('10 Требование на взаимное положение '), self.e10)

        self.e11 = QLineEdit()
        scroll_layout1.addRow(QLabel('11 Вид и величина требований взаимного положения '), self.e11)

        self.e12 = QLineEdit()
        scroll_layout1.addRow(QLabel('12 Радиус при переходе от элемента вращения\n к ограничивающей его плоскости '), self.e12)

        self.e13 = QLineEdit()
        scroll_layout1.addRow(QLabel('13 Шероховатость плоскости,\nограничивающий элемент вращения '), self.e13)

        self.e14 = QLineEdit()
        scroll_layout1.addRow(QLabel('14 Требование на взаимное расположение плоскости,\nограничивающей элемент первого уровня '), self.e14)

        self.e15 = QLineEdit()
        scroll_layout1.addRow(QLabel('15 Вид и величина этих требований '), self.e15)

        self.e16 = QLineEdit()
        scroll_layout1.addRow(QLabel('16 Количество элементов 2-ого уровня на элементе '), self.e16)

        self.e17 = QLineEdit()
        scroll_layout1.addRow(QLabel('17 Сумма элементов 2-ого уровня на детали в нарастающем порядке '), self.e17)

        self.e18 = QLineEdit()
        scroll_layout1.addRow(QLabel('18 Диаметр элемента в заготовке '), self.e18)

        self.e19 = QLineEdit()
        scroll_layout1.addRow(QLabel('19 Верхнее отклонение в заготовке '), self.e19)

        self.e20 = QLineEdit()
        scroll_layout1.addRow(QLabel('20 Нижнее отклонение в заготовке '), self.e20)

        self.e21 = QLineEdit()
        scroll_layout1.addRow(QLabel('21 Окончательная обработка '), self.e21)

        self.e22 = QLineEdit()
        scroll_layout1.addRow(QLabel('22 Резерв '), self.e22)

        self.e23 = QLineEdit()
        scroll_layout1.addRow(QLabel('23 Маршрут обработки плоскостей '), self.e23)

        self.e24 = QLineEdit()
        scroll_layout1.addRow(QLabel('24 Наличие канавки у буртика '), self.e24)

        self.e25 = QLineEdit()
        scroll_layout1.addRow(QLabel('25 Маршрут элементов вращение '), self.e25)

        self.e26 = QLineEdit()
        scroll_layout1.addRow(QLabel('26 Суммарное количество элементов 3-его уровня на элементе '), self.e26)

        self.e27 = QLineEdit()
        scroll_layout1.addRow(QLabel('27 Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня слева '), self.e27)

        self.e28 = QLineEdit()
        scroll_layout1.addRow(QLabel('28 Номер плоскостного элемента, ограничивающего\nрассматриваемый элемент 1-ого уровня справа '), self.e28)

        self.e29 = QLineEdit()
        scroll_layout1.addRow(QLabel('29 Признак обработки элементов вращения '), self.e29)

        self.e30 = QLineEdit()
        scroll_layout1.addRow(QLabel('30 Тип станка для окончательной обработки элемента 1-ого уровня\n и указание о необходимости проведения этой\nобработки до и после термообработки '), self.e30)

        self.nextTm3 = QPushButton('Next',self)
        self.nextTm3.setMaximumWidth(100)
        self.nextTm3.move(980, 900)
        self.nextTm3.clicked.connect(self.next_tab)

        layout.addLayout(V2layout)
        # layout.addLayout(layout2)
        #Добавляю скрол эреа на слой
        scroll_area_array.setWidget(set_widget1)
        H_layout.addWidget(scroll_area_array)
        H_layout.addWidget(self.l)
        H_layout.addWidget(self.nextTm3,Qt.AlignTop|Qt.AlignRight)

        self.B1 = QPushButton('1 поверхность', self)
        self.B1.setCheckable(True)
        self.B1.clicked.connect(self.Pic)

        self.B2 = QPushButton('2 поверхность')
        self.B2.setCheckable(True)
        self.B2.clicked.connect(self.Pic)

        self.B3 = QPushButton('3 поверхность')
        self.B3.setCheckable(True)
        self.B3.clicked.connect(self.Pic)

        self.B4 = QPushButton('4 поверхность')
        self.B4.setCheckable(True)
        self.B4.clicked.connect(self.Pic)

        self.B5 = QPushButton('5 поверхность')
        self.B5.setCheckable(True)
        self.B5.clicked.connect(self.Pic)

        self.B6 = QPushButton('6 поверхность')
        self.B6.setCheckable(True)
        self.B6.clicked.connect(self.Pic)

        self.B7 = QPushButton('7 поверхность')
        self.B7.setCheckable(True)
        self.B7.clicked.connect(self.Pic)

        self.B8 = QPushButton('8 поверхность')
        self.B8.setCheckable(True)
        self.B8.clicked.connect(self.Pic)

        self.B9 = QPushButton('9 поверхность')
        self.B9.setCheckable(True)
        self.B9.clicked.connect(self.Pic)

        self.B10 = QPushButton('10 поверхность')
        self.B10.setCheckable(True)
        self.B10.clicked.connect(self.Pic)

        self.B11 = QPushButton('11 поверхность')
        self.B11.setCheckable(True)
        self.B11.clicked.connect(self.Pic)

        self.B12 = QPushButton('12 поверхность')
        self.B12.setCheckable(True)
        self.B12.clicked.connect(self.Pic)

        self.B13 = QPushButton('13 поверхность')
        self.B13.setCheckable(True)
        self.B13.clicked.connect(self.Pic)

        self.B14 = QPushButton('14 поверхность')
        self.B14.setCheckable(True)
        self.B14.clicked.connect(self.Pic)

        self.B15 = QPushButton('15 поверхность')
        self.B15.setCheckable(True)
        self.B15.clicked.connect(self.Pic)

        self.save_param = QPushButton('Сохранить\nпараметры')
        self.save_param.setMaximumWidth(100)
        self.inf = QLabel('Information:\nButtons will be accessible after saving parameters')
        self.save_param.clicked.connect(self.dataTm2)



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

        layout4.addWidget(self.save_param)
        layout4.addWidget(self.inf)

        scroll_layout2.insertRow(1,layout2)
        scroll_layout2.insertRow(2, layout4)
        scroll_area_tab_improvisation.setWidget(set_widget2)
        V2layout.addWidget(scroll_area_tab_improvisation)

        V2layout.addLayout(H_layout)

        self.setTabText(1,"TM2")
        self.tab2.setLayout(layout)

    def next_tab(self):
        self.setCurrentIndex(self.currentIndex()+1)
        Initialisation.ExcelSaveLoad.my_func('TM2', TabUI.Tm2, Tab_Widget.XLS_FILE_PATH)

    def tab3f(self):
        self.file = json.load(open('Dataset/TM3.json'))
        # for i in range(len(self.file)):
        #     self.table.setItem(i, 0, QTableWidgetItem(str(self.file[i][0])))
        shapka_TM3 = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array_TM3 = QScrollArea()
        scroll_area_tab_improvisation_TM3 = QScrollArea()

        set_widget1_TM3 = QWidget()
        set_widget2_TM3 = QWidget()

        scroll_area_tab_improvisation_TM3.setMaximumHeight(100)
        scroll_area_array_TM3.setMaximumWidth(660)
        scroll_layout1_TM3 = QFormLayout(set_widget1_TM3)
        H_layout_TM3 = QHBoxLayout(set_widget1_TM3)
        scroll_layout2_TM3 = QFormLayout(set_widget2_TM3)

        window_tab2_TM3 = QWidget()
        layout_TM3 = QHBoxLayout(window_tab2_TM3)
        layout2_TM3 = QHBoxLayout(set_widget2_TM3)
        layout4_TM3 = QHBoxLayout(set_widget2_TM3)
        V2layout_TM3 = QVBoxLayout(window_tab2_TM3)
        V2layout_TM3.addWidget(shapka_TM3)

        # Создание кнопок выбора элемента
        self.l_TM3 = QLabel()

        self.B1_TM3 = QPushButton('1-й элемент', self)
        self.B1_TM3.clicked.connect(self.Pic)

        self.B2_TM3 = QPushButton('2-й элемент')
        self.B2_TM3.clicked.connect(self.Pic)

        self.B3_TM3 = QPushButton('3-й элемент')
        self.B3_TM3.clicked.connect(self.Pic)

        self.B4_TM3 = QPushButton('4-й элемент')
        self.B4_TM3.clicked.connect(self.Pic)

        self.B5_TM3 = QPushButton('5-й элемент')
        self.B5_TM3.clicked.connect(self.Pic)

        self.B6_TM3 = QPushButton('6-й элемент')
        self.B6_TM3.clicked.connect(self.Pic)

        self.B7_TM3 = QPushButton('7-й элемент')
        self.B7_TM3.clicked.connect(self.Pic)

        self.B8_TM3 = QPushButton('8-й элемент')
        self.B8_TM3.clicked.connect(self.Pic)

        self.B9_TM3 = QPushButton('9-й элемент')
        self.B9_TM3.clicked.connect(self.Pic)

        self.B10_TM3 = QPushButton('10-й элемент')
        self.B10_TM3.clicked.connect(self.Pic)

        self.B11_TM3 = QPushButton('11-й элемент')
        self.B11_TM3.clicked.connect(self.Pic)

        self.B12_TM3 = QPushButton('12-й элемент')
        self.B12_TM3.clicked.connect(self.Pic)

        self.B13_TM3 = QPushButton('13-й элемент')
        self.B13_TM3.clicked.connect(self.Pic)

        self.B14_TM3 = QPushButton('14-й элемент')
        self.B14_TM3.clicked.connect(self.Pic)

        self.B15_TM3 = QPushButton('15-й элемент')
        self.B15_TM3.clicked.connect(self.Pic)

        self.save_param_TM3 = QPushButton('Сохранить\nпараметры')
        self.save_param_TM3.setMaximumWidth(100)
        self.inf_TM3 = QLabel('Information:\nButtons will be accessible after saving parameters')
        self.save_param_TM3.clicked.connect(self.dataTm2)

        layout2_TM3.addWidget(self.B1_TM3)
        layout2_TM3.addWidget(self.B2_TM3)
        layout2_TM3.addWidget(self.B3_TM3)
        layout2_TM3.addWidget(self.B4_TM3)
        layout2_TM3.addWidget(self.B5_TM3)
        layout2_TM3.addWidget(self.B6_TM3)
        layout2_TM3.addWidget(self.B7_TM3)
        layout2_TM3.addWidget(self.B8_TM3)
        layout2_TM3.addWidget(self.B9_TM3)
        layout2_TM3.addWidget(self.B10_TM3)
        layout2_TM3.addWidget(self.B11_TM3)
        layout2_TM3.addWidget(self.B12_TM3)
        layout2_TM3.addWidget(self.B13_TM3)
        layout2_TM3.addWidget(self.B14_TM3)
        layout2_TM3.addWidget(self.B15_TM3)

        layout4_TM3.addWidget(self.save_param_TM3)
        layout4_TM3.addWidget(self.inf_TM3)

        scroll_layout2_TM3.insertRow(1, layout2_TM3)
        scroll_layout2_TM3.insertRow(2, layout4_TM3)
        scroll_area_tab_improvisation_TM3.setWidget(set_widget2_TM3)
        V2layout_TM3.addWidget(scroll_area_tab_improvisation_TM3)
        # Кнопки выбора элемента добавлены на слой

        self.e1_TM3 = QLineEdit()
        self.e2_TM3 = QLineEdit()
        self.e3_TM3 = QLineEdit()
        self.e4_TM3 = QLineEdit()
        self.e5_TM3 = QLineEdit()
        self.e6_TM3 = QLineEdit()
        self.e7_TM3 = QLineEdit()
        self.e8_TM3 = QLineEdit()
        self.e9_TM3 = QLineEdit()
        self.e10_TM3 = QLineEdit()
        self.e11_TM3 = QLineEdit()
        self.e12_TM3 = QLineEdit()
        self.e13_TM3 = QLineEdit()
        self.e14_TM3 = QLineEdit()
        self.e15_TM3 = QLineEdit()
        self.e16_TM3 = QLineEdit()
        self.e17_TM3 = QLineEdit()
        self.e18_TM3 = QLineEdit()
        self.e19_TM3 = QLineEdit()
        self.e20_TM3 = QLineEdit()
        self.e21_TM3 = QLineEdit()
        self.e22_TM3 = QLineEdit()
        self.e23_TM3 = QLineEdit()
        self.e24_TM3 = QLineEdit()
        self.e25_TM3 = QLineEdit()
        self.e26_TM3 = QLineEdit()
        self.e27_TM3 = QLineEdit()
        self.e28_TM3 = QLineEdit()
        self.e29_TM3 = QLineEdit()
        self.e30_TM3 = QLineEdit()

        scroll_layout1_TM3.addRow(QLabel(self.file[0][0]), self.e1_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[1][0]), self.e2_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[2][0]), self.e3_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[3][0]), self.e4_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[4][0]), self.e5_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[5][0]), self.e6_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[6][0]), self.e7_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[7][0]), self.e8_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[8][0]), self.e9_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[9][0]), self.e10_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[10][0]), self.e11_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[11][0]), self.e12_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[12][0]), self.e13_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[13][0]), self.e14_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[14][0]), self.e15_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[15][0]), self.e16_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[16][0]), self.e17_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[17][0]), self.e18_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[18][0]), self.e19_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[19][0]), self.e20_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[20][0]), self.e21_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[21][0]), self.e22_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[22][0]), self.e23_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[23][0]), self.e24_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[24][0]), self.e25_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[25][0]), self.e26_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[26][0]), self.e27_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[27][0]), self.e28_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[28][0]), self.e29_TM3)
        scroll_layout1_TM3.addRow(QLabel(self.file[29][0]), self.e30_TM3)

        layout_TM3.addLayout(V2layout_TM3)
        scroll_area_array_TM3.setWidget(set_widget1_TM3)
        H_layout_TM3.addWidget(scroll_area_array_TM3)

        self.nextTm3 = QPushButton('Next', self)
        self.nextTm3.setMaximumWidth(100)
        self.nextTm3.move(980, 900)
        self.nextTm3.clicked.connect(self.TM3_func)
        H_layout_TM3.addWidget(self.nextTm3, Qt.AlignTop | Qt.AlignRight)
        H_layout_TM3.addWidget(self.l_TM3)

        V2layout_TM3.addLayout(H_layout_TM3)

        self.setTabText(2, "TM3")
        self.tab3.setLayout(layout_TM3)
        # self.tab2.setLayout(sobaka)

    def TM3_func(self):
        print('1')
        # self.setCurrentWidget(self.tab4)
        Initialisation.ExcelSaveLoad.my_func('TM3', TabUI.Tm3, Tab_Widget.XLS_FILE_PATH)

    def tab4f(self):
        self.file = json.load(open('Dataset/TM4.json'))
        # for i in range(len(self.file)):
        #     self.table.setItem(i, 0, QTableWidgetItem(str(self.file[i][0])))
        shapka_TM4 = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array_TM4 = QScrollArea()
        scroll_area_tab_improvisation_TM4 = QScrollArea()

        set_widget1_TM4 = QWidget()
        set_widget2_TM4 = QWidget()

        scroll_area_tab_improvisation_TM4.setMaximumHeight(100)
        scroll_area_array_TM4.setMaximumWidth(660)
        scroll_layout1_TM4 = QFormLayout(set_widget1_TM4)
        H_layout_TM4 = QHBoxLayout(set_widget1_TM4)
        scroll_layout2_TM4 = QFormLayout(set_widget2_TM4)

        window_tab2_TM4 = QWidget()
        layout_TM4 = QHBoxLayout(window_tab2_TM4)
        layout2_TM4 = QHBoxLayout(set_widget2_TM4)
        layout4_TM4 = QHBoxLayout(set_widget2_TM4)
        V2layout_TM4 = QVBoxLayout(window_tab2_TM4)
        V2layout_TM4.addWidget(shapka_TM4)

        # Создание кнопок выбора элемента
        self.l_TM4 = QLabel()

        self.B1_TM4 = QPushButton('1-й элемент', self)
        self.B1_TM4.clicked.connect(self.Pic)
        # self.B1_TM4.clicked.connect(self.dataTm2)

        self.B2_TM4 = QPushButton('2-й элемент')
        self.B2_TM4.clicked.connect(self.Pic)

        self.B3_TM4 = QPushButton('3-й элемент')
        self.B3_TM4.clicked.connect(self.Pic)

        self.B4_TM4 = QPushButton('4-й элемент')
        self.B4_TM4.clicked.connect(self.Pic)

        self.B5_TM4 = QPushButton('5-й элемент')
        self.B5_TM4.clicked.connect(self.Pic)

        self.B6_TM4 = QPushButton('6-й элемент')
        self.B6_TM4.clicked.connect(self.Pic)

        self.B7_TM4 = QPushButton('7-й элемент')
        self.B7_TM4.clicked.connect(self.Pic)

        self.B8_TM4 = QPushButton('8-й элемент')
        self.B8_TM4.clicked.connect(self.Pic)

        self.B9_TM4 = QPushButton('9-й элемент')
        self.B9_TM4.clicked.connect(self.Pic)

        self.B10_TM4 = QPushButton('10-й элемент')
        self.B10_TM4.clicked.connect(self.Pic)

        self.B11_TM4 = QPushButton('11-й элемент')
        self.B11_TM4.clicked.connect(self.Pic)

        self.B12_TM4 = QPushButton('12-й элемент')
        self.B12_TM4.clicked.connect(self.Pic)

        self.B13_TM4 = QPushButton('13-й элемент')
        self.B13_TM4.clicked.connect(self.Pic)

        self.B14_TM4 = QPushButton('14-й элемент')
        self.B14_TM4.clicked.connect(self.Pic)

        self.B15_TM4 = QPushButton('15-й элемент')
        self.B15_TM4.clicked.connect(self.Pic)

        self.save_param_TM4 = QPushButton('Сохранить\nпараметры')
        self.save_param_TM4.setMaximumWidth(100)
        self.inf = QLabel('Information:\nButtons will be accessible after saving parameters')
        self.save_param_TM4.clicked.connect(self.dataTm2)

        layout2_TM4.addWidget(self.B1_TM4)
        layout2_TM4.addWidget(self.B2_TM4)
        layout2_TM4.addWidget(self.B3_TM4)
        layout2_TM4.addWidget(self.B4_TM4)
        layout2_TM4.addWidget(self.B5_TM4)
        layout2_TM4.addWidget(self.B6_TM4)
        layout2_TM4.addWidget(self.B7_TM4)
        layout2_TM4.addWidget(self.B8_TM4)
        layout2_TM4.addWidget(self.B9_TM4)
        layout2_TM4.addWidget(self.B10_TM4)
        layout2_TM4.addWidget(self.B11_TM4)
        layout2_TM4.addWidget(self.B12_TM4)
        layout2_TM4.addWidget(self.B13_TM4)
        layout2_TM4.addWidget(self.B14_TM4)
        layout2_TM4.addWidget(self.B15_TM4)

        layout4_TM4.addWidget(self.save_param_TM4)
        layout4_TM4.addWidget(self.inf)

        scroll_layout2_TM4.insertRow(1, layout2_TM4)
        scroll_layout2_TM4.insertRow(2, layout4_TM4)
        scroll_area_tab_improvisation_TM4.setWidget(set_widget2_TM4)
        V2layout_TM4.addWidget(scroll_area_tab_improvisation_TM4)
        # Кнопки выбора элемента добавлены на слой

        self.e1_TM4 = QLineEdit()
        self.e2_TM4 = QLineEdit()
        self.e3_TM4 = QLineEdit()
        self.e4_TM4 = QLineEdit()
        self.e5_TM4 = QLineEdit()
        self.e6_TM4 = QLineEdit()
        self.e7_TM4 = QLineEdit()
        self.e8_TM4 = QLineEdit()
        self.e9_TM4 = QLineEdit()
        self.e10_TM4 = QLineEdit()
        self.e11_TM4 = QLineEdit()
        self.e12_TM4 = QLineEdit()
        self.e13_TM4 = QLineEdit()
        self.e14_TM4 = QLineEdit()
        self.e15_TM4 = QLineEdit()
        self.e16_TM4 = QLineEdit()
        self.e17_TM4 = QLineEdit()
        self.e18_TM4 = QLineEdit()
        self.e19_TM4 = QLineEdit()
        self.e20_TM4 = QLineEdit()
        self.e21_TM4 = QLineEdit()
        self.e22_TM4 = QLineEdit()
        self.e23_TM4 = QLineEdit()
        self.e24_TM4 = QLineEdit()
        self.e25_TM4 = QLineEdit()
        self.e26_TM4 = QLineEdit()
        self.e27_TM4 = QLineEdit()
        self.e28_TM4 = QLineEdit()
        self.e29_TM4 = QLineEdit()
        self.e30_TM4 = QLineEdit()

        scroll_layout1_TM4.addRow(QLabel(self.file[0][0]), self.e1_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[1][0]), self.e2_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[2][0]), self.e3_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[3][0]), self.e4_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[4][0]), self.e5_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[5][0]), self.e6_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[6][0]), self.e7_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[7][0]), self.e8_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[8][0]), self.e9_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[9][0]), self.e10_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[10][0]), self.e11_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[11][0]), self.e12_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[12][0]), self.e13_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[13][0]), self.e14_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[14][0]), self.e15_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[15][0]), self.e16_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[16][0]), self.e17_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[17][0]), self.e18_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[18][0]), self.e19_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[19][0]), self.e20_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[20][0]), self.e21_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[21][0]), self.e22_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[22][0]), self.e23_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[23][0]), self.e24_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[24][0]), self.e25_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[25][0]), self.e26_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[26][0]), self.e27_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[27][0]), self.e28_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[28][0]), self.e29_TM4)
        scroll_layout1_TM4.addRow(QLabel(self.file[29][0]), self.e30_TM4)

        layout_TM4.addLayout(V2layout_TM4)
        scroll_area_array_TM4.setWidget(set_widget1_TM4)
        H_layout_TM4.addWidget(scroll_area_array_TM4)

        self.nextTm4 = QPushButton('Next', self)
        self.nextTm4.setMaximumWidth(100)
        self.nextTm4.move(980, 900)
        self.nextTm4.clicked.connect(self.next_tab)
        H_layout_TM4.addWidget(self.nextTm4, Qt.AlignTop | Qt.AlignRight)
        H_layout_TM4.addWidget(self.l_TM4)

        V2layout_TM4.addLayout(H_layout_TM4)

        self.setTabText(3, "TM4")
        self.tab4.setLayout(layout_TM4)
        # self.tab2.setLayout(sobaka)

    def tabDf(self):
        self.file = json.load(open('Dataset/TMD.json'))
        # for i in range(len(self.file)):
        #     self.table.setItem(i, 0, QTableWidgetItem(str(self.file[i][0])))
        shapka_TMD = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array_TMD = QScrollArea()
        scroll_area_tab_improvisation_TMD = QScrollArea()

        set_widget1_TMD = QWidget()
        set_widget2_TMD = QWidget()

        scroll_area_tab_improvisation_TMD.setMaximumHeight(100)
        scroll_area_array_TMD.setMaximumWidth(660)
        scroll_layout1_TMD = QFormLayout(set_widget1_TMD)
        H_layout_TMD = QHBoxLayout(set_widget1_TMD)
        scroll_layout2_TMD = QFormLayout(set_widget2_TMD)

        window_tab2_TMD = QWidget()
        layout_TMD = QHBoxLayout(window_tab2_TMD)
        layout2_TMD = QHBoxLayout(set_widget2_TMD)
        layout4_TMD = QHBoxLayout(set_widget2_TMD)
        V2layout_TMD = QVBoxLayout(window_tab2_TMD)
        V2layout_TMD.addWidget(shapka_TMD)

        # Создание кнопок выбора элемента
        self.l_TMD = QLabel()

        self.B1_TMD = QPushButton('1-й элемент', self)
        self.B1_TMD.clicked.connect(self.Pic)
        # self.B1_TMD.clicked.connect(self.dataTm2)

        self.B2_TMD = QPushButton('2-й элемент')
        self.B2_TMD.clicked.connect(self.Pic)

        self.B3_TMD = QPushButton('3-й элемент')
        self.B3_TMD.clicked.connect(self.Pic)

        self.B4_TMD = QPushButton('4-й элемент')
        self.B4_TMD.clicked.connect(self.Pic)

        self.B5_TMD = QPushButton('5-й элемент')
        self.B5_TMD.clicked.connect(self.Pic)

        self.B6_TMD = QPushButton('6-й элемент')
        self.B6_TMD.clicked.connect(self.Pic)

        self.B7_TMD = QPushButton('7-й элемент')
        self.B7_TMD.clicked.connect(self.Pic)

        self.B8_TMD = QPushButton('8-й элемент')
        self.B8_TMD.clicked.connect(self.Pic)

        self.B9_TMD = QPushButton('9-й элемент')
        self.B9_TMD.clicked.connect(self.Pic)

        self.B10_TMD = QPushButton('10-й элемент')
        self.B10_TMD.clicked.connect(self.Pic)

        self.B11_TMD = QPushButton('11-й элемент')
        self.B11_TMD.clicked.connect(self.Pic)

        self.B12_TMD = QPushButton('12-й элемент')
        self.B12_TMD.clicked.connect(self.Pic)

        self.B13_TMD = QPushButton('13-й элемент')
        self.B13_TMD.clicked.connect(self.Pic)

        self.B14_TMD = QPushButton('14-й элемент')
        self.B14_TMD.clicked.connect(self.Pic)

        self.B15_TMD = QPushButton('15-й элемент')
        self.B15_TMD.clicked.connect(self.Pic)

        self.save_param_TMD = QPushButton('Сохранить\nпараметры')
        self.save_param_TMD.setMaximumWidth(100)
        self.inf = QLabel('Information:\nButtons will be accessible after saving parameters')
        self.save_param_TMD.clicked.connect(self.dataTm2)

        layout2_TMD.addWidget(self.B1_TMD)
        layout2_TMD.addWidget(self.B2_TMD)
        layout2_TMD.addWidget(self.B3_TMD)
        layout2_TMD.addWidget(self.B4_TMD)
        layout2_TMD.addWidget(self.B5_TMD)
        layout2_TMD.addWidget(self.B6_TMD)
        layout2_TMD.addWidget(self.B7_TMD)
        layout2_TMD.addWidget(self.B8_TMD)
        layout2_TMD.addWidget(self.B9_TMD)
        layout2_TMD.addWidget(self.B10_TMD)
        layout2_TMD.addWidget(self.B11_TMD)
        layout2_TMD.addWidget(self.B12_TMD)
        layout2_TMD.addWidget(self.B13_TMD)
        layout2_TMD.addWidget(self.B14_TMD)
        layout2_TMD.addWidget(self.B15_TMD)

        layout4_TMD.addWidget(self.save_param_TMD)
        layout4_TMD.addWidget(self.inf)

        scroll_layout2_TMD.insertRow(1, layout2_TMD)
        scroll_layout2_TMD.insertRow(2, layout4_TMD)
        scroll_area_tab_improvisation_TMD.setWidget(set_widget2_TMD)
        V2layout_TMD.addWidget(scroll_area_tab_improvisation_TMD)
        # Кнопки выбора элемента добавлены на слой

        self.e1_TMD = QLineEdit()
        self.e2_TMD = QLineEdit()
        self.e3_TMD = QLineEdit()
        self.e4_TMD = QLineEdit()
        self.e5_TMD = QLineEdit()
        self.e6_TMD = QLineEdit()
        self.e7_TMD = QLineEdit()
        self.e8_TMD = QLineEdit()
        self.e9_TMD = QLineEdit()
        self.e10_TMD = QLineEdit()
        self.e11_TMD = QLineEdit()
        self.e12_TMD = QLineEdit()
        self.e13_TMD = QLineEdit()
        self.e14_TMD = QLineEdit()
        self.e15_TMD = QLineEdit()

        scroll_layout1_TMD.addRow(QLabel(self.file[0][0]), self.e1_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[1][0]), self.e2_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[2][0]), self.e3_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[3][0]), self.e4_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[4][0]), self.e5_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[5][0]), self.e6_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[6][0]), self.e7_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[7][0]), self.e8_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[8][0]), self.e9_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[9][0]), self.e10_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[10][0]), self.e11_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[11][0]), self.e12_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[12][0]), self.e13_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[13][0]), self.e14_TMD)
        scroll_layout1_TMD.addRow(QLabel(self.file[14][0]), self.e15_TMD)

        layout_TMD.addLayout(V2layout_TMD)
        scroll_area_array_TMD.setWidget(set_widget1_TMD)
        H_layout_TMD.addWidget(scroll_area_array_TMD)

        self.nextTMD = QPushButton('Next', self)
        self.nextTMD.setMaximumWidth(100)
        self.nextTMD.move(980, 900)
        self.nextTMD.clicked.connect(self.next_tab)
        H_layout_TMD.addWidget(self.nextTMD, Qt.AlignTop | Qt.AlignRight)
        H_layout_TMD.addWidget(self.l_TMD)

        V2layout_TMD.addLayout(H_layout_TMD)

        self.setTabText(4, "TMD")
        self.tabD.setLayout(layout_TMD)
        # self.tab2.setLayout(sobaka)

    def tabIf(self):
        self.file = json.load(open('Dataset/TMI.json'))
        # for i in range(len(self.file)):
        #     self.table.setItem(i, 0, QTableWidgetItem(str(self.file[i][0])))
        shapka_TMI = QLabel('ПОВЕРХНОСТИ')

        scroll_area_array_TMI = QScrollArea()
        scroll_area_tab_improvisation_TMI = QScrollArea()

        set_widget1_TMI = QWidget()
        set_widget2_TMI = QWidget()

        scroll_area_tab_improvisation_TMI.setMaximumHeight(100)
        scroll_area_array_TMI.setMaximumWidth(660)
        scroll_layout1_TMI = QFormLayout(set_widget1_TMI)
        H_layout_TMI = QHBoxLayout(set_widget1_TMI)
        scroll_layout2_TMI = QFormLayout(set_widget2_TMI)

        window_tab2_TMI = QWidget()
        layout_TMI = QHBoxLayout(window_tab2_TMI)
        layout2_TMI = QHBoxLayout(set_widget2_TMI)
        layout4_TMI = QHBoxLayout(set_widget2_TMI)
        V2layout_TMI = QVBoxLayout(window_tab2_TMI)
        V2layout_TMI.addWidget(shapka_TMI)

        # Создание кнопок выбора элемента
        self.l_TMI = QLabel()

        self.B1_TMI = QPushButton('1-й элемент', self)
        self.B1_TMI.clicked.connect(self.Pic)
        # self.B1_TMI.clicked.connect(self.dataTm2)

        self.B2_TMI = QPushButton('2-й элемент')
        self.B2_TMI.clicked.connect(self.Pic)

        self.B3_TMI = QPushButton('3-й элемент')
        self.B3_TMI.clicked.connect(self.Pic)

        self.B4_TMI = QPushButton('4-й элемент')
        self.B4_TMI.clicked.connect(self.Pic)

        self.B5_TMI = QPushButton('5-й элемент')
        self.B5_TMI.clicked.connect(self.Pic)

        self.B6_TMI = QPushButton('6-й элемент')
        self.B6_TMI.clicked.connect(self.Pic)

        self.B7_TMI = QPushButton('7-й элемент')
        self.B7_TMI.clicked.connect(self.Pic)

        self.B8_TMI = QPushButton('8-й элемент')
        self.B8_TMI.clicked.connect(self.Pic)

        self.B9_TMI = QPushButton('9-й элемент')
        self.B9_TMI.clicked.connect(self.Pic)

        self.B10_TMI = QPushButton('10-й элемент')
        self.B10_TMI.clicked.connect(self.Pic)

        self.B11_TMI = QPushButton('11-й элемент')
        self.B11_TMI.clicked.connect(self.Pic)

        self.B12_TMI = QPushButton('12-й элемент')
        self.B12_TMI.clicked.connect(self.Pic)

        self.B13_TMI = QPushButton('13-й элемент')
        self.B13_TMI.clicked.connect(self.Pic)

        self.B14_TMI = QPushButton('14-й элемент')
        self.B14_TMI.clicked.connect(self.Pic)

        self.B15_TMI = QPushButton('15-й элемент')
        self.B15_TMI.clicked.connect(self.Pic)

        self.save_param_TMI = QPushButton('Сохранить\nпараметры')
        self.save_param_TMI.setMaximumWidth(100)
        self.inf = QLabel('Information:\nButtons will be accessible after saving parameters')
        self.save_param_TMI.clicked.connect(self.dataTm2)

        layout2_TMI.addWidget(self.B1_TMI)
        layout2_TMI.addWidget(self.B2_TMI)
        layout2_TMI.addWidget(self.B3_TMI)
        layout2_TMI.addWidget(self.B4_TMI)
        layout2_TMI.addWidget(self.B5_TMI)
        layout2_TMI.addWidget(self.B6_TMI)
        layout2_TMI.addWidget(self.B7_TMI)
        layout2_TMI.addWidget(self.B8_TMI)
        layout2_TMI.addWidget(self.B9_TMI)
        layout2_TMI.addWidget(self.B10_TMI)
        layout2_TMI.addWidget(self.B11_TMI)
        layout2_TMI.addWidget(self.B12_TMI)
        layout2_TMI.addWidget(self.B13_TMI)
        layout2_TMI.addWidget(self.B14_TMI)
        layout2_TMI.addWidget(self.B15_TMI)

        layout4_TMI.addWidget(self.save_param_TMI)
        layout4_TMI.addWidget(self.inf)

        scroll_layout2_TMI.insertRow(1, layout2_TMI)
        scroll_layout2_TMI.insertRow(2, layout4_TMI)
        scroll_area_tab_improvisation_TMI.setWidget(set_widget2_TMI)
        V2layout_TMI.addWidget(scroll_area_tab_improvisation_TMI)
        # Кнопки выбора элемента добавлены на слой

        self.e1_TMI = QLineEdit()
        self.e2_TMI = QLineEdit()
        self.e3_TMI = QLineEdit()
        self.e4_TMI = QLineEdit()
        self.e5_TMI = QLineEdit()
        self.e6_TMI = QLineEdit()
        self.e7_TMI = QLineEdit()
        self.e8_TMI = QLineEdit()
        self.e9_TMI = QLineEdit()
        self.e10_TMI = QLineEdit()
        self.e11_TMI = QLineEdit()
        self.e12_TMI = QLineEdit()
        self.e13_TMI = QLineEdit()
        self.e14_TMI = QLineEdit()
        self.e15_TMI = QLineEdit()
        self.e16_TMI = QLineEdit()
        self.e17_TMI = QLineEdit()
        self.e18_TMI = QLineEdit()
        self.e19_TMI = QLineEdit()
        self.e20_TMI = QLineEdit()
        self.e21_TMI = QLineEdit()
        self.e22_TMI = QLineEdit()
        self.e23_TMI = QLineEdit()
        self.e24_TMI = QLineEdit()
        self.e25_TMI = QLineEdit()
        self.e26_TMI = QLineEdit()
        self.e27_TMI = QLineEdit()
        self.e28_TMI = QLineEdit()
        self.e29_TMI = QLineEdit()
        self.e30_TMI = QLineEdit()

        scroll_layout1_TMI.addRow(QLabel(self.file[0][0]), self.e1_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[1][0]), self.e2_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[2][0]), self.e3_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[3][0]), self.e4_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[4][0]), self.e5_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[5][0]), self.e6_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[6][0]), self.e7_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[7][0]), self.e8_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[8][0]), self.e9_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[9][0]), self.e10_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[10][0]), self.e11_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[11][0]), self.e12_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[12][0]), self.e13_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[13][0]), self.e14_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[14][0]), self.e15_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[15][0]), self.e16_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[16][0]), self.e17_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[17][0]), self.e18_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[18][0]), self.e19_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[19][0]), self.e20_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[20][0]), self.e21_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[21][0]), self.e22_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[22][0]), self.e23_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[23][0]), self.e24_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[24][0]), self.e25_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[25][0]), self.e26_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[26][0]), self.e27_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[27][0]), self.e28_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[28][0]), self.e29_TMI)
        scroll_layout1_TMI.addRow(QLabel(self.file[29][0]), self.e30_TMI)

        layout_TMI.addLayout(V2layout_TMI)
        scroll_area_array_TMI.setWidget(set_widget1_TMI)
        H_layout_TMI.addWidget(scroll_area_array_TMI)

        self.nextTMI = QPushButton('Next', self)
        self.nextTMI.setMaximumWidth(100)
        self.nextTMI.move(980, 900)
        self.nextTMI.clicked.connect(self.next_tab)
        H_layout_TMI.addWidget(self.nextTMI, Qt.AlignTop | Qt.AlignRight)
        H_layout_TMI.addWidget(self.l_TMI)

        V2layout_TMI.addLayout(H_layout_TMI)

        self.setTabText(5, "TMI")
        self.tabI.setLayout(layout_TMI)
        # self.tab2.setLayout(sobaka)

    def tabAf(self):
        self.file = json.load(open('Dataset/TMA.json'))

        set_widget1_TMA = QWidget()

        H_layout_TMA = QHBoxLayout(set_widget1_TMA)
        V_layout_TMA = QVBoxLayout(set_widget1_TMA)

        window_tab2_TMA = QWidget()
        layout_TMA = QHBoxLayout(window_tab2_TMA)

        self.save_param_TMA = QPushButton('Сохранить\nпараметры')
        self.save_param_TMA.setMaximumWidth(100)
        self.save_param_TMA.clicked.connect(self.dataTm2)

        self.e1_TMA = QLineEdit()
        self.e2_TMA = QLineEdit()
        self.e3_TMA = QLineEdit()
        self.e4_TMA = QLineEdit()

        scroll_layout1_TMA.addRow(QLabel(self.file[0][0]), self.e1_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[1][0]), self.e2_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[2][0]), self.e3_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[3][0]), self.e4_TMA)

        scroll_area_array_TMA.setWidget(set_widget1_TMA)
        H_layout_TMA.addWidget(scroll_area_array_TMA, Qt.AlignTop | Qt.AlignLeft)

        self.nextTMA = QPushButton('Exit', self)
        self.nextTMA.setMaximumWidth(100)
        self.nextTMA.move(980, 900)
        self.nextTMA.clicked.connect(self.next_tab)



        V_layout_TMA.addWidget(self.nextTMA, Qt.AlignTop | Qt.AlignRight)
        V_layout_TMA.addWidget(self.save_param_TMA, Qt.AlignTop | Qt.AlignRight)
        H_layout_TMA.addLayout(V_layout_TMA)

        layout_TMA.addLayout(H_layout_TMA)
        self.setTabText(6, "TMA")
        self.tabA.setLayout(layout_TMA)


    def enabl(self):
        if self.currentIndex() == 1:
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
            self.B3.setEnabled(True)
            self.B2.setEnabled(True)
            self.B1.setEnabled(True)

            hmp = 15-TabUI.image.count(0)
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

        elif self.currentIndex() == 2:
            self.B15_TM3.setEnabled(True)
            self.B14_TM3.setEnabled(True)
            self.B13_TM3.setEnabled(True)
            self.B12_TM3.setEnabled(True)
            self.B11_TM3.setEnabled(True)
            self.B10_TM3.setEnabled(True)
            self.B9_TM3.setEnabled(True)
            self.B8_TM3.setEnabled(True)
            self.B7_TM3.setEnabled(True)
            self.B6_TM3.setEnabled(True)
            self.B5_TM3.setEnabled(True)
            self.B4_TM3.setEnabled(True)
            self.B3_TM3.setEnabled(True)
            self.B2_TM3.setEnabled(True)
            self.B1_TM3.setEnabled(True)

            hmp = 15 - TabUI.image.count(0)
            if hmp < 15:
                self.B15_TM3.setEnabled(False)
                if hmp < 14:
                    self.B14_TM3.setEnabled(False)
                    if hmp < 13:
                        self.B13_TM3.setEnabled(False)
                        if hmp < 12:
                            self.B12_TM3.setEnabled(False)
                            if hmp < 11:
                                self.B11_TM3.setEnabled(False)
                                if hmp < 10:
                                    self.B10_TM3.setEnabled(False)
                                    if hmp < 9:
                                        self.B9_TM3.setEnabled(False)
                                        if hmp < 8:
                                            self.B8_TM3.setEnabled(False)
                                            if hmp < 7:
                                                self.B7_TM3.setEnabled(False)
                                                if hmp < 6:
                                                    self.B6_TM3.setEnabled(False)
                                                    if hmp < 5:
                                                        self.B5_TM3.setEnabled(False)
                                                        if hmp < 4:
                                                            self.B4_TM3.setEnabled(False)

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
        self.setCurrentWidget(self.tab2)
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
            print(row)
        Initialisation.ExcelSaveLoad.my_func('TM1', data, Tab_Widget.XLS_FILE_PATH)
        try:
            sum = int(self.table.item(12, 1).text())+int(self.table.item(13, 1).text())+int(self.table.item(14, 1).text())+int(self.table.item(15, 1).text())+3
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
#Записываем строки в массив для сохранения в ТМ2
    def dataTm2(self):

        self.enabl()
        if self.currentIndex() == 1:
            Tm2 = TabUI.Tm2
            # sender = self.sender()
            e = [self.e1.text(), self.e2.text(), self.e3.text(), self.e4.text(), self.e5.text(), self.e6.text(), self.e7.text(), self.e8.text(), self.e9.text(),
                 self.e10.text(), self.e11.text(), self.e12.text(), self.e13.text(), self.e14.text(), self.e15.text(), self.e16.text(), self.e17.text(), self.e18.text(),
                 self.e19.text(), self.e20.text(), self.e21.text(), self.e22.text(), self.e23.text(), self.e24.text(), self.e25.text(), self.e26.text(), self.e27.text(),
                 self.e28.text(), self.e29.text(), self.e30.text()]
        elif self.currentIndex() == 2:
            Tm2 = TabUI.Tm3
            e = [self.e1_TM3.text(), self.e2_TM3.text(), self.e3_TM3.text(), self.e4_TM3.text(), self.e5_TM3.text(),
                 self.e6_TM3.text(), self.e7_TM3.text(), self.e8_TM3.text(), self.e9_TM3.text(),
                 self.e10_TM3.text(), self.e11_TM3.text(), self.e12_TM3.text(), self.e13_TM3.text(),
                 self.e14_TM3.text(), self.e15_TM3.text(), self.e16_TM3.text(), self.e17_TM3.text(),
                 self.e18_TM3.text(),
                 self.e19_TM3.text(), self.e20_TM3.text(), self.e21_TM3.text(), self.e22_TM3.text(),
                 self.e23_TM3.text(), self.e24_TM3.text(), self.e25_TM3.text(), self.e26_TM3.text(),
                 self.e27_TM3.text(),
                 self.e28_TM3.text(), self.e29_TM3.text(), self.e30_TM3.text()]
        print(e)

        if self.B1.isChecked() or self.B1_TM3.isChecked():
            print('z1')

            for j in range(30):
                if e[j] == '':
                    Tm2[j][0] = '0'
                else:
                    Tm2[j][0] = e[j]

            if self.currentIndex() == 1:
                self.B1.setChecked(False)
            elif self.currentIndex() == 2:
                self.B1_TM3.setChecked(False)

        elif self.B2.isChecked() or self.B1_TM3.isChecked():
            print('z2')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][1] = '0'
                else:
                    Tm2[j][1] = e[j]
            if self.currentIndex() == 1:
                self.B2.setChecked(False)
            elif self.currentIndex() == 2:
                self.B2_TM3.setChecked(False)

        elif self.B3.isChecked() or self.B3_TM3.isChecked():
            print('z3')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][2] = '0'
                else:
                    Tm2[j][2] = e[j]
            if self.currentIndex() == 1:
                self.B3.setChecked(False)
            elif self.currentIndex() == 2:
                self.B3_TM3.setChecked(False)
        elif self.B4.isChecked() or self.B4_TM3.isChecked():
            print('z4')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][3] = '0'
                else:
                    Tm2[j][3] = e[j]
            if self.currentIndex() == 1:
                self.B4.setChecked(False)
            elif self.currentIndex() == 2:
                self.B4_TM3.setChecked(False)
        elif self.B5.isChecked() or self.B5_TM3.isChecked():
            print('z5')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][4] = '0'
                else:
                    Tm2[j][4] = e[j]
            if self.currentIndex() == 1:
                self.B5.setChecked(False)
            elif self.currentIndex() == 2:
                self.B5_TM3.setChecked(False)
        elif self.B6.isChecked() or self.B6_TM3.isChecked():
            print('z6')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][5] = '0'
                else:
                    Tm2[j][5] = e[j]
            if self.currentIndex() == 1:
                self.B6.setChecked(False)
            elif self.currentIndex() == 2:
                self.B6_TM3.setChecked(False)
        elif self.B7.isChecked() or self.B7_TM3.isChecked():
            print('z7')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][6] = '0'
                else:
                    Tm2[j][6] = e[j]
            if self.currentIndex() == 1:
                self.B7.setChecked(False)
            elif self.currentIndex() == 2:
                self.B7_TM3.setChecked(False)
        elif self.B8.isChecked() or self.B8_TM3.isChecked():
            print('z8')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][7] = '0'
                else:
                    Tm2[j][7] = e[j]
            if self.currentIndex() == 1:
                self.B8.setChecked(False)
            elif self.currentIndex() == 2:
                self.B8_TM3.setChecked(False)
        elif self.B9.isChecked() or self.B9_TM3.isChecked():
            print('z9')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][8] = '0'
                else:
                    Tm2[j][8] = e[j]
            if self.currentIndex() == 1:
                self.B9.setChecked(False)
            elif self.currentIndex() == 2:
                self.B9_TM3.setChecked(False)
        elif self.B10.isChecked() or self.B10_TM3.isChecked():
            print('z10')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][9] = '0'
                else:
                    Tm2[j][9] = e[j]
            if self.currentIndex() == 1:
                self.B10.setChecked(False)
            elif self.currentIndex() == 2:
                self.B10_TM3.setChecked(False)
        elif self.B11.isChecked() or self.B11_TM3.isChecked():
            print('z11')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][10] = '0'
                else:
                    Tm2[j][10] = e[j]
            if self.currentIndex() == 1:
                self.B11.setChecked(False)
            elif self.currentIndex() == 2:
                self.B11_TM3.setChecked(False)
        elif self.B12.isChecked() or self.B12_TM3.isChecked():
            print('z12')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][11] = '0'
                else:
                    Tm2[j][11] = e[j]
            if self.currentIndex() == 1:
                self.B12.setChecked(False)
            elif self.currentIndex() == 2:
                self.B12_TM3.setChecked(False)
        elif self.B13.isChecked() or self.B13_TM3.isChecked():
            print('z13')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][12] = '0'
                else:
                    Tm2[j][12] = e[j]
            if self.currentIndex() == 1:
                self.B13.setChecked(False)
            elif self.currentIndex() == 2:
                self.B13_TM3.setChecked(False)
        elif self.B14.isChecked() or self.B14_TM3.isChecked():
            print('z14')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][13] = '0'
                else:
                    Tm2[j][13] = e[j]
            if self.currentIndex() == 1:
                self.B14.setChecked(False)
            elif self.currentIndex() == 2:
                self.B14_TM3.setChecked(False)
        elif self.B15.isChecked() or self.B15_TM3.isChecked():
            print('z15')
            for j in range(30):
                if e[j] == '':
                    Tm2[j][14] = '0'
                else:
                    Tm2[j][14] = e[j]
            if self.currentIndex() == 1:
                self.B15.setChecked(False)
            elif self.currentIndex() == 2:
                self.B15_TM3.setChecked(False)
        print(Tm2)

    def enterTm2(self,i):
        if self.currentIndex() == 1:
            self.e1.setText(str(TabUI.Tm2[0][i]))
            self.e2.setText(str(TabUI.Tm2[1][i]))
            self.e3.setText(str(TabUI.Tm2[2][i]))
            self.e4.setText(str(TabUI.Tm2[3][i]))
            self.e5.setText(str(TabUI.Tm2[4][i]))
            self.e6.setText(str(TabUI.Tm2[5][i]))
            self.e7.setText(str(TabUI.Tm2[6][i]))
            self.e8.setText(str(TabUI.Tm2[7][i]))
            self.e9.setText(str(TabUI.Tm2[8][i]))
            self.e10.setText(str(TabUI.Tm2[9][i]))
            self.e11.setText(str(TabUI.Tm2[10][i]))
            self.e12.setText(str(TabUI.Tm2[11][i]))
            self.e13.setText(str(TabUI.Tm2[12][i]))
            self.e14.setText(str(TabUI.Tm2[13][i]))
            self.e15.setText(str(TabUI.Tm2[14][i]))
            self.e16.setText(str(TabUI.Tm2[15][i]))
            self.e17.setText(str(TabUI.Tm2[16][i]))
            self.e18.setText(str(TabUI.Tm2[17][i]))
            self.e19.setText(str(TabUI.Tm2[18][i]))
            self.e20.setText(str(TabUI.Tm2[19][i]))
            self.e21.setText(str(TabUI.Tm2[20][i]))
            self.e22.setText(str(TabUI.Tm2[21][i]))
            self.e23.setText(str(TabUI.Tm2[22][i]))
            self.e24.setText(str(TabUI.Tm2[23][i]))
            self.e25.setText(str(TabUI.Tm2[24][i]))
            self.e26.setText(str(TabUI.Tm2[25][i]))
            self.e27.setText(str(TabUI.Tm2[26][i]))
            self.e28.setText(str(TabUI.Tm2[27][i]))
            self.e29.setText(str(TabUI.Tm2[28][i]))
            self.e30.setText(str(TabUI.Tm2[29][i]))
        elif self.currentIndex() == 2:
            self.e1_TM3.setText(str(TabUI.Tm3[0][i]))
            self.e2_TM3.setText(str(TabUI.Tm3[1][i]))
            self.e3_TM3.setText(str(TabUI.Tm3[2][i]))
            self.e4_TM3.setText(str(TabUI.Tm3[3][i]))
            self.e5_TM3.setText(str(TabUI.Tm3[4][i]))
            self.e6_TM3.setText(str(TabUI.Tm3[5][i]))
            self.e7_TM3.setText(str(TabUI.Tm3[6][i]))
            self.e8_TM3.setText(str(TabUI.Tm3[7][i]))
            self.e9_TM3.setText(str(TabUI.Tm3[8][i]))
            self.e10_TM3.setText(str(TabUI.Tm3[9][i]))
            self.e11_TM3.setText(str(TabUI.Tm3[10][i]))
            self.e12_TM3.setText(str(TabUI.Tm3[11][i]))
            self.e13_TM3.setText(str(TabUI.Tm3[12][i]))
            self.e14_TM3.setText(str(TabUI.Tm3[13][i]))
            self.e15_TM3.setText(str(TabUI.Tm3[14][i]))
            self.e16_TM3.setText(str(TabUI.Tm3[15][i]))
            self.e17_TM3.setText(str(TabUI.Tm3[16][i]))
            self.e18_TM3.setText(str(TabUI.Tm3[17][i]))
            self.e19_TM3.setText(str(TabUI.Tm3[18][i]))
            self.e20_TM3.setText(str(TabUI.Tm3[19][i]))
            self.e21_TM3.setText(str(TabUI.Tm3[20][i]))
            self.e22_TM3.setText(str(TabUI.Tm3[21][i]))
            self.e23_TM3.setText(str(TabUI.Tm3[22][i]))
            self.e24_TM3.setText(str(TabUI.Tm3[23][i]))
            self.e25_TM3.setText(str(TabUI.Tm3[24][i]))
            self.e26_TM3.setText(str(TabUI.Tm3[25][i]))
            self.e27_TM3.setText(str(TabUI.Tm3[26][i]))
            self.e28_TM3.setText(str(TabUI.Tm3[27][i]))
            self.e29_TM3.setText(str(TabUI.Tm3[28][i]))
            self.e30_TM3.setText(str(TabUI.Tm3[29][i]))

    def Pic(self):
        if self.currentIndex() == 1:
            self.B15.setEnabled(False)
            self.B14.setEnabled(False)
            self.B13.setEnabled(False)
            self.B12.setEnabled(False)
            self.B11.setEnabled(False)
            self.B10.setEnabled(False)
            self.B9.setEnabled(False)
            self.B8.setEnabled(False)
            self.B7.setEnabled(False)
            self.B6.setEnabled(False)
            self.B5.setEnabled(False)
            self.B4.setEnabled(False)
            self.B3.setEnabled(False)
            self.B2.setEnabled(False)
            self.B1.setEnabled(False)

        elif self.currentIndex() == 2:
            self.B15_TM3.setEnabled(False)
            self.B14_TM3.setEnabled(False)
            self.B13_TM3.setEnabled(False)
            self.B12_TM3.setEnabled(False)
            self.B11_TM3.setEnabled(False)
            self.B10_TM3.setEnabled(False)
            self.B9_TM3.setEnabled(False)
            self.B8_TM3.setEnabled(False)
            self.B7_TM3.setEnabled(False)
            self.B6_TM3.setEnabled(False)
            self.B5_TM3.setEnabled(False)
            self.B4_TM3.setEnabled(False)
            self.B3_TM3.setEnabled(False)
            self.B2_TM3.setEnabled(False)
            self.B1_TM3.setEnabled(False)

        sender = self.sender()
        t = sender.text()
        if self.currentIndex() == 1:
            if t == '1 поверхность':
                self.enterTm2(0)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[0])))
            elif t == '2 поверхность':
                self.enterTm2(1)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[1])))
            elif t == '3 поверхность':
                self.enterTm2(2)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[2])))
            elif t == '4 поверхность':
                self.enterTm2(3)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[3])))
            elif t == '5 поверхность':
                self.enterTm2(4)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[4])))
            elif t == '6 поверхность':
                self.enterTm2(5)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[5])))
            elif t == '7 поверхность':
                self.enterTm2(6)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[6])))
            elif t == '8 поверхность':
                self.enterTm2(7)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[7])))
            elif t == '9 поверхность':
                self.enterTm2(8)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[8])))
            elif t == '10 поверхность':
                self.enterTm2(9)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[9])))
            elif t == '11 поверхность':
                self.enterTm2(10)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[10])))
            elif t == '12 поверхность':
                self.enterTm2(11)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[11])))
            elif t == '13 поверхность':
                self.enterTm2(12)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[12])))
            elif t == '14 поверхность':
                self.enterTm2(13)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[13])))
            elif t == '15 поверхность':
                self.enterTm2(14)
                self.l.setPixmap(QPixmap('Pics/' + str(TabUI.image[14])))
        elif self.currentIndex() == 2:
            if t == '1-й элемент':
                self.enterTm2(0)
            elif t == '2-й элемент':
                self.enterTm2(1)
            elif t == '3-й элемент':
                self.enterTm2(2)
            elif t == '4-й элемент':
                self.enterTm2(3)
            elif t == '5-й элемент':
                self.enterTm2(4)
            elif t == '6-й элемент':
                self.enterTm2(5)
            elif t == '7-й элемент':
                self.enterTm2(6)
            elif t == '8-й элемент':
                self.enterTm2(7)
            elif t == '9-й элемент':
                self.enterTm2(8)
            elif t == '10-й элемент':
                self.enterTm2(9)
            elif t == '11-й элемент':
                self.enterTm2(10)
            elif t == '12-й элемент':
                self.enterTm2(11)
            elif t == '13-й элемент':
                self.enterTm2(12)
            elif t == '14-й элемент':
                self.enterTm2(13)
            elif t == '15-й элемент':
                self.enterTm2(14)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())