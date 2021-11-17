# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:49:13 2021

@author: flori
"""

import sys
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
           
        layout = QVBoxLayout()
        layout.addWidget(self.createGlobalSettings(), 2)
        layout.addWidget(self.createFrameSettings(), 10)        

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


    def createGlobalSettings(self):
        groupbox = QGroupBox('Global Settings')

        box = QVBoxLayout()
        groupbox.setLayout(box)

        return groupbox
    
    def createFrameSettings(self):
        groupbox = QGroupBox('Frame Settings')
        box = QVBoxLayout()
        

        
        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        
        # labellist = []
        # combolist = []
        # for i in range(10):
        #     labellist.append(QtWidgets.QLabel('mylabel'))
        #     combolist.append(QtWidgets.QComboBox())
        #     # myform.addRow(labellist[i],combolist[i])
        #     scroll.setWidget(labellist[i],combolist[i])
        
        # labellist = []
        # for i in range(10):
        #     labellist.append(QtWidgets.QLabel('mylabel'))
        #     scroll.setWidget(labellist[i])
        
        widget = QtWidgets.QWidget()
        scroll.setWidget(widget)
        
        layout = QtWidgets.QFormLayout(self)
        layout.setVerticalSpacing(20)
        widget.setLayout(layout)
        
        for i in range(10):
            vbox = QtWidgets.QWidget()
            vBoxLayout = QVBoxLayout()
            vbox.setLayout(vBoxLayout)
            
            # boxLayout.addWidget(QtWidgets.QLabel('Name:'))
            
            hbox = QtWidgets.QWidget()
            hBoxLayout = QHBoxLayout()
            hbox.setLayout(hBoxLayout)
            hBoxLayout.addWidget(QtWidgets.QLabel(f'Name: <b>{"Fuel Consumption: LFC"}</b>'))
            hBoxLayout.addWidget(QtWidgets.QLabel(f'PGN: <b>{"FEE9"}<b>'))
            vBoxLayout.addWidget(hbox)
            
            hbox = QtWidgets.QWidget()
            hBoxLayout = QHBoxLayout()
            hbox.setLayout(hBoxLayout)
            hBoxLayout.addWidget(QtWidgets.QLabel(f'Filter: <b>{"Fuel Consumption: LFC"}</b>'))
            hBoxLayout.addWidget(QtWidgets.QLabel(f'Interval: <b>{"FEE9"}<b>'))
            vBoxLayout.addWidget(hbox)
            
            # filterBox = QComboBox()
            # interval = QLineEdit("100")
            # boxLayout.addRow(QtWidgets.QLabel('Filter:'), filterBox,
            #                  QtWidgets.QLabel('Interval:'), QLineEdit,
            #                  QtWidgets.QLabel('ms'))
            
            layout.addWidget(vbox)
        
        
        groupbox.setLayout(QVBoxLayout())
        groupbox.layout().addWidget(scroll)
        box.addWidget(groupbox)
        groupbox.setLayout(box)

        return groupbox

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        self.fileName = event.mimeData().urls()[0].toLocalFile()
        self.fileData = self.handler.loadFile(self, self.fileName)
        self.statusBar().showMessage("Open File: " + self.fileName)

    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open configuration file", "", "JSON Files (*.json);;All Files (*)")
        if self.fileName:
            self.fileData = self.handler.loadFile(self, self.fileName)
            self.statusBar().showMessage("Open File: " + self.fileName)
 
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
    app.setStyle('Windows')

    window = App()
    window.show()

    sys.exit(app.exec_())
