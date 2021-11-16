# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:49:13 2021

@author: flori
"""

import sys
from FileHandler import FileHandler
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QFileDialog,
    QPushButton,
    QShortcut,
    QGroupBox,
    QStatusBar,
    QScrollArea
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

        vbox = QVBoxLayout()
        groupbox.setLayout(vbox)

        return groupbox
    
    def createFrameSettings(self):
        groupbox = QGroupBox('Frame Settings')
        vbox = QVBoxLayout()
        

        
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        
        # labellist = []
        # combolist = []
        # for i in range(10):
        #     labellist.append(QtWidgets.QLabel('mylabel'))
        #     combolist.append(QtWidgets.QComboBox())
        #     # myform.addRow(labellist[i],combolist[i])
        #     scroll.setWidget(labellist[i],combolist[i])
        
        labellist = []
        for i in range(10):
            labellist.append(QtWidgets.QLabel('mylabel'))
            scroll.setWidget(labellist[i])
        
        
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(scroll)
        
        groupbox.setLayout(QVBoxLayout())
        groupbox.layout().addWidget(scroll)
        vbox.addWidget(groupbox)
        groupbox.setLayout(vbox)

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
