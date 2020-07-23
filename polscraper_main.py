# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polscraper_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

# I want to save the JSON so we can play with it later
# But for now it may be simple to just make one table in the sqlite DB
# that has the first column as the date, and the other columns as the
# scores, so we can plot these on a graph, both over time and as a bar chart
# perhaps
# Would also be worth collecting poster countries etc


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, QThread
from plyer import notification
from polscraper import polscraper

import main, polscraper_data

import time
import os, sys
import threading
step = 0

class ScannerThread(QThread):
    scanner_signal = pyqtSignal("PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject", "PyQt_PyObject")

    def __init__(self, pages_to_scan, interval):
        QThread.__init__(self)
        self.pages_to_scan = pages_to_scan
        self.interval = interval

    def run(self):

        if self.interval != "Once":
            pages, threads, replies, next_scan_time = polscraper.repeating(self.interval, self.pages_to_scan)
            next_scan_time = " Next scan scheduled for: " + str(next_scan_time.strftime('%H:%M:%S'))
            self.scanner_signal.emit(pages, threads, replies, next_scan_time)
            # self.scan_results_label.setText(f"Scan complete. {int(pages)} pages, {int(threads)} threads and {int(replies)} replies stored. Next scan scheduled for {str(next_scan_time.strftime('%H:%M:%S'))}")


        else:
            pages, threads, replies = polscraper.single(self.pages_to_scan)
            self.scanner_signal.emit(pages, threads, replies, "nothing because we're not doing another scan")
            # pages, threads, replies = polscraper.single(pages_to_scan)
            # self.scan_results_label.setText(f"Scan complete. {int(pages)} pages, {int(threads)} threads and {int(replies)} replies stored.")

        


class Ui_PolscraperWindow(object):

    def run_scanner(self):
        pages_to_scan = int(self.pagesList.currentText())
        interval = self.intervalList.currentText()

        self.scan_results_label.setText("Scanning...")

        print("starting scan thread")

        if interval != "Once":
            self.scanButton.setEnabled(False)
            # interval = int(interval[0])
            self.scan_results_label.setText(f"Scan will run on an interval of {interval}")
            self.scanButton.setEnabled(False)

            self.scan_thread = ScannerThread(pages_to_scan, interval)
            self.scan_thread.scanner_signal.connect(self.scan_complete)

            self.scan_thread.start()
            # pages, threads, replies, next_scan_time = polscraper.repeating(interval, pages_to_scan)

        else:
            self.scanButton.setEnabled(False)

            self.scan_thread = ScannerThread(pages_to_scan, interval)
            self.scan_thread.scanner_signal.connect(self.scan_complete)

            self.scan_thread.start()
            # pages, threads, replies = polscraper.single(pages_to_scan)



        

    def scan_complete(self, *args):
        print("scan complete, results:")
        print(args)

        scan_result = f"Scan complete. {int(args[0])} pages, {int(args[1])} threads and {int(args[2])} replies stored."

        if "scheduled" in args[3]:
            scan_result += str(args[3])

        self.scanButton.setEnabled(True)

        self.reportsList.clear()
        for file in os.listdir("polscraper/reports"):
                self.reportsList.addItem(file)

        self.scan_results_label.setText(scan_result)


    def setupUi(self, PolscraperWindow):
        PolscraperWindow.setObjectName("PolscraperWindow")
        PolscraperWindow.resize(436, 554)
        self.centralwidget = QtWidgets.QWidget(PolscraperWindow)
        self.centralwidget.setObjectName("centralwidget")


        
        # self.scan_thread = threading.Thread(name="scan_thread", target=self.run_scanner)

        self.scan_results_label = QtWidgets.QLabel(self.centralwidget)
        self.scan_results_label.setGeometry(QtCore.QRect(270, 270, 151, 61))
        self.scan_results_label.setText("Select how many pages to scan and how often (at what interval) and click SCAN to generate new report/s")
        self.scan_results_label.setWordWrap(True)
        self.scan_results_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scan_results_label.setObjectName("scan_results_label")

        self.pagesList = QtWidgets.QComboBox(self.centralwidget)
        self.pagesList.setGeometry(QtCore.QRect(290, 100, 111, 22))
        self.pagesList.setObjectName("pagesList")
        for i in range(1, 11):
            self.pagesList.addItem(str(i))

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(290, 230, 111, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(False)
        self.progressBar.setObjectName("progressBar")

        self.scanButton = QtWidgets.QPushButton(self.centralwidget)
        self.scanButton.setGeometry(QtCore.QRect(300, 190, 91, 31))
        self.scanButton.setObjectName("scanButton")
        self.scanButton.clicked.connect(self.run_scanner)
        # self.scanButton.clicked.connect(self.scan_thread.start())

        self.reportsList = QtWidgets.QListWidget(self.centralwidget)
        self.reportsList.setGeometry(QtCore.QRect(0, 50, 256, 461))
        self.reportsList.setObjectName("reportsList")
        try:
            for file in os.listdir("polscraper/reports"):
                self.reportsList.addItem(file)
                # if "analysis" in file:
                #     self.reportsList.addItem("-------------------------------------------------")
            self.reportsList.itemDoubleClicked.connect(self.open_file)
        except:
            self.reportsList.addItem("No reports found")
        



        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(50, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.intervals = [1, 2, 4, 6, 8, 12, 24, 36, 48]

        self.intervalList = QtWidgets.QComboBox(self.centralwidget)
        self.intervalList.setGeometry(QtCore.QRect(290, 150, 111, 22))
        self.intervalList.setObjectName("intervalList")
        self.intervalList.addItem("Once")
        for i in self.intervals:
            if i == 1:
                self.intervalList.addItem(str(i) + " hour")
            else:
                self.intervalList.addItem(str(i) + " hours")

        self.scanResultsBox = QtWidgets.QLabel(self.centralwidget)
        self.scanResultsBox.setGeometry(QtCore.QRect(290, 260, 111, 101))
        self.scanResultsBox.setText("")
        self.scanResultsBox.setObjectName("scanResultsBox")

        self.intervalLabel = QtWidgets.QLabel(self.centralwidget)
        self.intervalLabel.setGeometry(QtCore.QRect(290, 130, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.intervalLabel.setFont(font)
        self.intervalLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.intervalLabel.setObjectName("interval_label")

        self.pages_label = QtWidgets.QLabel(self.centralwidget)
        self.pages_label.setGeometry(QtCore.QRect(290, 80, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pages_label.setFont(font)
        self.pages_label.setAlignment(QtCore.Qt.AlignCenter)
        self.pages_label.setObjectName("pages_label")

        self.new_scan_title = QtWidgets.QLabel(self.centralwidget)
        self.new_scan_title.setGeometry(QtCore.QRect(260, 50, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.new_scan_title.setFont(font)
        self.new_scan_title.setAlignment(QtCore.Qt.AlignCenter)
        self.new_scan_title.setObjectName("new_scan_title")

        PolscraperWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(PolscraperWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 436, 21))
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        self.menuPolscraper = QtWidgets.QMenu(self.menubar)
        self.menuPolscraper.setObjectName("menuPolscraper")

        PolscraperWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(PolscraperWindow)
        self.statusbar.setObjectName("statusbar")

        PolscraperWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(PolscraperWindow)
        self.actionExit.setObjectName("actionExit")

        self.actionMainMenu = QtWidgets.QAction(PolscraperWindow)
        self.actionMainMenu.setObjectName("actionMainMenu")
        self.actionMainMenu.triggered.connect(self.toMainMenu)

        self.actionPolscraper = QtWidgets.QAction(PolscraperWindow)
        self.actionPolscraper.setObjectName("actionPolscraper")


        self.actionDataDisplay = QtWidgets.QAction(PolscraperWindow)
        self.actionDataDisplay.setObjectName("actionDataDisplay")
        self.actionDataDisplay.triggered.connect(self.toPolscraperData)

        self.actionSentiment = QtWidgets.QAction(PolscraperWindow)
        self.actionSentiment.setObjectName("actionSentiment")

        self.actionScheduler = QtWidgets.QAction(PolscraperWindow)
        self.actionScheduler.setObjectName("actionScheduler")

        self.menuMenu.addAction(self.actionMainMenu)
        self.menuMenu.addAction(self.actionExit)
        self.menuPolscraper.addAction(self.actionDataDisplay)
        self.menuPolscraper.addAction(self.actionSentiment)
        self.menuPolscraper.addAction(self.actionScheduler)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPolscraper.menuAction())

        self.retranslateUi(PolscraperWindow)
        QtCore.QMetaObject.connectSlotsByName(PolscraperWindow)

        
        # self.scan_thread = ScannerThread(pages_to_scan, interval)
        # self.scan_thread.scanner_signal.connect(self.scan_complete)

    def retranslateUi(self, PolscraperWindow):
        _translate = QtCore.QCoreApplication.translate
        PolscraperWindow.setWindowTitle(_translate("PolscraperWindow", "Polscraper Main"))
        self.scanButton.setText(_translate("PolscraperWindow", "Scan"))
        self.title.setText(_translate("PolscraperWindow", " Reports Stored"))
        self.intervalLabel.setText(_translate("PolscraperWindow", "Interval"))
        self.pages_label.setText(_translate("PolscraperWindow", "Pages"))
        self.new_scan_title.setText(_translate("PolscraperWindow", "Run New Scan"))
        self.menuMenu.setTitle(_translate("PolscraperWindow", "Menu"))
        self.menuPolscraper.setTitle(_translate("PolscraperWindow", "Polscraper"))
        self.actionMainMenu.setText(_translate("PolscraperWindow", "Main Menu"))
        self.actionExit.setText(_translate("PolscraperWindow", "Exit"))
 
        self.actionPolscraper.setText(_translate("PolscraperWindow", "Polscraper"))

        self.actionDataDisplay.setText(_translate("PolscraperWindow", "Data Display"))
        self.actionScheduler.setText(_translate("PolscraperWindow", "Scheduler"))
        self.actionSentiment.setText(_translate("PolscraperWindow", "Sentiment"))


    def open_file(self, file):
        print("opening " + file.text())
        try:
            os.startfile(f'polscraper\\reports\\{file.text()}')
            self.scan_results_label.setText(f"Opening {file.text()}")
        except Exception as err:
            self.scan_results_label.setText(f"{err}")
        
    def toMainMenu(self):
        print("to main menu")
        self.main_menu=QtWidgets.QMainWindow()
        self.ui = main.Ui_MainWindow()
        self.ui.setupUi(self.main_menu)
        PolscraperWindow.destroy()
        self.main_menu.show()
    def toPolscraperData(self):
        print("to polscraper data")
        self.polscraper_data=QtWidgets.QMainWindow()
        self.ui = polscraper_data.Ui_DataWindow()
        self.ui.setupUi(self.polscraper_data)
        PolscraperWindow.destroy()
        self.polscraper_data.show()


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     PolscraperWindow = QtWidgets.QMainWindow()
#     ui = Ui_PolscraperWindow()
#     ui.setupUi(PolscraperWindow)
#     PolscraperWindow.show()
#     sys.exit(app.exec_())

app = QtWidgets.QApplication(sys.argv)
PolscraperWindow = QtWidgets.QMainWindow()
ui = Ui_PolscraperWindow()
ui.setupUi(PolscraperWindow)

