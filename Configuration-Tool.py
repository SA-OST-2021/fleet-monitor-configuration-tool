###############################################################################
# file    Configuration-Tool.py
###############################################################################
# brief   Graphical User Interface to change the FMS-Frame Filter Configuration
###############################################################################
# author  Florian Baumgartner
# version 1.0
# date    2021-12-15
###############################################################################
# MIT License
#
# Copyright (c) 2021 Institute for Networked Solutions OST
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
###############################################################################

import sys
import json
from pathlib import Path
from functools import partial
from FileHandler import FileHandler
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QKeySequence, QFont, QIntValidator
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
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
        self.fileData = {}
        
        try:
            with open("sys.tmp") as f:
                self.fileName = json.load(f)["file"]
                if(Path(self.fileName).is_file()):
                    self.fileData = self.handler.loadFile(self, self.fileName)
                else:
                    self.fileName = None
        except:
            pass
        
        self.initUI()
        self.setWindowState(self.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
        self.activateWindow()

    def initUI(self):
        self.resize(QSize(900, 900))
        self.setMinimumSize(QSize(200, 200))
        self.setWindowTitle("Fleet-Monitor Configuator") 
        self.setAcceptDrops(True)
        
        menu = self.menuBar().addMenu('File')
        translate = QtCore.QCoreApplication.translate
        
        actionOpen = QtWidgets.QAction(self)
        actionOpen.setText(translate("MainWindow", "Open"))
        actionOpen.setShortcut(translate("MainWindow", "Ctrl+O"))
        actionOpen.triggered.connect(self.openFile)
        menu.addAction(actionOpen)
        
        actionSave = QtWidgets.QAction(self)
        actionSave.setText(translate("MainWindow", "Save"))
        actionSave.setShortcut(translate("MainWindow", "Ctrl+S"))
        actionSave.triggered.connect(self.saveFile)
        menu.addAction(actionSave)
        
        actionSaveAs = QtWidgets.QAction(self)
        actionSaveAs.setText(translate("MainWindow", "Save as"))
        actionSaveAs.setShortcut(translate("MainWindow", "Ctrl+Shift+S"))
        actionSaveAs.triggered.connect(self.saveFileAs)
        menu.addAction(actionSaveAs)
        
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
        box = QGridLayout()
        box.setAlignment(QtCore.Qt.AlignTop)
        groupbox.setLayout(box)
        
        self.unknownFrames = QtWidgets.QCheckBox("Send Unknown Frames")
        self.unknownFrames.setChecked(self.fileData.get("unknownframes", False))
        self.unknownFrames.toggled.connect(lambda x: self.fileData.update(unknownframes = self.unknownFrames.isChecked()))
        box.addWidget(self.unknownFrames, 0, 0)
        
        self.frameName = QtWidgets.QCheckBox("Send Frame Name")
        self.frameName.setChecked(self.fileData.get("framename", False))
        self.frameName.toggled.connect(lambda x: self.fileData.update(framename = self.frameName.isChecked()))
        box.addWidget(self.frameName, 1, 0)

        return groupbox
    
    def createFrameSettings(self):
        groupbox = QGroupBox('Frame Settings')
        box = QVBoxLayout()
        groupbox.setLayout(box)
        
        self.filterBoxTypes = {"nofilter": "No Filter", "change": "On Change", "interval": "Max. Interval"}
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["Active", "PGN", "Name", "Filter", "Interval [ms]"])
        self.tableWidget.verticalHeader().hide()
        
        header = self.tableWidget.horizontalHeader()  
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
        header.sectionClicked.connect(self.onSectionClicked)

        self.tableWidget.show()        
        self.updateFrameSettings()    
        box.addWidget(self.tableWidget)
        return groupbox
 
    
    def updateFrameSettings(self):
        if(self.fileName):
            self.setWindowTitle("Fleet-Monitor Configuator: " + Path(self.fileName).name)
            self.tableWidget.setRowCount(len(self.fileData["frames"]))
            self.active = []
            self.filters = []
            self.intervals = []
            
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
                self.active[-1].toggled.connect(partial(self.activeCallback, row))  
                self.tableWidget.setCellWidget(row, 0, checkBoxWidget)
                self.tableWidget.setItem(row, 0, cell)
                
                cell = QtWidgets.QTableWidgetItem(f"{i['pgn']}")
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                cell.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row, 1, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
                
                cell = QtWidgets.QTableWidgetItem(f"{i['name']}")
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.tableWidget.setItem(row, 2, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)
                
                cell = QtWidgets.QTableWidgetItem()
                cell.setFlags(QtCore.Qt.ItemIsEnabled)
                self.filters.append(QtWidgets.QComboBox())
                
                self.filters[-1].addItems(list(self.filterBoxTypes.values()))
                self.filters[-1].setCurrentText(self.filterBoxTypes[i["filter"]])
                self.filters[-1].currentIndexChanged.connect(partial(self.filterCallback, row))  
                self.tableWidget.setCellWidget(row, 3, self.filters[-1])
                self.tableWidget.setItem(row, 3, cell)
                
                if(i["filter"] == "interval"):
                    if "time" not in i:
                        self.fileData["frames"][row]["time"] = "0"
                else:
                    self.fileData["frames"][row].pop("time", None)  # Remove Key if not used
                value = self.fileData["frames"][row].get("time", "")
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
                self.intervals[-1].setStyleSheet("* {background-color: rgba(0,0,0,0);}")
                self.intervals[-1].textChanged.connect(partial(self.intervalCallback, row))
                self.intervals[-1].returnPressed.connect(self.updateFrameSettings)
                self.intervals[-1].setValidator(QIntValidator())
                self.tableWidget.setCellWidget(row, 4, self.intervals[-1])
                self.tableWidget.setItem(row, 4, cell)
                self.tableWidget.viewport().setFocusPolicy(QtCore.Qt.NoFocus)


    def activeCallback(self, index):
        self.fileData["frames"][index]["active"] = self.active[index].isChecked()

    def filterCallback(self, index):
        table = {self.filterBoxTypes[k]:k for k in self.filterBoxTypes}
        self.fileData["frames"][index]["filter"] = table[self.filters[index].currentText()]
        self.updateFrameSettings()

    def intervalCallback(self, index):
        try:
            value = int(self.intervals[index].text())
        except ValueError:
            value = 0
        self.fileData["frames"][index]["time"] = str(abs(value))
        
    def onSectionClicked(self, index):
        if(index == 0):
            state = self.active[0].isChecked()
            for i in self.active:
                i.setChecked(not state)

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
        with open ("sys.tmp", "w") as f:
            json.dump({"file": self.fileName}, f)

    def openFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open configuration file", "", "JSON Files (*.json);;All Files (*)")
        if self.fileName:
            self.fileData = self.handler.loadFile(self, self.fileName)
            self.statusBar().showMessage("Open File: " + self.fileName)
            self.updateFrameSettings()
            with open ("sys.tmp", "w") as f:
                json.dump({"file": self.fileName}, f)
 
    def saveFile(self):
        if self.fileName:
            self.handler.saveFile(self, self.fileName, self.fileData)
            self.statusBar().showMessage("Save File: " + self.fileName)
            self.updateFrameSettings()
        
    def saveFileAs(self):
        self.fileName, _ = QFileDialog.getSaveFileName(self, "Save configuration file", self.fileName, "JSON Files (*.json);;All Files (*)")
        if self.fileName:
            self.handler.saveFile(self, self.fileName, self.fileData)
            self.statusBar().showMessage("Save File as: " + self.fileName)
            self.updateFrameSettings()
            with open ("sys.tmp", "w") as f:
                json.dump({"file": self.fileName}, f)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    app.lastWindowClosed.connect(QtWidgets.QApplication.quit)
    # app.setStyleSheet(qdarktheme.load_stylesheet())

    window = App()
    window.show()
    sys.exit(app.exec_())
