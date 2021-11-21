# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:49:13 2021

@author: flori
"""

import sys
# import qdarktheme
from FileHandler import FileHandler
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QKeySequence, QFont
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


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.handler = FileHandler
        self.fileName = None
        self.fileData = None
        
        self.initUI()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        # self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.activateWindow()

    def initUI(self):
        self.resize(QSize(650, 900))
        self.setMinimumSize(QSize(200, 200))
        self.setWindowTitle("Fleet-Monitor Configuator") 
        self.setAcceptDrops(True)
        
        # centralWidget = QWidget(self)          
        # self.setCentralWidget(centralWidget)   
 
        # gridLayout = QGridLayout(self)     
        # centralWidget.setLayout(gridLayout)  
 
        # title = QLabel("Fleet-Monitor Configuator", self) 
        # title.setAlignment(QtCore.Qt.AlignCenter)
        # gridLayout.addWidget(title, 0, 0)

        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.openFile)   
        action = menu.addAction('Save')
        action.triggered.connect(self.saveFile)
        action = menu.addAction('Save as')
        action.triggered.connect(self.saveFileAs)
        
        self.shortcut = QShortcut(QKeySequence("Ctrl+O"), self)
        self.shortcut.activated.connect(self.openFile)
        self.shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcut.activated.connect(self.saveFile)
        self.shortcut = QShortcut(QKeySequence("Ctrl+Shift+S"), self)
        self.shortcut.activated.connect(self.saveFileAs)
        
        self.statusbar = QStatusBar()
        self.statusbar.setSizeGripEnabled(False)
        self.setStatusBar(self.statusbar)
           
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.createGlobalSettings(), 2)
        self.mainLayout.addWidget(self.createFrameSettings(), 10)        

        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)


    def createGlobalSettings(self):
        groupbox = QGroupBox('Global Settings')

        box = QVBoxLayout()
        groupbox.setLayout(box)

        return groupbox
    
    def createFrameSettings(self):
        groupbox = QGroupBox('Frame Settings')
        box = QVBoxLayout()
        
        # scroll = QtWidgets.QScrollArea()
        # scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # scroll.setWidgetResizable(True)
        
        
        # widget = QtWidgets.QWidget()
        # scroll.setWidget(widget)
        
        # self.frameSettingsLayout = QtWidgets.QFormLayout()
        # self.frameSettingsLayout.setVerticalSpacing(10)
        # widget.setLayout(self.frameSettingsLayout)
        
        print("createFrameSettings")
        
        self.tableWidget = QtWidgets.QTableWidget()
        # self.tableWidget.setGeometry(QtCore.QRect(220, 100, 411, 392))
        self.tableWidget.setColumnCount(5)
        
        
        self.tableWidget.setHorizontalHeaderLabels(["Active", "PGN", "Name", "Filter", "Interval [ms]"])
        self.tableWidget.verticalHeader().hide()
        
        header = self.tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)

        self.tableWidget.show()
        
        self.active = []
        self.filters = []
        self.intervals = []

        
        self.updateFrameSettings()
             
        groupbox.setLayout(QVBoxLayout())
        groupbox.layout().addWidget(self.tableWidget)
        box.addWidget(groupbox)
        groupbox.setLayout(box)

        return groupbox
 
    
    def updateFrameSettings(self):
        if(self.fileName):
            self.tableWidget.setRowCount(len(self.fileData["frames"]))
            
            for row, i in enumerate(self.fileData["frames"]):
                cell = QtWidgets.QTableWidgetItem()
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.active.append(QtWidgets.QCheckBox())
                checkBoxWidget = QWidget()
                layoutCheckBox = QHBoxLayout(checkBoxWidget)
                layoutCheckBox.addWidget(self.active[-1])
                layoutCheckBox.setAlignment(QtCore.Qt.AlignCenter)
                layoutCheckBox.setContentsMargins(0,0,0,0)
                self.active[-1].setChecked(i["active"])
                self.tableWidget.setCellWidget(row, 0, checkBoxWidget)
                self.tableWidget.setItem(row, 0, cell)
                
                cell = QtWidgets.QTableWidgetItem(f"{i['pgn']}")
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 1, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
                
                cell = QtWidgets.QTableWidgetItem(f"{i['name']}")
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 2, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
                
                
                cell = QtWidgets.QTableWidgetItem()
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.filters.append(QtWidgets.QComboBox())
                filterBoxTypes = {"nofilter": "No Filter", "change": "On Change", "interval": "Max. Interval"}
                self.filters[-1].addItems(list(filterBoxTypes.values()))
                self.filters[-1].setCurrentText(filterBoxTypes[i["filter"]])
                self.tableWidget.setCellWidget(row, 3, self.filters[-1])
                self.tableWidget.setItem(row, 3, cell)
                
                
                if(i["filter"] == "interval"):
                    if "time" not in i:
                        self.fileData["frames"][row]["time"] = "1000"
                else:
                    self.fileData.pop("time", None)  # Remove Key if not used
                value = self.fileData["frames"][row].get("time", "")
                # cell.setTextAlignment(QtCore.Qt.AlignCenter)
                cell = QtWidgets.QTableWidgetItem()
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.intervals.append(QtWidgets.QLineEdit(value))
                self.intervals[-1].setStyleSheet("QLineEdit { border: none }")
                self.intervals[-1].setAlignment(QtCore.Qt.AlignCenter)
                self.intervals[-1].setFont(self.tableWidget.font())
                f = self.intervals[-1].font()
                f.setPointSize(self.tableWidget.font().pointSize())
                self.intervals[-1].setFont(f)
                self.intervals[-1].setEnabled(i["filter"] == "interval")
                self.tableWidget.setCellWidget(row, 4, self.intervals[-1])
                self.tableWidget.setItem(row, 4, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
        
        
        
        
        # if(self.fileName):
        #     # scroll.setEnabled(True)
        #     print("show data")
        #     for n, i in enumerate(self.fileData["frames"]):
    
        #         hbox = QtWidgets.QWidget()
        #         hBoxLayout = QFormLayout()
        #         hBoxLayout.setContentsMargins(0,0,0,0)
        #         hbox.setLayout(hBoxLayout)
        #         # hBoxLayout.addWidget(QtWidgets.QLabel(f'PGN: <b>{i["pgn"]}<b>'))
        #         # hBoxLayout.addWidget(QtWidgets.QLabel(f'Name: <b>{i["name"]}</b>'))
        #         hBoxLayout.addRow(QtWidgets.QLabel(f'PGN: <b>{i["pgn"]}<b>'),
        #                              QtWidgets.QLabel(f'Name: <b>{i["name"]}</b>'))
        #         self.frameSettingsLayout.addRow(hbox)
                
        #         hbox = QtWidgets.QWidget()
        #         hBoxLayout = QHBoxLayout()
        #         hBoxLayout.setContentsMargins(0,0,0,0)
        #         hbox.setLayout(hBoxLayout)
                
        #         filterBoxTypes = {"never": "Never", "change": "On Change", "interval": "Max. Interval"}
        #         filterBox = QComboBox()
        #         filterBox.addItems(list(filterBoxTypes.values()))
        #         filterBox.setCurrentText(filterBoxTypes[i["filter"]])

        #         if (i["filter"] == "interval"):
        #             if "time" not in i:
        #                 self.fileData["frames"][n]["time"] = ""
        #             interval = QLineEdit(i["time"])
        #         else:
        #             interval = QLineEdit("")
        #             interval.setEnabled(False)

        #         hBoxLayout.addWidget(QtWidgets.QLabel('Filter:'))
        #         hBoxLayout.addWidget(filterBox)
        #         hBoxLayout.addWidget(QtWidgets.QLabel('Interval:'))
        #         hBoxLayout.addWidget(interval)
        #         hBoxLayout.addWidget(QtWidgets.QLabel('ms'))
        #         self.frameSettingsLayout.addRow(hbox)
                
        #         self.frameSettingsLayout.addRow(QtWidgets.QLabel(''))
        # else:
        #     # scroll.setEnabled(False)
        #     pass
        #     # scroll.delete()
            
        #     self.tableWidget = QtWidgets.QTableWidget()
        #     self.tableWidget.setGeometry(QtCore.QRect(220, 100, 411, 392))
        #     self.tableWidget.setColumnCount(2)
        #     self.tableWidget.setRowCount(5)
        #     self.tableWidget.show()

        #     attr = ['one', 'two', 'three', 'four', 'five']
        #     i = 0
        #     for j in attr:
        #         self.tableWidget.setItem(i, 0, QtWidgets.QTableWidgetItem(j))
        #         comboBox = QtWidgets.QComboBox()
        #         self.tableWidget.setCellWidget(i, 1, comboBox)
        #         i += 1


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.fileName = event.mimeData().urls()[0].toLocalFile()
        self.fileData = self.handler.loadFile(self, self.fileName)
        self.statusBar().showMessage("Open File: " + self.fileName)
        self.updateFrameSettings()

    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open configuration file", "", "JSON Files (*.json);;All Files (*)")
        if self.fileName:
            self.fileData = self.handler.loadFile(self, self.fileName)
            self.statusBar().showMessage("Open File: " + self.fileName)
            self.updateFrameSettings()
 
    def saveFile(self):
        if self.fileName:
            self.handler.saveFile(self, self.fileName, self.fileData)
            self.statusBar().showMessage("Save File: " + self.fileName)
        
    def saveFileAs(self):
        self.fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration file", self.fileName, "JSON Files (*.json);;All Files (*)")
        if self.fileName:
            self.handler.saveFile(self, self.fileName, self.fileData)
            self.statusBar().showMessage("Save File as: " + self.fileName)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(QtWidgets.QApplication.quit)
    # app.setStyleSheet(qdarktheme.load_stylesheet())

    window = App()
    window.show()

    sys.exit(app.exec_())
