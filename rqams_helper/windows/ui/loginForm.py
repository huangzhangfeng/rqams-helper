# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/loginForm.ui',
# licensing of 'ui/loginForm.ui' applies.
#
# Created: Wed Nov 20 19:34:15 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_LoginForm(object):
    def setupUi(self, LoginForm):
        LoginForm.setObjectName("LoginForm")
        LoginForm.resize(745, 157)
        self.gridLayout = QtWidgets.QGridLayout(LoginForm)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_usernameHint = QtWidgets.QLabel(LoginForm)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_usernameHint.setFont(font)
        self.label_usernameHint.setStyleSheet("color: rgba(0, 0, 0, 130)")
        self.label_usernameHint.setText("")
        self.label_usernameHint.setObjectName("label_usernameHint")
        self.horizontalLayout_2.addWidget(self.label_usernameHint)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_login = QtWidgets.QPushButton(LoginForm)
        self.pushButton_login.setEnabled(False)
        self.pushButton_login.setObjectName("pushButton_login")
        self.horizontalLayout_3.addWidget(self.pushButton_login)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 5, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_passwordHint = QtWidgets.QLabel(LoginForm)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setStrikeOut(False)
        self.label_passwordHint.setFont(font)
        self.label_passwordHint.setStyleSheet("color: rgba(0, 0, 0, 130)")
        self.label_passwordHint.setText("")
        self.label_passwordHint.setObjectName("label_passwordHint")
        self.horizontalLayout_4.addWidget(self.label_passwordHint)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.checkBox_autoLogin = QtWidgets.QCheckBox(LoginForm)
        self.checkBox_autoLogin.setObjectName("checkBox_autoLogin")
        self.horizontalLayout_4.addWidget(self.checkBox_autoLogin)
        self.gridLayout.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 28, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 4, 0, 1, 1)
        self.lineEdit_password = QtWidgets.QLineEdit(LoginForm)
        self.lineEdit_password.setInputMask("")
        self.lineEdit_password.setText("")
        self.lineEdit_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_password.setClearButtonEnabled(True)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.gridLayout.addWidget(self.lineEdit_password, 2, 0, 1, 1)
        self.gridLayout_usernameInput = QtWidgets.QGridLayout()
        self.gridLayout_usernameInput.setObjectName("gridLayout_usernameInput")
        self.comboBox_phoneArea = QtWidgets.QComboBox(LoginForm)
        self.comboBox_phoneArea.setObjectName("comboBox_phoneArea")
        self.comboBox_phoneArea.addItem("")
        self.gridLayout_usernameInput.addWidget(self.comboBox_phoneArea, 0, 0, 1, 1)
        self.lineEdit_username = QtWidgets.QLineEdit(LoginForm)
        self.lineEdit_username.setInputMask("")
        self.lineEdit_username.setText("")
        self.lineEdit_username.setClearButtonEnabled(True)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.gridLayout_usernameInput.addWidget(self.lineEdit_username, 0, 1, 1, 1)
        self.gridLayout_usernameInput.setColumnStretch(1, 1)
        self.gridLayout.addLayout(self.gridLayout_usernameInput, 0, 0, 1, 1)

        self.retranslateUi(LoginForm)
        QtCore.QMetaObject.connectSlotsByName(LoginForm)
        LoginForm.setTabOrder(self.lineEdit_username, self.comboBox_phoneArea)
        LoginForm.setTabOrder(self.comboBox_phoneArea, self.lineEdit_password)
        LoginForm.setTabOrder(self.lineEdit_password, self.checkBox_autoLogin)
        LoginForm.setTabOrder(self.checkBox_autoLogin, self.pushButton_login)

    def retranslateUi(self, LoginForm):
        LoginForm.setWindowTitle(QtWidgets.QApplication.translate("LoginForm", "Form", None, -1))
        self.pushButton_login.setText(QtWidgets.QApplication.translate("LoginForm", "确认登录", None, -1))
        self.checkBox_autoLogin.setText(QtWidgets.QApplication.translate("LoginForm", "15 天内自动登录", None, -1))
        self.lineEdit_password.setPlaceholderText(QtWidgets.QApplication.translate("LoginForm", "输入密码", None, -1))
        self.comboBox_phoneArea.setItemText(0, QtWidgets.QApplication.translate("LoginForm", "中国内地(+86)", None, -1))
        self.lineEdit_username.setPlaceholderText(QtWidgets.QApplication.translate("LoginForm", "输入手机号码", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    LoginForm = QtWidgets.QWidget()
    ui = Ui_LoginForm()
    ui.setupUi(LoginForm)
    LoginForm.show()
    sys.exit(app.exec_())

