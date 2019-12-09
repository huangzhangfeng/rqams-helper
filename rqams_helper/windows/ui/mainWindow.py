# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainWindow.ui',
# licensing of 'ui/mainWindow.ui' applies.
#
# Created: Wed Nov 20 19:34:15 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_search = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_search.setClearButtonEnabled(True)
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.horizontalLayout.addWidget(self.lineEdit_search)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_createAccount = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_createAccount.setObjectName("pushButton_createAccount")
        self.horizontalLayout.addWidget(self.pushButton_createAccount)
        self.pushButton_modifyAccount = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_modifyAccount.setObjectName("pushButton_modifyAccount")
        self.horizontalLayout.addWidget(self.pushButton_modifyAccount)
        self.pushButton_deleteAccount = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_deleteAccount.setObjectName("pushButton_deleteAccount")
        self.horizontalLayout.addWidget(self.pushButton_deleteAccount)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 22))
        self.menubar.setObjectName("menubar")
        self.menu_currentUser = QtWidgets.QMenu(self.menubar)
        self.menu_currentUser.setObjectName("menu_currentUser")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_logout = QtWidgets.QAction(MainWindow)
        self.action_logout.setObjectName("action_logout")
        self.menu_currentUser.addAction(self.action_logout)
        self.menubar.addAction(self.menu_currentUser.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "RQAMS助手", None, -1))
        self.lineEdit_search.setPlaceholderText(QtWidgets.QApplication.translate("MainWindow", "搜索资金账号/产品名称", None, -1))
        self.pushButton_createAccount.setText(QtWidgets.QApplication.translate("MainWindow", "新增", None, -1))
        self.pushButton_modifyAccount.setText(QtWidgets.QApplication.translate("MainWindow", "修改", None, -1))
        self.pushButton_deleteAccount.setText(QtWidgets.QApplication.translate("MainWindow", "删除", None, -1))
        self.menu_currentUser.setTitle(QtWidgets.QApplication.translate("MainWindow", "CurrentUser", None, -1))
        self.action_logout.setText(QtWidgets.QApplication.translate("MainWindow", "登出", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

