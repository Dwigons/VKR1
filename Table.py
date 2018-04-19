from PyQt5.QtWidgets import QLayout, QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction
from PyQt5.QtCore import QSize, Qt
import json


# Наследуемся от QMainWindow
class Tab_Widget(QMainWindow):
    # Переопределяем конструктор класса
    def __init__(self):
        # Обязательно нужно вызвать метод супер класса
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setMinimumSize(QSize(1100, 1000))  # Устанавливаем размеры
        self.setWindowTitle("Заполнение матриц")  # Устанавливаем заголовок окна
        central_widget = QMainWindow(self)  # Создаём центральный виджет
        QMainWindow.setCentralWidget(central_widget, self)  # Устанавливаем центральный виджет

        layout = QLayout()
        central_widget.setLayout(layout)

        self.tab = QTabWidget()
        BXlayout = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("File")
        file.addAction("New")

        save = QAction("Save", self)
        save.setShortcut("Ctrl+S")
        file.addAction(save)

        edit = file.addMenu("Edit")
        edit.addAction("copy")
        edit.addAction("paste")

        quit = QAction("Quit", self)
        file.addAction(quit)
        file.triggered[QAction].connect(self.processtrigger)
        self.setLayout(BXlayout)

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab.addTab(self.tab1, "TM1")
        self.tab.addTab(self.tab2, "TM2")
        self.tab.addTab(self.tab3, "TM3")

        self.tab1f()
        self.tab2f()
        self.tab3f()


    def processtrigger(self, q):
        print (q.text() + " is triggered")

    def tab1f(self):

        grid_layout = QGridLayout()  # Создаём QGridLayout
        central_widget.setLayout(grid_layout)  # Устанавливаем данное размещение в центральный виджет

        self.table = QTableWidget(self)  # Создаём таблицу
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

        file = json.load(open('dataset.json'))
        print(file)
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

        self.show()

    def tab2f(self):

        layout = QFormLayout()
        layout.addRow("Name", QLineEdit())
        layout.addRow("Address", QLineEdit())
        self.setTabText(1, "TM2")
        self.tab2.setLayout(layout)

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
            for col in range(cols):
                try:
                    tmp.append(self.table.item(row, col).text())
                except:
                    tmp.append('No data')
            data.append(tmp)
        for i in data: print(i)

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    tw = Tab_Widget()
    tw.show()
    sys.exit(app.exec())