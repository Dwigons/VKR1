from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout, QScroller, QScrollArea, QComboBox, QCheckBox
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap
import json
import Initialisation, ChoosePic, Dictionary




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
                            TabUI.Tm1[19][0] = '00'
                            TabUI.Tm2 = Array['TM2']
                            TabUI.Tm3 = Array['TM3']
                            TabUI.Tm4 = Array['TM4']
                            TabUI.TMD = Array['TMD']
                            TabUI.TMI = Array['TMI']

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
                TabUI.TMA = Array['TMA']
                TabUI.Tm1 = Array['TM1']
                TabUI.Tm2 = Array['TM2']
                TabUI.Tm3 = Array['TM3']
                TabUI.Tm4 = Array['TM4']
                TabUI.TMD = Array['TMD']
                TabUI.TMI = Array['TMI']

                TabUI.e1_TMA.setText(str(TabUI.TMA[0][0]))
                TabUI.e2_TMA.setText(str(TabUI.TMA[1][0]))
                TabUI.e3_TMA.setText(str(TabUI.TMA[2][0]))
                TabUI.e4_TMA.setText(str(TabUI.TMA[3][0]))
                # for i in range(len(TabUI.Tm1)):
                #     TabUI.table.setItem(i, 1, QTableWidgetItem(str(round(int(TabUI.Tm1[i][0]), 0))))

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


        self.addTab(self.tabA, "TMA")
        self.addTab(self.tab1, "TM1")
        self.addTab(self.tab2, "TM2")
        self.addTab(self.tab3, "TM3")
        self.addTab(self.tab4, "TM4")
        self.addTab(self.tabD, "TMD")
        self.addTab(self.tabI, "TMI")

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
        # self.table.resizeColumnsToContents()

        grid_layout.addWidget(self.table, 0, 0,3,1,Qt.AlignLeft)  # Добавляем таблицу в сетку

        self.code_material = QComboBox(self)
        self.code_material.setMinimumWidth(170)
        for value in Dictionary.material.values():
            self.code_material.addItem(value)
        self.table.setCellWidget(0, 1, self.code_material)

        self.code_profile = QComboBox(self)
        for value in Dictionary.profile.values():
            self.code_profile.addItem(value)
        self.table.setCellWidget(1, 1, self.code_profile)

        self.code_workpiece = QComboBox(self)
        for value in Dictionary.type_workpiece.values():
            self.code_workpiece.addItem(value)
        self.table.setCellWidget(2, 1, self.code_workpiece)

        self.code_HTO = QComboBox(self)
        for value in Dictionary.type_HTO.values():
            self.code_HTO.addItem(value)
        self.table.setCellWidget(6, 1, self.code_HTO)

        widget91 = QWidget()
        layout91 = QVBoxLayout(widget91)
        self.line91 = QLineEdit()

        self.code_cover = QComboBox(self)
        for value in Dictionary.cover.values():
            self.code_cover.addItem(value)
        layout91.addWidget(self.code_cover)
        layout91.addWidget(self.line91)

        self.table.setCellWidget(9, 1, widget91)

        self.code_mashine = QComboBox(self)
        for value in Dictionary.mashine.values():
            self.code_mashine.addItem(value)
        self.table.setCellWidget(19, 1, self.code_mashine)

        self.hole = QCheckBox()
        self.table.setCellWidget(18, 1, self.hole)

        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

        self.saveb = QPushButton('Next', self)
        self.saveb.setMaximumWidth(100)
        # self.proba = QPushButton('Проба', self)
        # self.proba.setMaximumWidth(100)
        # self.proba.setCheckable(False)
        self.saveb.setCheckable(False)
        self.saveb.move(980, 950)
        # self.proba.move(980, 900)

        # self.saveb.setGeometry(1000, 1000, 20, 25)
        grid_layout.addWidget(self.saveb,1,1, Qt.AlignLeft)
        # grid_layout.addWidget(self.proba,2,1, Qt.AlignLeft)

        self.saveb.clicked.connect(self.getData)

        self.setTabText(1, "TM1")
        self.tab1.setLayout(grid_layout)




    def tab2f(self):
        self.file_TM2 = json.load(open('Dataset/TM2.json'))
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
        self.s1 = QLabel('1 ' + self.file_TM2[0][0])
        scroll_layout1.addRow(self.s1, self.e1)
        # scroll_layout1.addRow(QLabel('1 Номинальный диаметр '), self.e1)

        self.e2 = QLineEdit()
        self.s2 = QLabel('2 ' + self.file_TM2[1][0])
        scroll_layout1.addRow(self.s2, self.e2)

        self.e3 = QLineEdit()
        self.s3 = QLabel('3 ' + self.file_TM2[2][0])
        scroll_layout1.addRow(self.s3, self.e3)

        self.e4 = QLineEdit()
        self.s4 = QLabel('4 ' + self.file_TM2[3][0])
        scroll_layout1.addRow(self.s4, self.e4)

        self.e5 = QLineEdit()
        self.s5 = QLabel('5 ' + self.file_TM2[4][0])
        scroll_layout1.addRow(self.s5, self.e5)

        self.e6 = QLineEdit()
        scroll_layout1.addRow(QLabel('6 ' + self.file_TM2[5][0]), self.e6)

        self.e7 = QLineEdit()
        scroll_layout1.addRow(QLabel('7 ' + self.file_TM2[6][0]), self.e7)

        self.e8 = QLineEdit()
        scroll_layout1.addRow(QLabel('8 ' + self.file_TM2[7][0]), self.e8)

        self.e9 = QLineEdit()
        scroll_layout1.addRow(QLabel('9 ' + self.file_TM2[8][0]), self.e9)

        self.e10 = QLineEdit()
        scroll_layout1.addRow(QLabel('10 ' + self.file_TM2[9][0]), self.e10)

        self.e11 = QLineEdit()
        scroll_layout1.addRow(QLabel('11 ' + self.file_TM2[10][0]), self.e11)

        self.e12 = QLineEdit()
        self.s12 = QLabel('12 ' + self.file_TM2[11][0])
        scroll_layout1.addRow(self.s12, self.e12)

        self.e13 = QLineEdit()
        self.s13 = QLabel('13 ' + self.file_TM2[12][0])
        scroll_layout1.addRow(self.s13, self.e13)

        self.e14 = QLineEdit()
        self.s14 = QLabel('14 ' + self.file_TM2[13][0])
        scroll_layout1.addRow(self.s14, self.e14)

        self.e15 = QLineEdit()
        self.s15 = QLabel('15 ' + self.file_TM2[14][0])
        scroll_layout1.addRow(self.s15, self.e15)

        self.e16 = QLineEdit()

        scroll_layout1.addRow(QLabel('16 ' + self.file_TM2[15][0]), self.e16)

        self.e17 = QLineEdit()
        scroll_layout1.addRow(QLabel('17 ' + self.file_TM2[16][0]), self.e17)

        self.e18 = QLineEdit()
        self.s18 = QLabel('18 ' + self.file_TM2[17][0])
        scroll_layout1.addRow(self.s18, self.e18)

        self.e19 = QLineEdit()
        self.s19 = QLabel('19 ' + self.file_TM2[18][0])
        scroll_layout1.addRow(self.s19, self.e19)

        self.e20 = QLineEdit()
        scroll_layout1.addRow(QLabel('20 ' + self.file_TM2[19][0]), self.e20)

        self.e21 = QLineEdit()
        self.s21 = QLabel('21 ' + self.file_TM2[20][0])
        scroll_layout1.addRow(self.s21, self.e21)

        self.e22 = QLineEdit()
        scroll_layout1.addRow(QLabel('22 ' + self.file_TM2[21][0]), self.e22)

        self.e23 = QLineEdit()
        scroll_layout1.addRow(QLabel('23 ' + self.file_TM2[22][0]), self.e23)

        self.e24 = QLineEdit()
        scroll_layout1.addRow(QLabel('24 ' + self.file_TM2[23][0]), self.e24)

        self.e25 = QLineEdit()
        scroll_layout1.addRow(QLabel('25 ' +self.file_TM2[24][0]), self.e25)

        self.e26 = QLineEdit()
        scroll_layout1.addRow(QLabel('26 ' + self.file_TM2[25][0]), self.e26)

        self.e27 = QLineEdit()
        scroll_layout1.addRow(QLabel('27 ' + self.file_TM2[26][0]), self.e27)

        self.e28 = QLineEdit()
        self.s28 = QLabel('28 ' + self.file_TM2[27][0])
        scroll_layout1.addRow(self.s28, self.e28)

        self.e29 = QLineEdit()
        scroll_layout1.addRow(QLabel('29 ' + self.file_TM2[28][0]), self.e29)

        self.e30 = QLineEdit()
        scroll_layout1.addRow(QLabel('30 ' + self.file_TM2[29][0]), self.e30)

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

        self.setTabText(2,"TM2")
        self.tab2.setLayout(layout)


    def tab3f(self):
        self.file = json.load(open('Dataset/TM3.json'))
        # for i in range(len(self.file)):
        #     self.table.setItem(i, 0, QTableWidgetItem(str(self.file[i][0])))
        shapka_TM3 = QLabel('ЭЛЕМЕНТЫ:')

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
        self.B1_TM3.setCheckable(True)
        self.B1_TM3.clicked.connect(self.Pic)
        # self.B1_TM3.clicked.connect(self.dataTm2)

        self.B2_TM3 = QPushButton('2-й элемент')
        self.B2_TM3.setCheckable(True)
        self.B2_TM3.clicked.connect(self.Pic)

        self.B3_TM3 = QPushButton('3-й элемент')
        self.B3_TM3.setCheckable(True)
        self.B3_TM3.clicked.connect(self.Pic)

        self.B4_TM3 = QPushButton('4-й элемент')
        self.B4_TM3.setCheckable(True)
        self.B4_TM3.clicked.connect(self.Pic)

        self.B5_TM3 = QPushButton('5-й элемент')
        self.B5_TM3.setCheckable(True)
        self.B5_TM3.clicked.connect(self.Pic)

        self.B6_TM3 = QPushButton('6-й элемент')
        self.B6_TM3.setCheckable(True)
        self.B6_TM3.clicked.connect(self.Pic)

        self.B7_TM3 = QPushButton('7-й элемент')
        self.B7_TM3.setCheckable(True)
        self.B7_TM3.clicked.connect(self.Pic)

        self.B8_TM3 = QPushButton('8-й элемент')
        self.B8_TM3.setCheckable(True)
        self.B8_TM3.clicked.connect(self.Pic)

        self.B9_TM3 = QPushButton('9-й элемент')
        self.B9_TM3.setCheckable(True)
        self.B9_TM3.clicked.connect(self.Pic)

        self.B10_TM3 = QPushButton('10-й элемент')
        self.B10_TM3.setCheckable(True)
        self.B10_TM3.clicked.connect(self.Pic)

        self.B11_TM3 = QPushButton('11-й элемент')
        self.B11_TM3.setCheckable(True)
        self.B11_TM3.clicked.connect(self.Pic)

        self.B12_TM3 = QPushButton('12-й элемент')
        self.B12_TM3.setCheckable(True)
        self.B12_TM3.clicked.connect(self.Pic)

        self.B13_TM3 = QPushButton('13-й элемент')
        self.B13_TM3.setCheckable(True)
        self.B13_TM3.clicked.connect(self.Pic)

        self.B14_TM3 = QPushButton('14-й элемент')
        self.B14_TM3.setCheckable(True)
        self.B14_TM3.clicked.connect(self.Pic)

        self.B15_TM3 = QPushButton('15-й элемент')
        self.B15_TM3.setCheckable(True)
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

        self.setTabText(3, "TM3")
        self.tab3.setLayout(layout_TM3)
        # self.tab2.setLayout(sobaka)
    def TM3_func(self):
        print('ТМ3Func')
        # self.setCurrentWidget(self.tab4)
        self.setCurrentIndex(self.currentIndex()+1)
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
        self.B1_TM4.setCheckable(True)
        self.B1_TM4.clicked.connect(self.Pic)
        # self.B1_TM4.clicked.connect(self.dataTm2)

        self.B2_TM4 = QPushButton('2-й элемент')
        self.B2_TM4.setCheckable(True)
        self.B2_TM4.clicked.connect(self.Pic)

        self.B3_TM4 = QPushButton('3-й элемент')
        self.B3_TM4.setCheckable(True)
        self.B3_TM4.clicked.connect(self.Pic)

        self.B4_TM4 = QPushButton('4-й элемент')
        self.B4_TM4.setCheckable(True)
        self.B4_TM4.clicked.connect(self.Pic)

        self.B5_TM4 = QPushButton('5-й элемент')
        self.B5_TM4.setCheckable(True)
        self.B5_TM4.clicked.connect(self.Pic)

        self.B6_TM4 = QPushButton('6-й элемент')
        self.B6_TM4.setCheckable(True)
        self.B6_TM4.clicked.connect(self.Pic)

        self.B7_TM4 = QPushButton('7-й элемент')
        self.B7_TM4.setCheckable(True)
        self.B7_TM4.clicked.connect(self.Pic)

        self.B8_TM4 = QPushButton('8-й элемент')
        self.B8_TM4.setCheckable(True)
        self.B8_TM4.clicked.connect(self.Pic)

        self.B9_TM4 = QPushButton('9-й элемент')
        self.B9_TM4.setCheckable(True)
        self.B9_TM4.clicked.connect(self.Pic)

        self.B10_TM4 = QPushButton('10-й элемент')
        self.B10_TM4.setCheckable(True)
        self.B10_TM4.clicked.connect(self.Pic)

        self.B11_TM4 = QPushButton('11-й элемент')
        self.B11_TM4.setCheckable(True)
        self.B11_TM4.clicked.connect(self.Pic)

        self.B12_TM4 = QPushButton('12-й элемент')
        self.B12_TM4.setCheckable(True)
        self.B12_TM4.clicked.connect(self.Pic)

        self.B13_TM4 = QPushButton('13-й элемент')
        self.B13_TM4.setCheckable(True)
        self.B13_TM4.clicked.connect(self.Pic)

        self.B14_TM4 = QPushButton('14-й элемент')
        self.B14_TM4.setCheckable(True)
        self.B14_TM4.clicked.connect(self.Pic)

        self.B15_TM4 = QPushButton('15-й элемент')
        self.B15_TM4.setCheckable(True)
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

        self.setTabText(4, "TM4")
        self.tab4.setLayout(layout_TM4)
        # self.tab2.setLayout(sobaka)

    def next_tab(self):
        if self.currentIndex() == 0:
            Initialisation.ExcelSaveLoad.my_func('TMA', TabUI.TMA, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 1:
            Initialisation.ExcelSaveLoad.my_func('TM1', TabUI.Tm1, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 2:
            Initialisation.ExcelSaveLoad.my_func('TM2', TabUI.Tm2, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 3:
            Initialisation.ExcelSaveLoad.my_func('TM3', TabUI.Tm3, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 4:
            Initialisation.ExcelSaveLoad.my_func('TM4', TabUI.Tm4, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 5:
            Initialisation.ExcelSaveLoad.my_func('TMD', TabUI.TMD, Tab_Widget.XLS_FILE_PATH)
        elif self.currentIndex() == 6:
            Initialisation.ExcelSaveLoad.my_func('TMI', TabUI.TMI, Tab_Widget.XLS_FILE_PATH)
        self.setCurrentIndex(self.currentIndex()+1)


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
        self.B1_TMD.setCheckable(True)
        self.B1_TMD.clicked.connect(self.Pic)
        # self.B1_TMD.clicked.connect(self.dataTm2)

        self.B2_TMD = QPushButton('2-й элемент')
        self.B2_TMD.setCheckable(True)
        self.B2_TMD.clicked.connect(self.Pic)

        self.B3_TMD = QPushButton('3-й элемент')
        self.B3_TMD.setCheckable(True)
        self.B3_TMD.clicked.connect(self.Pic)

        self.B4_TMD = QPushButton('4-й элемент')
        self.B4_TMD.setCheckable(True)
        self.B4_TMD.clicked.connect(self.Pic)

        self.B5_TMD = QPushButton('5-й элемент')
        self.B5_TMD.setCheckable(True)
        self.B5_TMD.clicked.connect(self.Pic)

        self.B6_TMD = QPushButton('6-й элемент')
        self.B6_TMD.setCheckable(True)
        self.B6_TMD.clicked.connect(self.Pic)

        self.B7_TMD = QPushButton('7-й элемент')
        self.B7_TMD.setCheckable(True)
        self.B7_TMD.clicked.connect(self.Pic)

        self.B8_TMD = QPushButton('8-й элемент')
        self.B8_TMD.setCheckable(True)
        self.B8_TMD.clicked.connect(self.Pic)

        self.B9_TMD = QPushButton('9-й элемент')
        self.B9_TMD.setCheckable(True)
        self.B9_TMD.clicked.connect(self.Pic)

        self.B10_TMD = QPushButton('10-й элемент')
        self.B10_TMD.setCheckable(True)
        self.B10_TMD.clicked.connect(self.Pic)

        self.B11_TMD = QPushButton('11-й элемент')
        self.B11_TMD.setCheckable(True)
        self.B11_TMD.clicked.connect(self.Pic)

        self.B12_TMD = QPushButton('12-й элемент')
        self.B12_TMD.setCheckable(True)
        self.B12_TMD.clicked.connect(self.Pic)

        self.B13_TMD = QPushButton('13-й элемент')
        self.B13_TMD.setCheckable(True)
        self.B13_TMD.clicked.connect(self.Pic)

        self.B14_TMD = QPushButton('14-й элемент')
        self.B14_TMD.setCheckable(True)
        self.B14_TMD.clicked.connect(self.Pic)

        self.B15_TMD = QPushButton('15-й элемент')
        self.B15_TMD.setCheckable(True)
        self.B15_TMD.clicked.connect(self.Pic)

        self.B16_TMD = QPushButton('16-й элемент')
        self.B16_TMD.setCheckable(True)
        self.B16_TMD.clicked.connect(self.Pic)

        self.B17_TMD = QPushButton('17-й элемент')
        self.B17_TMD.setCheckable(True)
        self.B17_TMD.clicked.connect(self.Pic)

        self.B18_TMD = QPushButton('18-й элемент')
        self.B18_TMD.setCheckable(True)
        self.B18_TMD.clicked.connect(self.Pic)

        self.B19_TMD = QPushButton('19-й элемент')
        self.B19_TMD.setCheckable(True)
        self.B19_TMD.clicked.connect(self.Pic)

        self.B20_TMD = QPushButton('20-й элемент')
        self.B20_TMD.setCheckable(True)
        self.B20_TMD.clicked.connect(self.Pic)

        self.B21_TMD = QPushButton('21-й элемент')
        self.B21_TMD.setCheckable(True)
        self.B21_TMD.clicked.connect(self.Pic)

        self.B22_TMD = QPushButton('22-й элемент')
        self.B22_TMD.setCheckable(True)
        self.B22_TMD.clicked.connect(self.Pic)

        self.B23_TMD = QPushButton('23-й элемент')
        self.B23_TMD.setCheckable(True)
        self.B23_TMD.clicked.connect(self.Pic)

        self.B24_TMD = QPushButton('24-й элемент')
        self.B24_TMD.setCheckable(True)
        self.B24_TMD.clicked.connect(self.Pic)

        self.B25_TMD = QPushButton('25-й элемент')
        self.B25_TMD.setCheckable(True)
        self.B25_TMD.clicked.connect(self.Pic)

        self.B26_TMD = QPushButton('26-й элемент')
        self.B26_TMD.setCheckable(True)
        self.B26_TMD.clicked.connect(self.Pic)

        self.B27_TMD = QPushButton('27-й элемент')
        self.B27_TMD.setCheckable(True)
        self.B27_TMD.clicked.connect(self.Pic)

        self.B28_TMD = QPushButton('28-й элемент')
        self.B28_TMD.setCheckable(True)
        self.B28_TMD.clicked.connect(self.Pic)

        self.B29_TMD = QPushButton('29-й элемент')
        self.B29_TMD.setCheckable(True)
        self.B29_TMD.clicked.connect(self.Pic)

        self.B30_TMD = QPushButton('30-й элемент')
        self.B30_TMD.setCheckable(True)
        self.B30_TMD.clicked.connect(self.Pic)

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
        layout2_TMD.addWidget(self.B16_TMD)
        layout2_TMD.addWidget(self.B17_TMD)
        layout2_TMD.addWidget(self.B18_TMD)
        layout2_TMD.addWidget(self.B19_TMD)
        layout2_TMD.addWidget(self.B20_TMD)
        layout2_TMD.addWidget(self.B21_TMD)
        layout2_TMD.addWidget(self.B22_TMD)
        layout2_TMD.addWidget(self.B23_TMD)
        layout2_TMD.addWidget(self.B24_TMD)
        layout2_TMD.addWidget(self.B25_TMD)
        layout2_TMD.addWidget(self.B26_TMD)
        layout2_TMD.addWidget(self.B27_TMD)
        layout2_TMD.addWidget(self.B28_TMD)
        layout2_TMD.addWidget(self.B29_TMD)
        layout2_TMD.addWidget(self.B30_TMD)

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

        self.setTabText(5, "TMD")
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
        self.B1_TMI.setCheckable(True)
        self.B1_TMI.clicked.connect(self.Pic)
        # self.B1_TMI.clicked.connect(self.dataTm2)

        self.B2_TMI = QPushButton('2-й элемент')
        self.B2_TMI.setCheckable(True)
        self.B2_TMI.clicked.connect(self.Pic)

        self.B3_TMI = QPushButton('3-й элемент')
        self.B3_TMI.setCheckable(True)
        self.B3_TMI.clicked.connect(self.Pic)

        self.B4_TMI = QPushButton('4-й элемент')
        self.B4_TMI.setCheckable(True)
        self.B4_TMI.clicked.connect(self.Pic)

        self.B5_TMI = QPushButton('5-й элемент')
        self.B5_TMI.setCheckable(True)
        self.B5_TMI.clicked.connect(self.Pic)

        self.B6_TMI = QPushButton('6-й элемент')
        self.B6_TMI.setCheckable(True)
        self.B6_TMI.clicked.connect(self.Pic)

        self.B7_TMI = QPushButton('7-й элемент')
        self.B7_TMI.setCheckable(True)
        self.B7_TMI.clicked.connect(self.Pic)

        self.B8_TMI = QPushButton('8-й элемент')
        self.B8_TMI.setCheckable(True)
        self.B8_TMI.clicked.connect(self.Pic)

        self.B9_TMI = QPushButton('9-й элемент')
        self.B9_TMI.setCheckable(True)
        self.B9_TMI.clicked.connect(self.Pic)

        self.B10_TMI = QPushButton('10-й элемент')
        self.B10_TMI.setCheckable(True)
        self.B10_TMI.clicked.connect(self.Pic)

        self.B11_TMI = QPushButton('11-й элемент')
        self.B11_TMI.setCheckable(True)
        self.B11_TMI.clicked.connect(self.Pic)

        self.B12_TMI = QPushButton('12-й элемент')
        self.B12_TMI.setCheckable(True)
        self.B12_TMI.clicked.connect(self.Pic)

        self.B13_TMI = QPushButton('13-й элемент')
        self.B13_TMI.setCheckable(True)
        self.B13_TMI.clicked.connect(self.Pic)

        self.B14_TMI = QPushButton('14-й элемент')
        self.B14_TMI.setCheckable(True)
        self.B14_TMI.clicked.connect(self.Pic)

        self.B15_TMI = QPushButton('15-й элемент')
        self.B15_TMI.setCheckable(True)
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

        self.setTabText(6, "TMI")
        self.tabI.setLayout(layout_TMI)
        # self.tab2.setLayout(sobaka)

    def tabAf(self):
        self.file = json.load(open('Dataset/TMA.json'))

        set_widget1_TMA = QWidget()
        scroll_layout1_TMA = QFormLayout(set_widget1_TMA)

        H_layout_TMA = QHBoxLayout(set_widget1_TMA)
        V_layout_TMA = QVBoxLayout(set_widget1_TMA)

        layout_TMA = QHBoxLayout()

        self.save_param_TMA = QPushButton('Сохранить\nпараметры')
        self.save_param_TMA.setMaximumWidth(100)
        self.save_param_TMA.clicked.connect(self.dataTm2)

        TabUI.e1_TMA = QLineEdit()
        TabUI.e2_TMA = QLineEdit()
        TabUI.e3_TMA = QLineEdit()
        TabUI.e4_TMA = QLineEdit()

        scroll_layout1_TMA.addRow(QLabel(self.file[0][0]), self.e1_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[1][0]), self.e2_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[2][0]), self.e3_TMA)
        scroll_layout1_TMA.addRow(QLabel(self.file[3][0]), self.e4_TMA)

        H_layout_TMA.addWidget(set_widget1_TMA)

        self.nextTMA = QPushButton('Next', self)
        self.nextTMA.setMaximumWidth(100)
        self.nextTMA.move(980, 900)
        self.nextTMA.clicked.connect(self.next_tab)

        V_layout_TMA.addWidget(self.nextTMA, Qt.AlignTop | Qt.AlignRight)
        V_layout_TMA.addWidget(self.save_param_TMA, Qt.AlignTop | Qt.AlignRight)
        H_layout_TMA.addLayout(V_layout_TMA)

        layout_TMA.addLayout(H_layout_TMA)
        self.setTabText(0, "TMA")
        self.tabA.setLayout(layout_TMA)

    def enabl(self):
        if self.currentIndex() == 2:
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
        elif self.currentIndex() == 3:
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
        elif self.currentIndex() == 4:
            self.B15_TM4.setEnabled(True)
            self.B14_TM4.setEnabled(True)
            self.B13_TM4.setEnabled(True)
            self.B12_TM4.setEnabled(True)
            self.B11_TM4.setEnabled(True)
            self.B10_TM4.setEnabled(True)
            self.B9_TM4.setEnabled(True)
            self.B8_TM4.setEnabled(True)
            self.B7_TM4.setEnabled(True)
            self.B6_TM4.setEnabled(True)
            self.B5_TM4.setEnabled(True)
            self.B4_TM4.setEnabled(True)
            self.B3_TM4.setEnabled(True)
            self.B2_TM4.setEnabled(True)
            self.B1_TM4.setEnabled(True)


            hmp = 15 - TabUI.image.count(0)
            if hmp < 15:
                self.B15_TM4.setEnabled(False)
                if hmp < 14:
                    self.B14_TM4.setEnabled(False)
                    if hmp < 13:
                        self.B13_TM4.setEnabled(False)
                        if hmp < 12:
                            self.B12_TM4.setEnabled(False)
                            if hmp < 11:
                                self.B11_TM4.setEnabled(False)
                                if hmp < 10:
                                    self.B10_TM4.setEnabled(False)
                                    if hmp < 9:
                                        self.B9_TM4.setEnabled(False)
                                        if hmp < 8:
                                            self.B8_TM4.setEnabled(False)
                                            if hmp < 7:
                                                self.B7_TM4.setEnabled(False)
                                                if hmp < 6:
                                                    self.B6_TM4.setEnabled(False)
                                                    if hmp < 5:
                                                        self.B5_TM4.setEnabled(False)
                                                        if hmp < 4:
                                                            self.B4_TM4.setEnabled(False)
        elif self.currentIndex() == 5:
            self.B30_TMD.setEnabled(True)
            self.B29_TMD.setEnabled(True)
            self.B28_TMD.setEnabled(True)
            self.B27_TMD.setEnabled(True)
            self.B26_TMD.setEnabled(True)
            self.B25_TMD.setEnabled(True)
            self.B24_TMD.setEnabled(True)
            self.B23_TMD.setEnabled(True)
            self.B22_TMD.setEnabled(True)
            self.B21_TMD.setEnabled(True)
            self.B20_TMD.setEnabled(True)
            self.B19_TMD.setEnabled(True)
            self.B18_TMD.setEnabled(True)
            self.B17_TMD.setEnabled(True)
            self.B16_TMD.setEnabled(True)
            self.B15_TMD.setEnabled(True)
            self.B14_TMD.setEnabled(True)
            self.B13_TMD.setEnabled(True)
            self.B12_TMD.setEnabled(True)
            self.B11_TMD.setEnabled(True)
            self.B10_TMD.setEnabled(True)
            self.B9_TMD.setEnabled(True)
            self.B8_TMD.setEnabled(True)
            self.B7_TMD.setEnabled(True)
            self.B6_TMD.setEnabled(True)
            self.B5_TMD.setEnabled(True)
            self.B4_TMD.setEnabled(True)
            self.B3_TMD.setEnabled(True)
            self.B2_TMD.setEnabled(True)
            self.B1_TMD.setEnabled(True)


            hmp = 15 - TabUI.image.count(0)
            if hmp < 15:
                self.B15_TMD.setEnabled(False)
                if hmp < 14:
                    self.B14_TMD.setEnabled(False)
                    if hmp < 13:
                        self.B13_TMD.setEnabled(False)
                        if hmp < 12:
                            self.B12_TMD.setEnabled(False)
                            if hmp < 11:
                                self.B11_TMD.setEnabled(False)
                                if hmp < 10:
                                    self.B10_TMD.setEnabled(False)
                                    if hmp < 9:
                                        self.B9_TMD.setEnabled(False)
                                        if hmp < 8:
                                            self.B8_TMD.setEnabled(False)
                                            if hmp < 7:
                                                self.B7_TMD.setEnabled(False)
                                                if hmp < 6:
                                                    self.B6_TMD.setEnabled(False)
                                                    if hmp < 5:
                                                        self.B5_TMD.setEnabled(False)
                                                        if hmp < 4:
                                                            self.B4_TMD.setEnabled(False)
        elif self.currentIndex() == 6:
            self.B15_TMI.setEnabled(True)
            self.B14_TMI.setEnabled(True)
            self.B13_TMI.setEnabled(True)
            self.B12_TMI.setEnabled(True)
            self.B11_TMI.setEnabled(True)
            self.B10_TMI.setEnabled(True)
            self.B9_TMI.setEnabled(True)
            self.B8_TMI.setEnabled(True)
            self.B7_TMI.setEnabled(True)
            self.B6_TMI.setEnabled(True)
            self.B5_TMI.setEnabled(True)
            self.B4_TMI.setEnabled(True)
            self.B3_TMI.setEnabled(True)
            self.B2_TMI.setEnabled(True)
            self.B1_TMI.setEnabled(True)


            hmp = 15 - TabUI.image.count(0)
            if hmp < 15:
                self.B15_TMI.setEnabled(False)
                if hmp < 14:
                    self.B14_TMI.setEnabled(False)
                    if hmp < 13:
                        self.B13_TMI.setEnabled(False)
                        if hmp < 12:
                            self.B12_TMI.setEnabled(False)
                            if hmp < 11:
                                self.B11_TMI.setEnabled(False)
                                if hmp < 10:
                                    self.B10_TMI.setEnabled(False)
                                    if hmp < 9:
                                        self.B9_TMI.setEnabled(False)
                                        if hmp < 8:
                                            self.B8_TMI.setEnabled(False)
                                            if hmp < 7:
                                                self.B7_TMI.setEnabled(False)
                                                if hmp < 6:
                                                    self.B6_TMI.setEnabled(False)
                                                    if hmp < 5:
                                                        self.B5_TMI.setEnabled(False)
                                                        if hmp < 4:
                                                            self.B4_TMI.setEnabled(False)

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
        Initialisation.ExcelSaveLoad.my_func('TM1', data, Tab_Widget.XLS_FILE_PATH)

        try:
            sum = int(self.table.item(12, 1).text())+int(self.table.item(13, 1).text())+int(self.table.item(14, 1).text())+int(self.table.item(15, 1).text())+3
            print(sum)
            # TabUI.image = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            for i in range(1, sum):
                print(ChoosePic.ChoosePic(data, i))
                TabUI.image[i-1] = ChoosePic.ChoosePic(data, i)
            print(data)
            print(TabUI.image)
            self.enabl()
            self.B1.click()
        except:
            self.Message()
#Записываем строки в массив для сохранения в ТМ2
    def dataTm2(self):

        self.enabl()
        if self.currentIndex() == 0:
            Tm2 = TabUI.TMA
            # sender = self.sender()
            e = [TabUI.e1_TMA.text(), TabUI.e2_TMA.text(), TabUI.e3_TMA.text(), TabUI.e4_TMA.text()]

        if self.currentIndex() == 2:
            Tm2 = TabUI.Tm2
            # sender = self.sender()
            e = [self.e1.text(), self.e2.text(), self.e3.text(), self.e4.text(), self.e5.text(), self.e6.text(), self.e7.text(), self.e8.text(), self.e9.text(),
                 self.e10.text(), self.e11.text(), self.e12.text(), self.e13.text(), self.e14.text(), self.e15.text(), self.e16.text(), self.e17.text(), self.e18.text(),
                 self.e19.text(), self.e20.text(), self.e21.text(), self.e22.text(), self.e23.text(), self.e24.text(), self.e25.text(), self.e26.text(), self.e27.text(),
                 self.e28.text(), self.e29.text(), self.e30.text()]
        elif self.currentIndex() == 3:
            Tm2 = TabUI.Tm3
            e = [self.e1_TM3.text(), self.e2_TM3.text(), self.e3_TM3.text(), self.e4_TM3.text(), self.e5_TM3.text(), self.e6_TM3.text(), self.e7_TM3.text(), self.e8_TM3.text(), self.e9_TM3.text(),
                 self.e10_TM3.text(), self.e11_TM3.text(), self.e12_TM3.text(), self.e13_TM3.text(), self.e14_TM3.text(), self.e15_TM3.text(), self.e16_TM3.text(), self.e17_TM3.text(), self.e18_TM3.text(),
                 self.e19_TM3.text(), self.e20_TM3.text(), self.e21_TM3.text(), self.e22_TM3.text(), self.e23_TM3.text(), self.e24_TM3.text(), self.e25_TM3.text(), self.e26_TM3.text(), self.e27_TM3.text(),
                 self.e28_TM3.text(), self.e29_TM3.text(), self.e30_TM3.text()]
        elif self.currentIndex() == 4:
            Tm2 = TabUI.Tm4
            e = [self.e1_TM4.text(), self.e2_TM4.text(), self.e3_TM4.text(), self.e4_TM4.text(), self.e5_TM4.text(), self.e6_TM4.text(), self.e7_TM4.text(), self.e8_TM4.text(), self.e9_TM4.text(),
                 self.e10_TM4.text(), self.e11_TM4.text(), self.e12_TM4.text(), self.e13_TM4.text(), self.e14_TM4.text(), self.e15_TM4.text(), self.e16_TM4.text(), self.e17_TM4.text(), self.e18_TM4.text(),
                 self.e19_TM4.text(), self.e20_TM4.text(), self.e21_TM4.text(), self.e22_TM4.text(), self.e23_TM4.text(), self.e24_TM4.text(), self.e25_TM4.text(), self.e26_TM4.text(), self.e27_TM4.text(),
                 self.e28_TM4.text(), self.e29_TM4.text(), self.e30_TM4.text()]
        elif self.currentIndex() == 5:
            Tm2 = TabUI.TMD
            e = [self.e1_TMD.text(), self.e2_TMD.text(), self.e3_TMD.text(), self.e4_TMD.text(), self.e5_TMD.text(), self.e6_TMD.text(), self.e7_TMD.text(), self.e8_TMD.text(), self.e9_TMD.text(),
                 self.e10_TMD.text(), self.e11_TMD.text(), self.e12_TMD.text(), self.e13_TMD.text(), self.e14_TMD.text(), self.e15_TMD.text()]
        elif self.currentIndex() == 6:
            Tm2 = TabUI.TMI
            e = [self.e1_TMI.text(), self.e2_TMI.text(), self.e3_TMI.text(), self.e4_TMI.text(), self.e5_TMI.text(), self.e6_TMI.text(), self.e7_TMI.text(), self.e8_TMI.text(), self.e9_TMI.text(),
                 self.e10_TMI.text(), self.e11_TMI.text(), self.e12_TMI.text(), self.e13_TMI.text(), self.e14_TMI.text(), self.e15_TMI.text(), self.e16_TMI.text(), self.e17_TMI.text(), self.e18_TMI.text(),
                 self.e19_TMI.text(), self.e20_TMI.text(), self.e21_TMI.text(), self.e22_TMI.text(), self.e23_TMI.text(), self.e24_TMI.text(), self.e25_TMI.text(), self.e26_TMI.text(), self.e27_TMI.text(),
                 self.e28_TMI.text(), self.e29_TMI.text(), self.e30_TMI.text()]
        
        if self.currentIndex() != 5 and self.currentIndex() != 0:
            if self.B1.isChecked() or self.B1_TM3.isChecked() or self.B1_TM4.isChecked() or self.B1_TMI.isChecked():
                print('1-й запись начата')
                for j in range(30):
                    print('check ' + str(j))
                    if e[j] == '':
                        Tm2[j][0] = '0'
                    else:
                        Tm2[j][0] = e[j]
                # self.B1.setChecked(False)
                if self.currentIndex() == 2:
                    self.B1.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B1_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B1_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B1_TMI.setChecked(False)
            elif self.B2.isChecked()  or self.B2_TM3.isChecked() or self.B2_TM4.isChecked() or self.B2_TMI.isChecked():
                print('2-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][1] = '0'
                    else:
                        Tm2[j][1] = e[j]
                if self.currentIndex() == 2:
                    self.B2.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B2_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B2_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B2_TMI.setChecked(False)
            elif self.B3.isChecked() or self.B3_TM3.isChecked() or self.B3_TM4.isChecked() or self.B3_TMI.isChecked():
                print('3-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][2] = '0'
                    else:
                        Tm2[j][2] = e[j]
                if self.currentIndex() == 2:
                    self.B3.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B3_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B3_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B3_TMI.setChecked(False)

            elif self.B4.isChecked() or self.B4_TM3.isChecked() or self.B4_TM4.isChecked()or self.B4_TMI.isChecked():
                print('4-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][3] = '0'
                    else:
                        Tm2[j][3] = e[j]
                if self.currentIndex() == 2:
                    self.B4.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B4_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B4_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B4_TMI.setChecked(False)
            elif self.B5.isChecked() or self.B5_TM3.isChecked() or self.B5_TM4.isChecked() or self.B5_TMI.isChecked():
                print('5-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][4] = '0'
                    else:
                        Tm2[j][4] = e[j]
                if self.currentIndex() == 2:
                    self.B5.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B5_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B5_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B5_TMI.setChecked(False)
            elif self.B6.isChecked() or self.B6_TM3.isChecked() or self.B6_TM4.isChecked() or self.B6_TMI.isChecked():
                print('6-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][5] = '0'
                    else:
                        Tm2[j][5] = e[j]
                if self.currentIndex() == 2:
                    self.B6.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B6_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B6_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B6_TMI.setChecked(False)
            elif self.B7.isChecked() or self.B7_TM3.isChecked() or self.B7_TM4.isChecked() or self.B7_TMI.isChecked():
                print('7-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][6] = '0'
                    else:
                        Tm2[j][6] = e[j]
                if self.currentIndex() == 2:
                    self.B7.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B7_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B7_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B7_TMI.setChecked(False)
            elif self.B8.isChecked() or self.B8_TM3.isChecked() or self.B8_TM4.isChecked() or self.B8_TMI.isChecked():
                print('8-й записан')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][7] = '0'
                    else:
                        Tm2[j][7] = e[j]
                if self.currentIndex() == 2:
                    self.B8.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B8_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B8_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B8_TMI.setChecked(False)
            elif self.B9.isChecked() or self.B9_TM3.isChecked() or self.B9_TM4.isChecked() or self.B9_TMI.isChecked():
                print('z9')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][8] = '0'
                    else:
                        Tm2[j][8] = e[j]
                if self.currentIndex() == 2:
                    self.B9.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B9_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B9_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B9_TMI.setChecked(False)
            elif self.B10.isChecked() or self.B10_TM3.isChecked() or self.B10_TM4.isChecked() or self.B10_TMI.isChecked():
                print('z10')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][9] = '0'
                    else:
                        Tm2[j][9] = e[j]
                if self.currentIndex() == 2:
                    self.B10.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B10_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B10_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B10_TMI.setChecked(False)
            elif self.B11.isChecked() or self.B11_TM3.isChecked() or self.B11_TM4.isChecked() or self.B11_TMI.isChecked():
                print('z11')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][10] = '0'
                    else:
                        Tm2[j][10] = e[j]
                if self.currentIndex() == 2:
                    self.B11.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B11_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B11_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B11_TMI.setChecked(False)
            elif self.B12.isChecked() or self.B12_TM3.isChecked() or self.B12_TM4.isChecked() or self.B12_TMI.isChecked():
                print('z12')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][11] = '0'
                    else:
                        Tm2[j][11] = e[j]
                if self.currentIndex() == 2:
                    self.B12.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B12_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B12_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B12_TMI.setChecked(False)
            elif self.B13.isChecked() or self.B13_TM3.isChecked() or self.B13_TM4.isChecked() or self.B13_TMI.isChecked():
                print('z13')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][12] = '0'
                    else:
                        Tm2[j][12] = e[j]
                if self.currentIndex() == 2:
                    self.B13.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B13_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B13_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B13_TMI.setChecked(False)
            elif self.B14.isChecked() or self.B14_TM3.isChecked() or self.B14_TM4.isChecked() or self.B14_TMI.isChecked():
                print('z14')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][13] = '0'
                    else:
                        Tm2[j][13] = e[j]
                if self.currentIndex() == 2:
                    self.B14.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B14_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B14_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B14_TMI.setChecked(False)
            elif self.B15.isChecked() or self.B15_TM3.isChecked() or self.B15_TM4.isChecked() or self.B15_TMI.isChecked():
                print('z15')
                for j in range(30):
                    if e[j] == '':
                        Tm2[j][14] = '0'
                    else:
                        Tm2[j][14] = e[j]
                if self.currentIndex() == 2:
                    self.B15.setChecked(False)
                elif self.currentIndex() == 3:
                    self.B15_TM3.setChecked(False)
                elif self.currentIndex() == 4:
                    self.B15_TM4.setChecked(False)
                elif self.currentIndex() == 6:
                    self.B15_TMI.setChecked(False)
        elif self.currentIndex() == 5:
            if self.B1_TMD.isChecked():
                print('ТМД 1-й запись начата')
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][0] = '0'
                    else:
                        Tm2[j][0] = e[j]
                self.B1_TMD.setChecked(False)
                print('ТМД 1-й записан')
            elif self.B2_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][1] = '0'
                    else:
                        Tm2[j][1] = e[j]
                self.B2_TMD.setChecked(False)
                print('ТМД 2-й записан')
            elif self.B3_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][2] = '0'
                    else:
                        Tm2[j][2] = e[j]
                self.B3_TMD.setChecked(False)
                print('ТМД 3-й записан')

            elif self.B4_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][3] = '0'
                    else:
                        Tm2[j][3] = e[j]
                self.B4_TMD.setChecked(False)
                print('ТМД 4-й записан')

            elif self.B5_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][4] = '0'
                    else:
                        Tm2[j][4] = e[j]
                self.B5_TMD.setChecked(False)
                print('ТМД 5-й записан')

            elif self.B6_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][5] = '0'
                    else:
                        Tm2[j][5] = e[j]
                self.B6_TMD.setChecked(False)
                print('ТМД 6-й записан')

            elif self.B7_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][6] = '0'
                    else:
                        Tm2[j][6] = e[j]
                self.B7_TMD.setChecked(False)
                print('ТМД 7-й записан')

            elif self.B8_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][7] = '0'
                    else:
                        Tm2[j][7] = e[j]
                self.B8_TMD.setChecked(False)
                print('ТМД 8-й записан')

            elif self.B9_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][8] = '0'
                    else:
                        Tm2[j][8] = e[j]
                self.B9_TMD.setChecked(False)
                print('ТМД 9-й записан')

            elif self.B10_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][9] = '0'
                    else:
                        Tm2[j][9] = e[j]
                self.B10_TMD.setChecked(False)
                print('ТМД 10-й записан')

            elif self.B11_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][10] = '0'
                    else:
                        Tm2[j][10] = e[j]
                self.B11_TMD.setChecked(False)
                print('ТМД 11-й записан')

            elif self.B12_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][11] = '0'
                    else:
                        Tm2[j][11] = e[j]
                self.B12_TMD.setChecked(False)
                print('ТМД 12-й записан')

            elif self.B13_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][12] = '0'
                    else:
                        Tm2[j][12] = e[j]
                self.B13_TMD.setChecked(False)
                print('ТМД 13-й записан')

            elif self.B14_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][13] = '0'
                    else:
                        Tm2[j][13] = e[j]
                self.B14_TMD.setChecked(False)
                print('ТМД 14-й записан')

            elif self.B15_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][14] = '0'
                    else:
                        Tm2[j][14] = e[j]
                self.B15_TMD.setChecked(False)
                print('ТМД 15-й записан')

            elif self.B16_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][15] = '0'
                    else:
                        Tm2[j][15] = e[j]
                self.B16_TMD.setChecked(False)
                print('ТМД 16-й записан')

            elif self.B17_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][16] = '0'
                    else:
                        Tm2[j][16] = e[j]
                self.B17_TMD.setChecked(False)
                print('ТМД 17-й записан')

            elif self.B18_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][17] = '0'
                    else:
                        Tm2[j][17] = e[j]
                self.B18_TMD.setChecked(False)
                print('ТМД 18-й записан')

            elif self.B19_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][18] = '0'
                    else:
                        Tm2[j][18] = e[j]
                self.B19_TMD.setChecked(False)
                print('ТМД 19-й записан')

            elif self.B20_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][19] = '0'
                    else:
                        Tm2[j][19] = e[j]
                self.B20_TMD.setChecked(False)
                print('ТМД 20-й записан')

            elif self.B21_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][20] = '0'
                    else:
                        Tm2[j][20] = e[j]
                self.B21_TMD.setChecked(False)
                print('ТМД 21-й записан')

            elif self.B22_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][21] = '0'
                    else:
                        Tm2[j][21] = e[j]
                self.B22_TMD.setChecked(False)
                print('ТМД 22-й записан')

            elif self.B23_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][22] = '0'
                    else:
                        Tm2[j][22] = e[j]
                self.B23_TMD.setChecked(False)
                print('ТМД 23-й записан')

            elif self.B24_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][23] = '0'
                    else:
                        Tm2[j][23] = e[j]
                self.B24_TMD.setChecked(False)
                print('ТМД 24-й записан')

            elif self.B25_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][24] = '0'
                    else:
                        Tm2[j][24] = e[j]
                self.B25_TMD.setChecked(False)
                print('ТМД 25-й записан')

            elif self.B26_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][25] = '0'
                    else:
                        Tm2[j][25] = e[j]
                self.B26_TMD.setChecked(False)
                print('ТМД 26-й записан')

            elif self.B27_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][26] = '0'
                    else:
                        Tm2[j][26] = e[j]
                self.B27_TMD.setChecked(False)
                print('ТМД 27-й записан')

            elif self.B28_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][27] = '0'
                    else:
                        Tm2[j][27] = e[j]
                self.B28_TMD.setChecked(False)
                print('ТМД 28-й записан')

            elif self.B29_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][28] = '0'
                    else:
                        Tm2[j][28] = e[j]
                self.B29_TMD.setChecked(False)
                print('ТМД 29-й записан')

            elif self.B30_TMD.isChecked():
                for j in range(15):
                    if e[j] == '':
                        Tm2[j][29] = '0'
                    else:
                        Tm2[j][29] = e[j]
                self.B30_TMD.setChecked(False)
                print('ТМД 30-й записан')

        elif self.currentIndex() == 0:
            for j in range(4):
                if e[j] == '':
                    Tm2[j][0] = '0'
                else:
                    Tm2[j][0] = e[j]
            print('ТМА записан')
        print(Tm2)


    def enterTm2(self,i):
        if self.currentIndex() == 0:
            self.e1_TMA.setText(str(TabUI.TMA[0][i]))
            self.e2_TMA.setText(str(TabUI.TMA[1][i]))
            self.e3_TMA.setText(str(TabUI.TMA[2][i]))
            self.e4_TMA.setText(str(TabUI.TMA[3][i]))
        elif self.currentIndex() == 2:
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
        elif self.currentIndex() == 3:
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
        elif self.currentIndex() == 4:
            self.e1_TM4.setText(str(TabUI.Tm4[0][i]))
            self.e2_TM4.setText(str(TabUI.Tm4[1][i]))
            self.e3_TM4.setText(str(TabUI.Tm4[2][i]))
            self.e4_TM4.setText(str(TabUI.Tm4[3][i]))
            self.e5_TM4.setText(str(TabUI.Tm4[4][i]))
            self.e6_TM4.setText(str(TabUI.Tm4[5][i]))
            self.e7_TM4.setText(str(TabUI.Tm4[6][i]))
            self.e8_TM4.setText(str(TabUI.Tm4[7][i]))
            self.e9_TM4.setText(str(TabUI.Tm4[8][i]))
            self.e10_TM4.setText(str(TabUI.Tm4[9][i]))
            self.e11_TM4.setText(str(TabUI.Tm4[10][i]))
            self.e12_TM4.setText(str(TabUI.Tm4[11][i]))
            self.e13_TM4.setText(str(TabUI.Tm4[12][i]))
            self.e14_TM4.setText(str(TabUI.Tm4[13][i]))
            self.e15_TM4.setText(str(TabUI.Tm4[14][i]))
            self.e16_TM4.setText(str(TabUI.Tm4[15][i]))
            self.e17_TM4.setText(str(TabUI.Tm4[16][i]))
            self.e18_TM4.setText(str(TabUI.Tm4[17][i]))
            self.e19_TM4.setText(str(TabUI.Tm4[18][i]))
            self.e20_TM4.setText(str(TabUI.Tm4[19][i]))
            self.e21_TM4.setText(str(TabUI.Tm4[20][i]))
            self.e22_TM4.setText(str(TabUI.Tm4[21][i]))
            self.e23_TM4.setText(str(TabUI.Tm4[22][i]))
            self.e24_TM4.setText(str(TabUI.Tm4[23][i]))
            self.e25_TM4.setText(str(TabUI.Tm4[24][i]))
            self.e26_TM4.setText(str(TabUI.Tm4[25][i]))
            self.e27_TM4.setText(str(TabUI.Tm4[26][i]))
            self.e28_TM4.setText(str(TabUI.Tm4[27][i]))
            self.e29_TM4.setText(str(TabUI.Tm4[28][i]))
            self.e30_TM4.setText(str(TabUI.Tm4[29][i]))

        elif self.currentIndex() == 5:
            self.e1_TMD.setText(str(TabUI.TMD[0][i]))
            self.e2_TMD.setText(str(TabUI.TMD[1][i]))
            self.e3_TMD.setText(str(TabUI.TMD[2][i]))
            self.e4_TMD.setText(str(TabUI.TMD[3][i]))
            self.e5_TMD.setText(str(TabUI.TMD[4][i]))
            self.e6_TMD.setText(str(TabUI.TMD[5][i]))
            self.e7_TMD.setText(str(TabUI.TMD[6][i]))
            self.e8_TMD.setText(str(TabUI.TMD[7][i]))
            self.e9_TMD.setText(str(TabUI.TMD[8][i]))
            self.e10_TMD.setText(str(TabUI.TMD[9][i]))
            self.e11_TMD.setText(str(TabUI.TMD[10][i]))
            self.e12_TMD.setText(str(TabUI.TMD[11][i]))
            self.e13_TMD.setText(str(TabUI.TMD[12][i]))
            self.e14_TMD.setText(str(TabUI.TMD[13][i]))
            self.e15_TMD.setText(str(TabUI.TMD[14][i]))
            
        elif self.currentIndex() == 6:
            self.e1_TMI.setText(str(TabUI.TMI[0][i]))
            self.e2_TMI.setText(str(TabUI.TMI[1][i]))
            self.e3_TMI.setText(str(TabUI.TMI[2][i]))
            self.e4_TMI.setText(str(TabUI.TMI[3][i]))
            self.e5_TMI.setText(str(TabUI.TMI[4][i]))
            self.e6_TMI.setText(str(TabUI.TMI[5][i]))
            self.e7_TMI.setText(str(TabUI.TMI[6][i]))
            self.e8_TMI.setText(str(TabUI.TMI[7][i]))
            self.e9_TMI.setText(str(TabUI.TMI[8][i]))
            self.e10_TMI.setText(str(TabUI.TMI[9][i]))
            self.e11_TMI.setText(str(TabUI.TMI[10][i]))
            self.e12_TMI.setText(str(TabUI.TMI[11][i]))
            self.e13_TMI.setText(str(TabUI.TMI[12][i]))
            self.e14_TMI.setText(str(TabUI.TMI[13][i]))
            self.e15_TMI.setText(str(TabUI.TMI[14][i]))
            self.e16_TMI.setText(str(TabUI.TMI[15][i]))
            self.e17_TMI.setText(str(TabUI.TMI[16][i]))
            self.e18_TMI.setText(str(TabUI.TMI[17][i]))
            self.e19_TMI.setText(str(TabUI.TMI[18][i]))
            self.e20_TMI.setText(str(TabUI.TMI[19][i]))
            self.e21_TMI.setText(str(TabUI.TMI[20][i]))
            self.e22_TMI.setText(str(TabUI.TMI[21][i]))
            self.e23_TMI.setText(str(TabUI.TMI[22][i]))
            self.e24_TMI.setText(str(TabUI.TMI[23][i]))
            self.e25_TMI.setText(str(TabUI.TMI[24][i]))
            self.e26_TMI.setText(str(TabUI.TMI[25][i]))
            self.e27_TMI.setText(str(TabUI.TMI[26][i]))
            self.e28_TMI.setText(str(TabUI.TMI[27][i]))
            self.e29_TMI.setText(str(TabUI.TMI[28][i]))
            self.e30_TMI.setText(str(TabUI.TMI[29][i]))
           


    def Pic(self):
        if self.currentIndex() == 2:
            sender = self.sender()
            print(sender.text()+'ONO')
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

        elif self.currentIndex() == 3:
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
        elif self.currentIndex() == 4:
            self.B15_TM4.setEnabled(False)
            self.B14_TM4.setEnabled(False)
            self.B13_TM4.setEnabled(False)
            self.B12_TM4.setEnabled(False)
            self.B11_TM4.setEnabled(False)
            self.B10_TM4.setEnabled(False)
            self.B9_TM4.setEnabled(False)
            self.B8_TM4.setEnabled(False)
            self.B7_TM4.setEnabled(False)
            self.B6_TM4.setEnabled(False)
            self.B5_TM4.setEnabled(False)
            self.B4_TM4.setEnabled(False)
            self.B3_TM4.setEnabled(False)
            self.B2_TM4.setEnabled(False)
            self.B1_TM4.setEnabled(False)
            
        elif self.currentIndex() == 5:
            self.B30_TMD.setEnabled(False)
            self.B29_TMD.setEnabled(False)
            self.B28_TMD.setEnabled(False)
            self.B27_TMD.setEnabled(False)
            self.B26_TMD.setEnabled(False)
            self.B25_TMD.setEnabled(False)
            self.B24_TMD.setEnabled(False)
            self.B23_TMD.setEnabled(False)
            self.B22_TMD.setEnabled(False)
            self.B21_TMD.setEnabled(False)
            self.B20_TMD.setEnabled(False)
            self.B19_TMD.setEnabled(False)
            self.B18_TMD.setEnabled(False)
            self.B17_TMD.setEnabled(False)
            self.B16_TMD.setEnabled(False)
            self.B15_TMD.setEnabled(False)
            self.B14_TMD.setEnabled(False)
            self.B13_TMD.setEnabled(False)
            self.B12_TMD.setEnabled(False)
            self.B11_TMD.setEnabled(False)
            self.B10_TMD.setEnabled(False)
            self.B9_TMD.setEnabled(False)
            self.B8_TMD.setEnabled(False)
            self.B7_TMD.setEnabled(False)
            self.B6_TMD.setEnabled(False)
            self.B5_TMD.setEnabled(False)
            self.B4_TMD.setEnabled(False)
            self.B3_TMD.setEnabled(False)
            self.B2_TMD.setEnabled(False)
            self.B1_TMD.setEnabled(False)
        elif self.currentIndex() == 6:
            self.B15_TMI.setEnabled(False)
            self.B14_TMI.setEnabled(False)
            self.B13_TMI.setEnabled(False)
            self.B12_TMI.setEnabled(False)
            self.B11_TMI.setEnabled(False)
            self.B10_TMI.setEnabled(False)
            self.B9_TMI.setEnabled(False)
            self.B8_TMI.setEnabled(False)
            self.B7_TMI.setEnabled(False)
            self.B6_TMI.setEnabled(False)
            self.B5_TMI.setEnabled(False)
            self.B4_TMI.setEnabled(False)
            self.B3_TMI.setEnabled(False)
            self.B2_TMI.setEnabled(False)
            self.B1_TMI.setEnabled(False)


        sender = self.sender()
        t = sender.text()
        if self.currentIndex() == 2:
            if t == '1 поверхность':
                self.s1.setText('1 ' + 'Информация о начале обработки')
                self.s2.setText('2 ' + 'Мощность массива MTV (*)')
                self.s3.setText('3 ' + 'Мощность массива MTG (*)')
                self.s4.setText('4 ' + 'Мощность массива MC (*)')
                self.s5.setText('5 ' + 'Мощность массива ТМ4 (!)')
                self.s12.setText('12 Максимальный квалитет точности размеров, который необходимо достигнуть на первых операциях технологического процесса (!)')
                self.s13.setText('13 ' + 'Указание о необходимости корректировки массива ТМ7 и печати маршрутной карты')
                self.s14.setText('14 ' + 'Указание о введении массива ТМ4')
                self.s15.setText('15 ' + 'Указание о введении массива ТМ10')
                self.s18.setText('18 ' + 'Указание о типе станка, применяемого для фрезерных операций')
                self.s19.setText('19 ' + 'Указание о типе станка, применяемого для сверлильных операций')
                self.s21.setText('21 ' + 'Указание о разработке технологического процесса изготовления деталей')
                self.s28.setText('28 ' + 'Код заготовки')

            elif t == '2 поверхность':
                self.s1.setText('1 ' + 'Код технологического процесса по его организации')
                self.s2.setText('2 ' + 'Код вида технологического процесса по методу выполнения по ГОСТ 3.1201-74')
                self.s3.setText('3 ' + self.file_TM2[2][0])
                self.s4.setText('4 ' + self.file_TM2[3][0])
                self.s5.setText('5 ' + 'Мощность массива ТМИ')
                self.s12.setText('12 ' + self.file_TM2[11][0])
                self.s13.setText('13 ' + self.file_TM2[12][0])
                self.s14.setText('14 ' + self.file_TM2[13][0])
                self.s15.setText('15 ' + self.file_TM2[14][0])
                self.s18.setText('18 ' + self.file_TM2[17][0])
                self.s19.setText('19 ' + self.file_TM2[18][0])
                self.s21.setText('21 ' + self.file_TM2[20][0])
                self.s28.setText('28 ' + 'Вид литья')

            else:
                self.s1.setText('1 ' + self.file_TM2[0][0])
                self.s2.setText('2 ' + self.file_TM2[1][0])
                self.s3.setText('3 ' + self.file_TM2[2][0])
                self.s4.setText('4 ' + self.file_TM2[3][0])
                self.s5.setText('5 ' + self.file_TM2[4][0])
                self.s12.setText('12 ' + self.file_TM2[11][0])
                self.s13.setText('13 ' + self.file_TM2[12][0])
                self.s14.setText('14 ' + self.file_TM2[13][0])
                self.s15.setText('15 ' + self.file_TM2[14][0])
                self.s18.setText('18 ' + self.file_TM2[17][0])
                self.s19.setText('19 ' + self.file_TM2[18][0])
                self.s21.setText('21 ' + self.file_TM2[20][0])
                self.s28.setText('28 ' + self.file_TM2[27][0])

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
        elif self.currentIndex() == 3 or self.currentIndex() == 4 or self.currentIndex() == 6:
            if  t == '1-й элемент':
                self.enterTm2(0)
                print('Запиь первого элемента произведена, текущая вкладка: ' + str(self.currentIndex()))
            elif  t == '2-й элемент':
                self.enterTm2(1)
            elif  t == '3-й элемент':
                self.enterTm2(2)
            elif  t == '4-й элемент':
                self.enterTm2(3)
            elif  t == '5-й элемент':
                self.enterTm2(4)
            elif  t == '6-й элемент':
                self.enterTm2(5)
            elif  t == '7-й элемент':
                self.enterTm2(6)
            elif  t == '8-й элемент':
                self.enterTm2(7)
            elif  t == '9-й элемент':
                self.enterTm2(8)
            elif  t == '10-й элемент':
                self.enterTm2(9)
            elif  t == '11-й элемент':
                self.enterTm2(10)
            elif  t == '12-й элемент':
                self.enterTm2(11)
            elif  t == '13-й элемент':
                self.enterTm2(12)
            elif  t == '14-й элемент':
                self.enterTm2(13)
            elif  t == '15-й элемент':
                self.enterTm2(14)

        elif self.currentIndex() == 5:
            if t == '1-й элемент':
                self.enterTm2(0)
                print('Запиь первого элемента произведена, текущая вкладка: ' + str(self.currentIndex()))
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
            elif t == '16-й элемент':
                self.enterTm2(15)
            elif t == '17-й элемент':
                self.enterTm2(16)
            elif t == '18-й элемент':
                self.enterTm2(17)
            elif t == '19-й элемент': 
                self.enterTm2(18)
            elif t == '20-й элемент':
                self.enterTm2(19)
            elif t == '21-й элемент':
                self.enterTm2(20)
            elif t == '22-й элемент':
                self.enterTm2(21)
            elif t == '23-й элемент':
                self.enterTm2(22)
            elif t == '24-й элемент':
                self.enterTm2(23)
            elif t == '25-й элемент':
                self.enterTm2(24)
            elif t == '26-й элемент':
                self.enterTm2(25)
            elif t == '27-й элемент':
                self.enterTm2(26)
            elif t == '28-й элемент':
                self.enterTm2(27)
            elif t == '29-й элемент':
                self.enterTm2(28)
            elif t == '30-й элемент':
                self.enterTm2(29)




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())