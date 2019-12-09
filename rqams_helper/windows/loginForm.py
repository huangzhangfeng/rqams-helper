# -*- coding: utf-8 -*-
# 版权所有 2019 深圳米筐科技有限公司（下称“米筐科技”）
#
# 除非遵守当前许可，否则不得使用本软件。
#
#     * 非商业用途（非商业用途指个人出于非商业目的使用本软件，或者高校、研究所等非营利机构出于教育、科研等目的使用本软件）：
#         遵守 Apache License 2.0（下称“Apache 2.0 许可”），您可以在以下位置获得 Apache 2.0 许可的副本：http://www.apache.org/licenses/LICENSE-2.0。
#         除非法律有要求或以书面形式达成协议，否则本软件分发时需保持当前许可“原样”不变，且不得附加任何条件。
#
#     * 商业用途（商业用途指个人出于任何商业目的使用本软件，或者法人或其他组织出于任何目的使用本软件）：
#         未经米筐科技授权，任何个人不得出于任何商业目的使用本软件（包括但不限于向第三方提供、销售、出租、出借、转让本软件、本软件的衍生产品、引用或借鉴了本软件功能或源代码的产品或服务），任何法人或其他组织不得出于任何目的使用本软件，否则米筐科技有权追究相应的知识产权侵权责任。
#         在此前提下，对本软件的使用同样需要遵守 Apache 2.0 许可，Apache 2.0 许可与本许可冲突之处，以本许可为准。
#         详细的授权流程，请联系 public@ricequant.com 获取。

import re
from abc import abstractmethod
from PySide2.QtWidgets import QWidget
from PySide2.QtCore import Signal

from .ui.loginForm import Ui_LoginForm

from rqams_helper.utils.slot import slot
from rqams_helper.utils.widgets import add_enter_press_event, disable_widget, enabled_widget


class _LoginForm(QWidget):
    LOGIN_BUTTON_TOOL_TIP = "请输入合法的用户名和密码"

    login = Signal(str, str, bool)

    invalid_username_msg = None
    username_input_placeholder_text = None

    def __init__(self, *args, **kwargs):
        super(_LoginForm, self).__init__(*args, **kwargs)
        self.ui = Ui_LoginForm()
        self.ui.setupUi(self)

        self.ui.lineEdit_username.textChanged[str].connect(self._check_username_password)
        self.ui.lineEdit_password.textChanged[str].connect(self._check_username_password)
        self.ui.pushButton_login.clicked.connect(self._login)
        disable_widget(self.ui.pushButton_login, self.LOGIN_BUTTON_TOOL_TIP)

        add_enter_press_event(
            (self.ui.lineEdit_username, self.ui.lineEdit_password),
            lambda: self._login() if self.ui.pushButton_login.isEnabled() else None
        )

    def setup(self):
        self.ui.lineEdit_username.clear()
        self.ui.lineEdit_password.clear()
        self.ui.lineEdit_username.setPlaceholderText(self.username_input_placeholder_text)
        self.ui.lineEdit_username.setFocus()

    @abstractmethod
    def _check_username(self, username: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def _get_username(self) -> str:
        return self.ui.lineEdit_username.text()

    @slot
    def _check_username_password(self, _):
        login_enabled = True

        username_text = self.ui.lineEdit_username.text()
        if len(username_text) > 0 and not self._check_username(username_text):
            self.ui.label_usernameHint.setText(self.invalid_username_msg)
            login_enabled = False
        else:
            self.ui.label_usernameHint.setText("")

        if 0 < len(self.ui.lineEdit_password.text()) < 6:
            self.ui.label_passwordHint.setText("密码不能少于6位")
            login_enabled = False
        else:
            self.ui.label_passwordHint.setText("")
        enabled_widget(self.ui.pushButton_login)
        if login_enabled:
            enabled_widget(self.ui.pushButton_login)
        else:
            disable_widget(self.ui.pushButton_login, self.LOGIN_BUTTON_TOOL_TIP)

    @slot
    def _login(self):
        self.login.emit(self._get_username(), self.ui.lineEdit_password.text(), self.ui.checkBox_autoLogin.isChecked())


class PhoneLoginForm(_LoginForm):
    invalid_username_msg = "不合法的手机号"
    username_input_placeholder_text = "输入手机号码"

    def _check_username(self, username: str) -> bool:
        return bool(re.match(r"^1\d{10}$", username))

    def _get_username(self) -> str:
        # TODO: i18n
        return "+86" + self.ui.lineEdit_username.text()


class EmailLoginForm(_LoginForm):
    invalid_username_msg = "不合法的邮箱地址"
    username_input_placeholder_text = "输入邮箱"

    def __init__(self, *args, **kwargs):
        super(EmailLoginForm, self).__init__(*args, **kwargs)
        self.ui.gridLayout_usernameInput.removeWidget(self.ui.comboBox_phoneArea)
        self.ui.comboBox_phoneArea.deleteLater()
        self.ui.gridLayout_usernameInput.removeWidget(self.ui.lineEdit_username)
        self.ui.gridLayout_usernameInput.addWidget(self.ui.lineEdit_username, 0, 1, 1, 2)

    def _check_username(self, username: str) -> bool:
        return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", username))
