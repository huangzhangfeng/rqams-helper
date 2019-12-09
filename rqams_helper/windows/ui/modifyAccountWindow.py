# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/modifyAccountWindow.ui',
# licensing of 'ui/modifyAccountWindow.ui' applies.
#
# Created: Wed Nov 20 19:34:15 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_modifyAccountWindow(object):
    def setupUi(self, modifyAccountWindow):
        modifyAccountWindow.setObjectName("modifyAccountWindow")
        modifyAccountWindow.resize(347, 190)
        self.centralwidget = QtWidgets.QWidget(modifyAccountWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 3, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem1, 9, 0, 1, 1)
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 8, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 1, 0, 1, 1)
        self.label_assetUnit = QtWidgets.QLabel(self.centralwidget)
        self.label_assetUnit.setObjectName("label_assetUnit")
        self.gridLayout.addWidget(self.label_assetUnit, 6, 1, 1, 1)
        self.label_broker = QtWidgets.QLabel(self.centralwidget)
        self.label_broker.setObjectName("label_broker")
        self.gridLayout.addWidget(self.label_broker, 2, 1, 1, 1)
        self.comboBox_portfolios = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_portfolios.setObjectName("comboBox_portfolios")
        self.gridLayout.addWidget(self.comboBox_portfolios, 8, 1, 1, 1)
        self.label_account = QtWidgets.QLabel(self.centralwidget)
        self.label_account.setObjectName("label_account")
        self.gridLayout.addWidget(self.label_account, 4, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 7, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem4, 3, 0, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 5, 0, 1, 1)
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
        self.pushButton_done = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_done.setObjectName("pushButton_done")
        self.horizontalLayout.addWidget(self.pushButton_done)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem9)
        self.verticalLayout.addLayout(self.horizontalLayout)
        spacerItem10 = QtWidgets.QSpacerItem(20, 4, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem10)
        modifyAccountWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(modifyAccountWindow)
        QtCore.QMetaObject.connectSlotsByName(modifyAccountWindow)

    def retranslateUi(self, modifyAccountWindow):
        modifyAccountWindow.setWindowTitle(QtWidgets.QApplication.translate("modifyAccountWindow", "账号绑定修改", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "* 资金账号名称", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "* 资金账号", None, -1))
        self.label_name.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "TextLabel", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "* 券商通道", None, -1))
        self.label_5.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "* 组合", None, -1))
        self.label_4.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "* 资产单元", None, -1))
        self.label_assetUnit.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "TextLabel", None, -1))
        self.label_broker.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "TextLabel", None, -1))
        self.label_account.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "TextLabel", None, -1))
        self.pushButton_reset.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "重置", None, -1))
        self.pushButton_done.setText(QtWidgets.QApplication.translate("modifyAccountWindow", "完成", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    modifyAccountWindow = QtWidgets.QMainWindow()
    ui = Ui_modifyAccountWindow()
    ui.setupUi(modifyAccountWindow)
    modifyAccountWindow.show()
    sys.exit(app.exec_())

