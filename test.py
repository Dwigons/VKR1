# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QPushButton, QTabWidget, QHBoxLayout, QAction, QTableWidget, QFormLayout, QLabel, QLineEdit
# import sys
#
#
# # этот класс позволяет легко использовать
# # главное меню и другие бонусы QMainWindow
# class MyMainWindow(QMainWindow):
#
#     def __init__(self, parent=None):
#         super(MyMainWindow, self).__init__(parent)
#         self.form_widget = FormWidget(self)
#         #self.table_widget = TableWidget(self)
#         # Ниже мы паркуем класс виджета  производного от QWidget
#         # на главном окне ( на  QMainWindow)
#         layout3 = QHBoxLayout()
#         bar = self.menuBar()
#         file = bar.addMenu("FFFFFile")
#         file.addAction("XAO")
#         l = QFormLayout()
#         l.addRow(QLabel('aaa'), QLineEdit())
#         # self.form_widget.layout.addWiget(l)
#         self.setCentralWidget(self.form_widget)  # припарковали =)
#         #self.setCentralWidget(self.table_widget)  # припарковали =)
#
# class TableWidget(QTableWidget):
#
#     def __init__(self, parent):
#         super(FormWidget, self).__init__(parent)
#
# # а этот  - виджет - использовать слои и добавлять
# # кнопки и иные эжлементы управления
# class FormWidget(QTabWidget):
#
#     def __init__(self, parent):
#         super(FormWidget, self).__init__(parent)
#         self.layout = QVBoxLayout(self)
#         self.layout2 = QVBoxLayout(self)
#         self.layout3 = QVBoxLayout(self)
#
#
#         self.tab1 = QWidget()
#         self.addTab(self.tab1,"sda")
#         self.table1 = QTableWidget()
#         self.table1.setColumnCount(3)
#         self.table1.setRowCount(3)
#         self.layout.addWidget(self.table1)
#
#         self.button1 = QPushButton("Button 1")
#         self.layout.addWidget(self.button1)
#         self.tab1.setLayout(self.layout)
#         #self.layout.addWidget(self.tab1)
#
#
#         self.tab2 = QWidget()
#         self.addTab(self.tab2, "sda1")
#         QTabWidget.tab3 = QWidget()
#         self.button2 = QPushButton("Button 2")
#         self.layout2.addWidget(self.button2)
#         self.addTab(QTabWidget.tab3, "aaa")
#         # self.layout2.addWidget(self.tab3)
#         # self.layout3.addWidget(self.tab3)
#         self.tab2.setLayout(self.layout2)
#         QTabWidget.tab3.setLayout(self.layout3)
#         # self.layout2.setLayout(self.layout3)
#         #self.layout2.addWidget(self.tab1)
#
#         # self.layout3.addWidget(self.l)
# if __name__ == "__main__":
#     app = QApplication([])
#     foo = MyMainWindow()
#     foo.show()
#     sys.exit(app.exec_())
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QFormLayout,
    QGridLayout,
    QLabel,
    QScrollArea,
    QScroller,
    QWidget,
    QLineEdit,
    QPushButton,
)


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        scroll_area = QScrollArea()
        layout = QGridLayout(self)
        layout.addWidget(scroll_area)

        scroll_widget = QWidget()
        scroll_layout = QFormLayout(scroll_widget)

        for i in range(30):
            scroll_layout.addRow(QLabel('Label #{}'.format(i)), QPushButton('{}'.format(i)))
            # scroll_layout.addRow(QLabel('Label #{}'.format(i)), QLineEdit()).clicked.connect(print(scroll_layout.addRow(QLabel('Label #{}'.format(i)), QLineEdit())))




        scroll_area.setWidget(scroll_widget)

        QScroller.grabGesture(
            scroll_area.viewport(), QScroller.LeftMouseButtonGesture
        )


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())