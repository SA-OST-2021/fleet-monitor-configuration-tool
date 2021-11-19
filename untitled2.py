import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QPushButton,
    QShortcut,
    QGroupBox,
    QStatusBar,
    QScrollArea,
    QComboBox,
    QLineEdit,
    QSpacerItem,
    QSizePolicy,
    QFormLayout,
)

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50,50,500,500)
        self.setWindowTitle('PyQt Tuts')
        self.table()


    def table(self):

        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setGeometry(QtCore.QRect(220, 100, 411, 392))
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(20)
        
        self.tableWidget.setHorizontalHeaderLabels(["Active", "PGN", "Name", "Filter", "Interval [ms]"])
        self.tableWidget.verticalHeader().hide()
        
        # self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.tableWidget.setFocusPolicy(QtCore.NoFocus)

        self.tableWidget.show()
        
        
        
        self.active = []
        self.filters = []
        for row in range(self.tableWidget.rowCount()):
            
            
            cell = QtWidgets.QTableWidgetItem()
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            self.active.append(QtWidgets.QCheckBox())
            w = - self.active[-1].sizeHint().width() // 2
            w = 20
            self.active[-1].setStyleSheet(f"margin:99%;")
            self.tableWidget.setCellWidget(row, 0, self.active[-1])
            self.tableWidget.setItem(row, 0, cell)
            
            cell = QtWidgets.QTableWidgetItem(f"{row}")
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 1, cell)
            self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
            
            cell = QtWidgets.QTableWidgetItem(f"name")
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(row, 2, cell)
            self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
            
            cell = QtWidgets.QTableWidgetItem()
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            self.filters.append(QtWidgets.QComboBox())
            self.tableWidget.setCellWidget(row, 3, self.filters[-1])
            self.tableWidget.setItem(row, 3, cell)
            
            cell = QtWidgets.QTableWidgetItem(f"0")
            cell.setTextAlignment(QtCore.Qt.AlignCenter)
            # cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 4, cell)
            self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
            
            
            
        



def run():
    app = QtWidgets.QApplication(sys.argv)      
    w = Window()
    sys.exit(app.exec_())      

run()