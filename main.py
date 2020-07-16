# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from scripts import news_scraper
from properties import Ui_PropertyWindow

import sqlite3
print("called")

class Ui_MainWindow(object):


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Python Control Panel")
        MainWindow.resize(826, 554)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.news_list_view = QtWidgets.QListWidget(self.centralwidget)
        self.news_list_view.setGeometry(QtCore.QRect(0, 50, 256, 431))
        self.news_list_view.setObjectName("news_list_view")
        self.news_list_view.setWordWrap(True)
        # self.news_list_view.setText("Fetching news...")

        self.weather_text_browser = QtWidgets.QTextBrowser(self.centralwidget)
        self.weather_text_browser.setGeometry(QtCore.QRect(550, 50, 271, 61))
        self.weather_text_browser.setObjectName("weather_text_browser")

        self.news_label = QtWidgets.QLabel(self.centralwidget)
        self.news_label.setGeometry(QtCore.QRect(60, 20, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.news_label.setFont(font)
        self.news_label.setAlignment(QtCore.Qt.AlignCenter)
        self.news_label.setObjectName("news_label")

        self.weather_label = QtWidgets.QLabel(self.centralwidget)
        self.weather_label.setGeometry(QtCore.QRect(630, 20, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.weather_label.setFont(font)
        self.weather_label.setAlignment(QtCore.Qt.AlignCenter)
        self.weather_label.setObjectName("weather_label")

        self.view_news_button = QtWidgets.QPushButton(self.centralwidget)
        self.view_news_button.setGeometry(QtCore.QRect(90, 490, 75, 23))
        self.view_news_button.setObjectName("view_news_button")
        self.view_news_button.clicked.connect(self.loadData)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 826, 21))
        self.menubar.setObjectName("menubar")

        self.menuMenu = QtWidgets.QMenu(self.menubar)
        self.menuMenu.setObjectName("menuMenu")

        self.menuPrograms = QtWidgets.QMenu(self.menubar)
        self.menuPrograms.setObjectName("menuPrograms")

        self.menuAPI = QtWidgets.QMenu(self.menubar)
        self.menuAPI.setObjectName("menuAPI")

        self.menuComputer = QtWidgets.QMenu(self.menubar)
        self.menuComputer.setObjectName("menuComputer")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionNews_Scraper = QtWidgets.QAction(MainWindow)
        self.actionNews_Scraper.setObjectName("actionNews_Scraper")

        self.actionProperty_Data = QtWidgets.QAction(MainWindow)
        self.actionProperty_Data.setObjectName("actionProperty_Data")
        self.actionProperty_Data.triggered.connect(self.to_properties)

        self.actionPolscraper = QtWidgets.QAction(MainWindow)
        self.actionPolscraper.setObjectName("actionPolscraper")

        self.actionDarkSky_Weather = QtWidgets.QAction(MainWindow)
        self.actionDarkSky_Weather.setObjectName("actionDarkSky_Weather")

        self.actionLocal_Information = QtWidgets.QAction(MainWindow)
        self.actionLocal_Information.setObjectName("actionLocal_Information")

        self.actionLock = QtWidgets.QAction(MainWindow)
        self.actionLock.setObjectName("actionLock")

        self.menuMenu.addAction(self.actionExit)
        self.menuPrograms.addAction(self.actionNews_Scraper)
        self.menuPrograms.addAction(self.actionProperty_Data)
        self.menuPrograms.addAction(self.actionPolscraper)
        self.menuAPI.addAction(self.actionDarkSky_Weather)
        self.menuAPI.addAction(self.actionLocal_Information)
        self.menuComputer.addAction(self.actionLock)
        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuPrograms.menuAction())
        self.menubar.addAction(self.menuAPI.menuAction())
        self.menubar.addAction(self.menuComputer.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.news_label.setText(_translate("MainWindow", "RECENT NEWS"))
        self.weather_label.setText(_translate("MainWindow", "WEATHER"))
        self.view_news_button.setText(_translate("MainWindow", "View"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuPrograms.setTitle(_translate("MainWindow", "Programs"))
        self.menuAPI.setTitle(_translate("MainWindow", "API"))
        self.menuComputer.setTitle(_translate("MainWindow", "Computer"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionNews_Scraper.setText(_translate("MainWindow", "News Scraper"))
        self.actionProperty_Data.setText(_translate("MainWindow", "Property Data"))
        self.actionPolscraper.setText(_translate("MainWindow", "Polscraper"))
        self.actionDarkSky_Weather.setText(_translate("MainWindow", "DarkSky Weather"))
        self.actionLocal_Information.setText(_translate("MainWindow", "Local Information"))
        self.actionLock.setText(_translate("MainWindow", "Lock"))

    def to_properties(self, MainWindow):
        # if password = correct
        self.property_window=QtWidgets.QMainWindow()
        self.ui = Ui_PropertyWindow()
        self.ui.setupUi(self.property_window)
        self.property_window.show()
        # MainWindow.close()

    def loadData(self):
        print("Begin scan")
        news_scraper.scanner()
        print("Scan complete")
        conn=sqlite3.connect("pcp.db")
        cur=conn.cursor()
        cur.execute("SELECT * FROM newsitems")
        result = cur.fetchall()
        for r in result:
            r[3].replace("\n", "")
            newsitem = str(r[1]) + "\n" + str(r[3] + "\n---------------------------------------------")
            self.news_list_view.addItem(newsitem)




if __name__ == "__main__":
    print("called from other")
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
