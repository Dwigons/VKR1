from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout, QAction, QTableWidget
import sys


# этот класс позволяет легко использовать
# главное меню и другие бонусы QMainWindow
class MyMainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.form_widget = FormWidget(self)
        #self.table_widget = TableWidget(self)
        # Ниже мы паркуем класс виджета  производного от QWidget
        # на главном окне ( на  QMainWindow)
        layout3 = QHBoxLayout()
        bar = self.menuBar()
        file = bar.addMenu("FFFFFile")
        file.addAction("XAO")
        self.setCentralWidget(self.form_widget)  # припарковали =)
        #self.setCentralWidget(self.table_widget)  # припарковали =)

class TableWidget(QTableWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)

# а этот  - виджет - использовать слои и добавлять
# кнопки и иные эжлементы управления
class FormWidget(QTabWidget):

    def __init__(self, parent):
        super(FormWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout2 = QVBoxLayout(self)
        self.layout3 = QVBoxLayout(self)


        # self.tab1 = QWidget()
        # self.addTab(self.tab1,"sda")
        # self.table1 = QTableWidget()
        # self.table1.setColumnCount(3)
        # self.table1.setRowCount(3)
        # self.layout.addWidget(self.table1)
        # self.button1 = QPushButton("Button 1")
        # self.layout.addWidget(self.button1)
        # self.tab1.setLayout(self.layout)
        # #self.layout.addWidget(self.tab1)
        #
        #
        # self.tab2 = QWidget()
        # self.addTab(self.tab2, "sda1")
        # QTabWidget.tab3 = QWidget()
        # self.button2 = QPushButton("Button 2")
        # self.layout2.addWidget(self.button2)
        # self.addTab(QTabWidget.tab3, "aaa")
        # # self.layout2.addWidget(self.tab3)
        # # self.layout3.addWidget(self.tab3)
        # self.tab2.setLayout(self.layout2)
        # QTabWidget.tab3.setLayout(self.layout3)
        # self.layout2.setLayout(self.layout3)
        # #self.layout2.addWidget(self.tab1)
        print(self.arr(2))
    def arr(self, i):
        i+=1
        return(i)
app = QApplication([])
foo = MyMainWindow()
foo.show()
sys.exit(app.exec_())