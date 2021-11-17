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
        
        scroll = QtWidgets.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        
        
        widget = QtWidgets.QWidget()
        scroll.setWidget(widget)
        
        self.frameSettingsLayout = QtWidgets.QFormLayout()
        self.frameSettingsLayout.setVerticalSpacing(10)
        widget.setLayout(self.frameSettingsLayout)
        
        print("createFrameSettings")
        
        self.updateFrameSettings()
             
        groupbox.setLayout(QVBoxLayout())
        groupbox.layout().addWidget(scroll)
        box.addWidget(groupbox)
        groupbox.setLayout(box)

        return groupbox
 
    
    def updateFrameSettings(self):
        if(self.fileName):
            # scroll.setEnabled(True)
            print("show data")
            for n, i in enumerate(self.fileData["frames"]):
    
                hbox = QtWidgets.QWidget()
                hBoxLayout = QFormLayout()
                hBoxLayout.setContentsMargins(0,0,0,0)
                hbox.setLayout(hBoxLayout)
                # hBoxLayout.addWidget(QtWidgets.QLabel(f'PGN: <b>{i["pgn"]}<b>'))
                # hBoxLayout.addWidget(QtWidgets.QLabel(f'Name: <b>{i["name"]}</b>'))
                hBoxLayout.addRow(QtWidgets.QLabel(f'PGN: <b>{i["pgn"]}<b>'),
                                     QtWidgets.QLabel(f'Name: <b>{i["name"]}</b>'))
                self.frameSettingsLayout.addRow(hbox)
                
                hbox = QtWidgets.QWidget()
                hBoxLayout = QHBoxLayout()
                hBoxLayout.setContentsMargins(0,0,0,0)
                hbox.setLayout(hBoxLayout)
                
                filterBoxTypes = {"never": "Never", "change": "On Change", "interval": "Max. Interval"}
                filterBox = QComboBox()
                filterBox.addItems(list(filterBoxTypes.values()))
                filterBox.setCurrentText(filterBoxTypes[i["filter"]])

                if (i["filter"] == "interval"):
                    if "time" not in i:
                        self.fileData["frames"][n]["time"] = ""
                    interval = QLineEdit(i["time"])
                else:
                    interval = QLineEdit("")
                    interval.setEnabled(False)

                hBoxLayout.addWidget(QtWidgets.QLabel('Filter:'))
                hBoxLayout.addWidget(filterBox)
                hBoxLayout.addWidget(QtWidgets.QLabel('Interval:'))
                hBoxLayout.addWidget(interval)
                hBoxLayout.addWidget(QtWidgets.QLabel('ms'))
                self.frameSettingsLayout.addRow(hbox)
                
                self.frameSettingsLayout.addRow(QtWidgets.QLabel(''))
        else:
            # scroll.setEnabled(False)
            pass
            # scroll.delete()


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
    app.setStyle('Windows')

    window = App()
    window.show()

    sys.exit(app.exec_())
