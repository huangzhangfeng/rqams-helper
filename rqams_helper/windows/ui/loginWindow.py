# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/loginWindow.ui',
# licensing of 'ui/loginWindow.ui' applies.
#
# Created: Wed Nov 20 19:34:15 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(532, 196)
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setStyleSheet("QTabWidget::tab-bar {alignment: center;}")
        self.tabWidget.setObjectName("tabWidget")
        self.tab_loginWithPhone = QtWidgets.QWidget()
        self.tab_loginWithPhone.setObjectName("tab_loginWithPhone")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_loginWithPhone)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout_loginWithPhone = QtWidgets.QGridLayout()
        self.gridLayout_loginWithPhone.setObjectName("gridLayout_loginWithPhone")
        self.verticalLayout_2.addLayout(self.gridLayout_loginWithPhone)
        self.tabWidget.addTab(self.tab_loginWithPhone, "")
        self.tab_loginWithEmail = QtWidgets.QWidget()
        self.tab_loginWithEmail.setObjectName("tab_loginWithEmail")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_loginWithEmail)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_loginWithEmail = QtWidgets.QGridLayout()
        self.gridLayout_loginWithEmail.setObjectName("gridLayout_loginWithEmail")
        self.gridLayout_3.addLayout(self.gridLayout_loginWithEmail, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_loginWithEmail, "")
        self.verticalLayout.addWidget(self.tabWidget)
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        LoginWindow.setWindowTitle(QtWidgets.QApplication.translate("LoginWindow", "RQAMS账号登录", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_loginWithPhone), QtWidgets.QApplication.translate("LoginWindow", "手机登录", None, -1))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_loginWithEmail), QtWidgets.QApplication.translate("LoginWindow", "邮箱登录", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())

