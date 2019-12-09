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

import os
from typing import Dict, Optional, Iterable
from collections import OrderedDict

from PySide2.QtWidgets import (
    QMainWindow, QTableWidgetItem, QTableWidget, QWidget, QHBoxLayout, QLineEdit, QCheckBox, QHeaderView,
)
from PySide2.QtCore import Signal, Qt, QObject

from rqams_client.client import RQAMSClient
from rqams_client.models import Account, Portfolio
from rqams_client.utils import ReqestException

from rqams_helper.utils.slot import slot
from rqams_helper.utils.logger import logger
from rqams_helper.utils.widgets import disable_widget, enabled_widget, ToggleSwitch, MessageBox, ConfirmMessageBox
from rqams_helper.utils.future import Future
from rqams_helper.utils.exceptions import RQAmsHelperException
from rqams_helper.ctp_controller import CtpAccount

from .ui.mainWindow import Ui_MainWindow
from .resources import get_icon


class Cell(QObject):
    header = ""
    resize_mode = QHeaderView.ResizeToContents

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(Cell, self).__init__()
        self._table_widget = table_widget

    def set(self, row: int, column: int):
        raise NotImplementedError

    @classmethod
    def get_header_item(cls):
        item = QTableWidgetItem(cls.header)
        item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        return item

    def setEnabled(self, enabled, disable_tool_tip):
        raise NotImplementedError


class EmptyCell(Cell):
    def __init__(self, table_widget: QTableWidget, account: Account):
        super(EmptyCell, self).__init__(table_widget, account)
        self._item = QTableWidgetItem()
        self._item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self._row = self._column = None

    def set(self, row: int, column: int):
        self._row, self._column = row, column
        self._table_widget.setItem(row, column, self._item)

    def setEnabled(self, enabled, disable_tool_tip):
        if enabled:
            self._item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            self._item.setToolTip("")
        else:
            self._item.setFlags(~(Qt.ItemIsEnabled | Qt.ItemIsSelectable))
            self._item.setToolTip(disable_tool_tip)


class TextCell(EmptyCell):
    def __init__(self, table_widget: QTableWidget, account: Account):
        super(TextCell, self).__init__(table_widget, account)
        self._account = account
        self._item.setText(self._get_text(account))
        self.setText = self._item.setText

    def _get_text(self, account: Account):
        raise NotImplementedError


class WidgetCell(Cell):
    def __init__(self, table_widget: QTableWidget, account: Account):
        super(WidgetCell, self).__init__(table_widget, account)
        self._layout = QHBoxLayout()
        self._widget = QWidget()

        self._layout.setMargin(0)
        self._layout.setAlignment(Qt.AlignHCenter)
        self._widget.setLayout(self._layout)

    def set(self, row: int, column: int):
        self._table_widget.setCellWidget(row, column, self._widget)

    def setEnabled(self, enabled: bool, disable_tool_tip: str = ""):
        if enabled:
            enabled_widget(self._widget)
        else:
            disable_widget(self._widget, disable_tool_tip)


class CheckBoxCell(WidgetCell):
    def __init__(self, table_widget: QTableWidget, account: Account):
        super(CheckBoxCell, self).__init__(table_widget, account)
        self._checkbox = QCheckBox()
        self._layout.addWidget(self._checkbox)
        self.isChecked = self._checkbox.isChecked
        self.stateChanged = self._checkbox.stateChanged
        self.setCheckState = self._checkbox.setCheckState


class CheckCell(CheckBoxCell):
    header = ""


class BrokerCell(TextCell):
    header = "券商通道"
    resize_mode = QHeaderView.Stretch

    def _get_text(self, account: Account):
        return account.broker.name


class NameCell(TextCell):
    header = "资金账号名称"
    resize_mode = QHeaderView.Stretch

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(NameCell, self).__init__(table_widget, account)
        self._item.setToolTip(self._get_text(account))

    def _get_text(self, account: Account):
        return account.name

    def setEnabled(self, enabled, disable_tool_tip):
        super(NameCell, self).setEnabled(enabled, disable_tool_tip)
        if enabled:
            self._item.setToolTip(self._get_text(self._account))


class AccountCell(TextCell):
    header = "资金账号"
    resize_mode = QHeaderView.Stretch

    def _get_text(self, account: Account):
        return account.account


class AccountPasswordLineEdit(QLineEdit):
    focusLost = Signal()

    def __init__(self):
        super(AccountPasswordLineEdit, self).__init__()
        self.setEchoMode(self.Password)

    def focusOutEvent(self, event):
        self.focusLost.emit()
        super(AccountPasswordLineEdit, self).focusOutEvent(event)


class PasswordCell(WidgetCell):
    header = "账号密码"

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(PasswordCell, self).__init__(table_widget, account)
        self._line_edit = AccountPasswordLineEdit()
        self._layout.addWidget(self._line_edit)
        self.textChanged = self._line_edit.textChanged
        self.focusLost = self._line_edit.focusLost
        self._line_edit.setPlaceholderText("请输入密码")

    def text(self):
        return self._line_edit.text()

    def setText(self, text):
        self._line_edit.setText(text)


class RememberPasswordCell(CheckBoxCell):
    header = "保存密码"


class SwitchCell(WidgetCell):
    header = "连接开关"
    checked = Signal(Account)
    unchecked = Signal(Account)

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(SwitchCell, self).__init__(table_widget, account)
        self._account = Account
        self._switch = ToggleSwitch()
        self._layout.addWidget(self._switch)
        self.isChecked = self._switch.isChecked
        self.switched = self._switch.toggled


class AssetUnitCell(TextCell):
    header = "资产单元名称"
    resize_mode = QHeaderView.Stretch

    def _get_text(self, account: Account):
        return account.asset_unit.name


class PortfolioCell(TextCell):
    header = "组合名称"
    resize_mode = QHeaderView.Stretch

    def _get_text(self, account: Account):
        return account.portfolio.name


class ProductCell(TextCell):
    header = "产品名称"
    resize_mode = QHeaderView.Stretch

    def _get_text(self, account: Account):
        product = account.product
        if product:
            return product.name
        return ""


class StateCell(EmptyCell):
    header = "连接状态"
    TEXT_OFF = "未连接"
    TEXT_ON = "已连接"

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(StateCell, self).__init__(table_widget, account)
        self._item.setText(self.TEXT_OFF)

    def update_state(self, connected: bool):
        self._item.setText(self.TEXT_ON if connected else self.TEXT_OFF)


class InfoCell(EmptyCell):
    header = "连接信息"

    def __init__(self, table_widget: QTableWidget, account: Account):
        super(InfoCell, self).__init__(table_widget, account)
        self._item.setText("未开启连接")
        self.setText = self._item.setText

    def update_info(self, info: str):
        self._item.setText(info)


class Row(QObject):
    TOGGLE_TOOL_TIP = "资金账号连接期间不能编辑/删除资金账号"

    check: CheckCell
    broker: BrokerCell
    name: NameCell
    account: AccountCell
    password: PasswordCell
    remember_password: RememberPasswordCell
    switch: SwitchCell
    asset_unit: AssetUnitCell
    portfolio: PortfolioCell
    product: ProductCell
    state: StateCell
    info: InfoCell

    connect_account = Signal(CtpAccount)
    disconnect_account = Signal(str)
    save_password = Signal(str, str)
    unsave_password = Signal(str)

    def __init__(self, table_widget: QTableWidget, account: Account, password: Optional[str]):
        super(Row, self).__init__()
        self._table_widget = table_widget
        self._account = account
        for name, CellType in self.__annotations__.items():
            cell = CellType(table_widget, account)
            self.__dict__[name] = cell
        self.switch.switched.connect(self._switched)
        self.password.textChanged[str].connect(self._password_changed)
        self.password.focusLost.connect(self._save_password)
        self.remember_password.stateChanged.connect(self._remember_password_state_changed)
        if password:
            self.password.setText(password)
            self.remember_password.setCheckState(Qt.Checked)
        self.checkStateChanged = self.check.stateChanged
        self.isChecked = self.check.isChecked
        self.enabled = False

    def search(self, text: str):
        if self._account.product:
            return text in self._account.account or text in self._account.product.name
        return text in self._account.account

    def setup(self, row: int):
        for i, name in enumerate(self.__annotations__.keys()):
            cell = self.__dict__[name] # type: Cell
            cell.set(row, i)

    def setEnabled(self, enabled: bool, disable_tool_tip: Optional[str] = ""):
        self.enabled = enabled
        for name in self.__annotations__.keys():
            cell = self.__dict__[name]
            cell.setEnabled(enabled, disable_tool_tip)
        if enabled:
            self._password_changed(self.password.text())
            self._switched(self.switch.isChecked())

    def update_state_info(self, connected: bool, info: str):
        if connected is not None:
            self.state.update_state(connected)
        if info is not None:
            self.info.update_info(info)

    def get_account(self):
        return self._account

    @classmethod
    def set_header(cls, table_widget: QTableWidget):
        table_widget.setColumnCount(len(cls.__annotations__))
        table_widget.setRowCount(0)

        for i, CellType in enumerate(cls.__annotations__.values()):
            table_widget.setHorizontalHeaderItem(i, CellType.get_header_item())

    @classmethod
    def set_resize_mode(cls, table_widget: QTableWidget):
        header = table_widget.horizontalHeader()
        for i, CellType in enumerate(cls.__annotations__.values()):
            header.setSectionResizeMode(i, CellType.resize_mode)

    @slot
    def _switched(self, checked):
        edit_enabled = not checked
        self.check.setEnabled(edit_enabled, self.TOGGLE_TOOL_TIP)
        self.remember_password.setEnabled(edit_enabled, self.TOGGLE_TOOL_TIP)
        self.password.setEnabled(edit_enabled, self.TOGGLE_TOOL_TIP)

        if checked:
            ctp_account = CtpAccount(
                fronts=self._account.broker.trade_frontend_urls,
                broker_id=self._account.broker.broker_id,
                account=self._account.account,
                password=self.password.text(),
                user_product_info=self._account.broker.user_product_info,
                auth_code=self._account.broker.auth_code,
                app_id=self._account.broker.app_id
            )
            self.check.setCheckState(Qt.Unchecked)
            self.connect_account.emit(ctp_account)
        else:
            self.disconnect_account.emit(self._account.account)

    @slot
    def _password_changed(self, password_text):
        self.switch.setEnabled(len(password_text) > 0, "请输入密码")

    @slot
    def _remember_password_state_changed(self, checked):
        if checked == Qt.Checked:
            self.save_password.emit(self._account.account, self.password.text())
        else:
            self.unsave_password.emit(self._account.account)

    @slot
    def _save_password(self, *a_):
        if self.remember_password.isChecked():
            self.save_password.emit(self._account.account, self.password.text())


def _sync_account_deletion(client: RQAMSClient, account: str):
    try:
        del client.accounts[account]
    except ReqestException as e:
        if e.response.status_code == 404:
            logger.warn("delete account {} failed with response: {}, {}".format(
                account, e.response.status_code, getattr(e.response, "content", "")
            ))
        else:
            raise


def _sync_account_creation(client: RQAMSClient, account: Account):
    try:
        client.accounts[account.account] = account
    except Exception as e:
        return account.account, e
    else:
        return account.account, None


class MainWindow(QMainWindow):
    MODIFY_BUTTON_TOOLTTIP = "请选择一个资金账号"
    DELETE_BUTTON_TOOLTIP = "请选择资金账号"

    create_button_pushed = Signal(RQAMSClient, set, set, set)
    modify_button_pushed = Signal(Account)
    connect_account = Signal(CtpAccount)
    disconnect_account = Signal(str)

    def __init__(self, persister):
        super(MainWindow, self).__init__()

        self._persister = persister

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_createAccount.clicked.connect(self._on_create_button_pushed)
        self.ui.pushButton_deleteAccount.clicked.connect(self._delete)
        self.ui.pushButton_modifyAccount.clicked.connect(self._on_modify_button_pushed)
        self.ui.lineEdit_search.textChanged[str].connect(self._search)

        self.logout_button_pushed = self.ui.action_logout.triggered

        self.setWindowIcon(get_icon())

        self._client = None
        self._user_id = None
        self._account_row_map: Dict[str, Row] = OrderedDict()
        self._current_accounts: Dict = {}

        Row.set_header(self.ui.tableWidget)
        Row.set_resize_mode(self.ui.tableWidget)

    @property
    def current_accounts(self):
        return self._current_accounts

    def setup(self, client: RQAMSClient, username: str, user_id: int):
        self._client = client
        self._user_id = user_id
        self._account_row_map.clear()
        self.ui.tableWidget.setRowCount(0)

        self.ui.menu_currentUser.setTitle(username)

        for btn in (
            self.ui.pushButton_createAccount, self.ui.pushButton_modifyAccount, self.ui.pushButton_deleteAccount
        ):
            disable_widget(btn, "数据正在加载")
        Future(self, lambda c: list(c.accounts.values()), (client, ), self._update_accounts).run()

    def update_account_state_info(self, account: str, connected: Optional[bool], info: Optional[str]):
        try:
            row = self._account_row_map[account]
        except KeyError:
            # TODO: need warning
            pass
        else:
            row.update_state_info(connected, info)

    def create_account(self, account: Account):
        if account.account in self._account_row_map:
            MessageBox(MessageBox.Warning, "添加账号失败", f"添加账号失败，账号 {account.account} 已存在").exec_()
            return
        row = self._add_account(account)
        row.setEnabled(False, "请等待资金账户同步完成")
        Future(self, _sync_account_creation, (self._client, account), self._on_account_synced).run()

    def modify_account(self, account: str, portfolio: Portfolio):
        try:
            row = self._account_row_map[account]
        except KeyError:
            MessageBox(MessageBox.Warning, "修改账号失败", f"修改账号失败，账号 {account} 不存在").exec_()
            return
        else:
            row.portfolio.setText(portfolio.name)

    def _add_account(self, account: Account):
        self._current_accounts[account.account] = account
        row_index = len(self._account_row_map)
        row = Row(self.ui.tableWidget, account, self._persister.get_password(self._user_id, account.account))
        row.connect_account.connect(self._connect_account)
        row.disconnect_account.connect(self._disconnect_account)
        row.checkStateChanged.connect(self._row_check_state_changed)
        row.save_password.connect(self._save_password)
        row.unsave_password.connect(self._unsave_password)
        self._account_row_map[account.account] = row
        self.ui.tableWidget.insertRow(row_index)
        row.setup(row_index)
        search_text = self.ui.lineEdit_search.text()
        if search_text and not row.search(search_text):
            self.ui.tableWidget.hideRow(row_index)
        return row

    def _update_accounts(self, accounts: Iterable[Account]):
        for account in accounts:
            row = self._add_account(account)
            row.setEnabled(True)
            row.info.setText("未开启连接")
        enabled_widget(self.ui.pushButton_createAccount)
        disable_widget(self.ui.pushButton_modifyAccount, self.MODIFY_BUTTON_TOOLTTIP)
        disable_widget(self.ui.pushButton_deleteAccount, self.DELETE_BUTTON_TOOLTIP)

    @slot
    def _on_account_synced(self, result):
        account, exception = result
        row = self._account_row_map[account]
        if exception:
            if isinstance(exception, ReqestException) and exception.response.status_code == 409:
                reason = "资金账号同步失败，资金账号已存在或产品/资产单元已被其他资金账号绑定"
                exception = RQAmsHelperException(reason, "同步资金账号失败")
            else:
                reason = "资金账号同步失败，请删除后尝试重新添加"
            row.setEnabled(False, reason)
            row.check.setEnabled(True)
            raise exception
        else:
            row.setEnabled(True)
            row.info.setText("未开启连接")

    @slot
    def _on_create_button_pushed(self):
        account_black_list, portfolio_black_list, asset_unit_black_list = set(), set(), set()
        for row in self._account_row_map.values():
            account = row.get_account()
            account_black_list.add(account.account)
            portfolio_black_list.add(account.portfolio.id)
            asset_unit_black_list.add(account.asset_unit.id)

        self.create_button_pushed.emit(self._client, account_black_list, portfolio_black_list, asset_unit_black_list)

    @slot
    def _on_modify_button_pushed(self):
        for row in self._account_row_map.values():
            if row.isChecked():
                self.modify_button_pushed.emit(row.get_account())
                row.check.setCheckState(Qt.Unchecked)
                break
        else:
            raise RuntimeError("no account has been chenked")
        self._row_check_state_changed()

    @slot
    def _row_check_state_changed(self, *_):
        check_count = 0
        disabled_row_checked = False

        for row in self._account_row_map.values():
            if row.isChecked():
                check_count += 1
                if not row.enabled:
                    disabled_row_checked = True

        if check_count > 0:
            enabled_widget(self.ui.pushButton_deleteAccount)
        else:
            disable_widget(self.ui.pushButton_deleteAccount, self.DELETE_BUTTON_TOOLTIP)

        if check_count == 1 and not disabled_row_checked:
            enabled_widget(self.ui.pushButton_modifyAccount)
        else:
            disable_widget(self.ui.pushButton_modifyAccount, self.MODIFY_BUTTON_TOOLTTIP)

    @slot
    def _delete(self):
        account_to_be_delete = [account for account, row in self._account_row_map.items() if row.isChecked()]
        if ConfirmMessageBox(
            "删除确认", "资金账号 {} 将被删除".format("，".join(account_to_be_delete))
        ).exec_() != MessageBox.Ok:
            for account in account_to_be_delete:
                self._account_row_map[account].check.setCheckState(Qt.Unchecked)
            return
        offset = 0
        for i, (account, row) in enumerate(self._account_row_map.copy().items()):
            if row.isChecked():
                self._account_row_map.pop(account)
                self._current_accounts.pop(account, None)
                self.ui.tableWidget.removeRow(i - offset)
                Future(self, _sync_account_deletion, (self._client, account)).run()
                offset += 1
            else:
                if offset > 0:
                    row.setup(i - offset)
        self._row_check_state_changed()
        self._persister.clear_password(self._user_id, account_to_be_delete)

    @slot
    def _search(self, text: str):
        for i, (account, row) in enumerate(self._account_row_map.items()):
            if text and not row.search(text):
                self.ui.tableWidget.hideRow(i)
            else:
                self.ui.tableWidget.showRow(i)

    @slot
    def _connect_account(self, ctp_account: CtpAccount):
        self.connect_account.emit(ctp_account)

    @slot
    def _disconnect_account(self, account: str):
        self.disconnect_account.emit(account)

    @slot
    def _save_password(self, account: str, password: str):
        self._persister.save_password(self._user_id, account, password)

    @slot
    def _unsave_password(self, account: str):
        self._persister.clear_password(self._user_id, [account])

    def closeEvent(self, event):
        activated_account = [account for account, row in self._account_row_map.items() if row.switch.isChecked()]
        if len(activated_account) > 0:
            if ConfirmMessageBox(
                    "操作确认", "当前操作将断开资金账号 {}。".format("，".join(activated_account))
            ).exec_() != MessageBox.Ok:
                event.ignore()
                return

        for account, row in self._account_row_map.items():
            if row.isChecked():
                self._disconnect_account(account)
        event.accept()
