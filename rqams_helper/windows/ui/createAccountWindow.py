# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/createAccountWindow.ui',
# licensing of 'ui/createAccountWindow.ui' applies.
#
# Created: Wed Nov 20 19:34:14 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_CreateAccountWIndow(object):
    def setupUi(self, CreateAccountWIndow):
        CreateAccountWIndow.setObjectName("CreateAccountWIndow")
        CreateAccountWIndow.resize(349, 243)
        self.centralwidget = QtWidgets.QWidget(CreateAccountWIndow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_portfolios = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_portfolios.setObjectName("comboBox_portfolios")
        self.gridLayout.addWidget(self.comboBox_portfolios, 9, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_products = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_products.setEnabled(True)
        self.lineEdit_products.setObjectName("lineEdit_products")
        self.gridLayout.addWidget(self.lineEdit_products, 11, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 1)
        self.comboBox_broker = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_broker.setObjectName("comboBox_broker")
        self.gridLayout.addWidget(self.comboBox_broker, 3, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 1, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.comboBox_assetUnits = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_assetUnits.setObjectName("comboBox_assetUnits")
        self.gridLayout.addWidget(self.comboBox_assetUnits, 7, 1, 1, 1)
        self.lineEdit_account = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_account.setMaxLength(16)
        self.lineEdit_account.setObjectName("lineEdit_account")
        self.gridLayout.addWidget(self.lineEdit_account, 5, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 8, 0, 1, 1)
        self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_name.setMaxLength(100)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.gridLayout.addWidget(self.lineEdit_name, 0, 1, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 11, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 10, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem6 = QtWidgets.QSpacerItem(20, 0, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem6)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem7)
        self.pushButton_reset = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_reset.setObjectName("pushButton_reset")
        self.horizontalLayout.addWidget(self.pushButton_reset)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem8)
        self.pushButton_create = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_create.setObjectName("pushButton_create")
        self.horizontalLayout.addWidget(self.pushButton_create)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem10 = QtWidgets.QSpacerItem(20, 1, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        CreateAccountWIndow.setCentralWidget(self.centralwidget)

        self.retranslateUi(CreateAccountWIndow)
        QtCore.QMetaObject.connectSlotsByName(CreateAccountWIndow)

    def retranslateUi(self, CreateAccountWIndow):
        CreateAccountWIndow.setWindowTitle(QtWidgets.QApplication.translate("CreateAccountWIndow", "账号新增", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "* 资金账号名称", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "* 资金账号", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "* 资产单元", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "* 组合", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "* 券商通道", None, -1))
        self.label_6.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "产品", None, -1))
        self.pushButton_reset.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "重置", None, -1))
        self.pushButton_create.setText(QtWidgets.QApplication.translate("CreateAccountWIndow", "完成", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    CreateAccountWIndow = QtWidgets.QMainWindow()
    ui = Ui_CreateAccountWIndow()
    ui.setupUi(CreateAccountWIndow)
    CreateAccountWIndow.show()
    sys.exit(app.exec_())

