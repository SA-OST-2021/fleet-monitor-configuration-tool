# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 11:49:13 2021

@author: flori
"""

import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QSize  


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.activateWindow()

    def initUI(self):
        self.setMinimumSize(QSize(750, 1000))    
        self.setWindowTitle("Hello world") 
        
        centralWidget = QWidget(self)          
        self.setCentralWidget(centralWidget)   
 
        gridLayout = QGridLayout(self)     
        centralWidget.setLayout(gridLayout)  
 
        title = QLabel("Fleet-Monitor Configuator", self) 
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)
        
        menu = self.menuBar().addMenu('File')
        action = menu.addAction('Open')
        action.triggered.connect(self.openFile)   
        action = menu.addAction('Save')
        action.triggered.connect(self.saveFile)
        action = menu.addAction('Save as')
        action.triggered.connect(self.saveFileAs)
        
        
    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open configuration file", "", "JSON Files (*.json);;All Files (*)")
        if fileName:
            print(fileName)

        
    def saveFile(self):
        print("Save File...")
        
    def saveFileAs(self):
        prevName = "test.json"
        fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration file", prevName, "JSON Files (*.json);;All Files (*)")
        if fileName:
            print(fileName)

 
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(QtWidgets.QApplication.quit)
    app.setStyle('Windows')

    window = App()
    window.show()

    sys.exit(app.exec_())
