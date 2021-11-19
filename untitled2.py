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

import PyQt5
from PyQt5 import QtCore, QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QWidget



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
        
        header = self.tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        
        # self.tableWidget.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        # self.tableWidget.setFocusPolicy(QtCore.NoFocus)

        self.tableWidget.show()
        
        
        
        self.active = []
        self.filters = []
        for row in range(self.tableWidget.rowCount()):
            
            
            cell = QtWidgets.QTableWidgetItem()
            cell.setFlags(QtCore.Qt.ItemIsEnabled)
            self.active.append(QtWidgets.QCheckBox())
            checkBoxWidget = QWidget()
            layoutCheckBox = QHBoxLayout(checkBoxWidget)
            layoutCheckBox.addWidget(self.active[-1])
            layoutCheckBox.setAlignment(QtCore.Qt.AlignCenter)
            layoutCheckBox.setContentsMargins(0,0,0,0)
            self.tableWidget.setCellWidget(row, 0, checkBoxWidget)
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
            filterBoxTypes = {"never": "Never", "change": "On Change", "interval": "Max. Interval"}
            self.filters[-1].addItems(list(filterBoxTypes.values()))
            self.tableWidget.setCellWidget(row, 3, self.filters[-1])
            self.tableWidget.setItem(row, 3, cell)
            
            cell = QtWidgets.QTableWidgetItem(f"0")
            cell.setTextAlignment(QtCore.Qt.AlignCenter)
            # cell.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
            self.tableWidget.setItem(row, 4, cell)
            self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
            
            
        


app = QtWidgets.QApplication(sys.argv)  
app.setQuitOnLastWindowClosed(False)
app.lastWindowClosed.connect(QtWidgets.QApplication.quit)    
w = Window()
sys.exit(app.exec_())      
