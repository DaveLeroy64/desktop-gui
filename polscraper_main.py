# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polscraper_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from polscraper import polscraper


class Ui_PolscraperWindow(object):
    def setupUi(self, PolscraperWindow):
        PolscraperWindow.setObjectName("PolscraperWindow")
        PolscraperWindow.resize(436, 554)
        self.centralwidget = QtWidgets.QWidget(PolscraperWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.scan_results_label = QtWidgets.QLabel(self.centralwidget)
        self.scan_results_label.setGeometry(QtCore.QRect(670, 390, 151, 61))
        self.scan_results_label.setText("")
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

        self.reportsList = QtWidgets.QTableView(self.centralwidget)
        self.reportsList.setGeometry(QtCore.QRect(0, 50, 256, 461))
        self.reportsList.setObjectName("reportsList")

        self.title = QtWidgets.QLabel(self.centralwidget)
        self.title.setGeometry(QtCore.QRect(50, 10, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setObjectName("title")

        self.intervalList = QtWidgets.QComboBox(self.centralwidget)
        self.intervalList.setGeometry(QtCore.QRect(290, 150, 111, 22))
        self.intervalList.setObjectName("intervalList")
        self.intervalList.addItem("Once")
        for i in range(1, 65):
            if i % 5 == 0:
                self.intervalList.addItem(str(i))

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

        self.actionPolscraper = QtWidgets.QAction(PolscraperWindow)
        self.actionPolscraper.setObjectName("actionPolscraper")


        self.actionGraph = QtWidgets.QAction(PolscraperWindow)
        self.actionGraph.setObjectName("actionGraph")
        self.actionTable = QtWidgets.QAction(PolscraperWindow)
        self.actionTable.setObjectName("actionTable")
        self.actionSentiment = QtWidgets.QAction(PolscraperWindow)
        self.actionSentiment.setObjectName("actionSentiment")
        self.menuMenu.addAction(self.actionExit)
        self.menuPolscraper.addAction(self.actionGraph)
        self.menuPolscraper.addAction(self.actionTable)
        self.menuPolscraper.addAction(self.actionSentiment)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPolscraper.menuAction())

        self.retranslateUi(PolscraperWindow)
        QtCore.QMetaObject.connectSlotsByName(PolscraperWindow)

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
        self.actionExit.setText(_translate("PolscraperWindow", "Exit"))
 
        self.actionPolscraper.setText(_translate("PolscraperWindow", "Polscraper"))

        self.actionGraph.setText(_translate("PolscraperWindow", "Graph"))
        self.actionTable.setText(_translate("PolscraperWindow", "Table"))
        self.actionSentiment.setText(_translate("PolscraperWindow", "Sentiment"))

    def run_scanner(self):
        pages = self.pagesList.currentText()
        interval = self.intervalList.currentText()
        polscraper.test(pages, interval)

        if interval != "Once":
            polscraper.repeating(interval, pages)
        else:
            polscraper.single(pages)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PolscraperWindow = QtWidgets.QMainWindow()
    ui = Ui_PolscraperWindow()
    ui.setupUi(PolscraperWindow)
    PolscraperWindow.show()
    sys.exit(app.exec_())
