import sys
from PyQt5.QtWidgets import QTabWidget, QApplication, QMainWindow, QGridLayout, QWidget, QVBoxLayout, QLabel, QInputDialog, QMessageBox,\
    QTableWidget, QTableWidgetItem, QPushButton, QFormLayout, QLineEdit, QHBoxLayout, QAction, QFileDialog, \
    QLayout, QScroller, QScrollArea, QComboBox
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap
import json

class combodemo(QWidget):
    def __init__(self, parent=None):
        super(combodemo, self).__init__(parent)

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.cb.addItem("C")
        self.cb.addItem("C++")
        self.cb.addItems(["Java", "C#", "Python"])
        self.cb.currentIndexChanged.connect(self.selectionchange)

        layout.addWidget(self.cb)
        self.setLayout(layout)
        self.setWindowTitle("combo box demo")

    def selectionchange(self, i):
        print(self.cb.count())
        print ("Items in the list are :")

        for count in range(self.cb.count()):
            print (self.cb.itemText(count))

        print ("Current index", i, "selection changed ", self.cb.currentText())
        print(self.cb.setCurrentIndex(self.cb.findText('Java')))
        print ("Current index", i, "selection changed ", self.cb.currentText())
        a = '01.23'
        print(a[3:])


def main():
    app = QApplication(sys.argv)
    ex = combodemo()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()