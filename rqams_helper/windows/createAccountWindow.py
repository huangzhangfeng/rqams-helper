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
from typing import Optional, Sequence, List, Set, Tuple

from PySide2.QtWidgets import QMainWindow, QComboBox
from PySide2.QtCore import Signal, Qt

from rqams_client.client import RQAMSClient
from rqams_client.models import AssetUnit, Portfolio, Broker, Product, Account
from rqams_client.utils import ReqestException

from rqams_helper.utils.slot import slot
from rqams_helper.utils.widgets import add_enter_press_event, disable_widget, enabled_widget
from rqams_helper.utils.future import Future
from .ui.createAccountWindow import Ui_CreateAccountWIndow
from .resources import get_icon


def _disable_combo_box(box: QComboBox):
    disable_widget(box, "数据正在加载")
    box.clear()


def _enable_combo_box(box: QComboBox, items: List[str]):
    box.addItems(items)
    enabled_widget(box)


class CreateAccountWindow(QMainWindow):
    account_created = Signal(Account)

    def __init__(self):
        super(CreateAccountWindow, self).__init__(None, Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)

        self.ui = Ui_CreateAccountWIndow()
        self.ui.setupUi(self)
        self.ui.lineEdit_products.setReadOnly(True)

        self.ui.pushButton_reset.clicked.connect(self._reset)
        self.ui.lineEdit_account.textChanged[str].connect(self._check_form)
        self.ui.lineEdit_name.textChanged[str].connect(self._check_form)
        self.ui.comboBox_assetUnits.currentIndexChanged.connect(self._on_asset_unit_changed)
        self.ui.pushButton_create.clicked.connect(self._on_create_button_clicked)

        self.setWindowIcon(get_icon())

        self._client: Optional[RQAMSClient]= None
        self._brokers: Optional[Sequence[Broker]] = None
        self._asset_units: Optional[Sequence[AssetUnit]] = None
        self._portfolios: Optional[Sequence[Portfolio]] = None
        self._product: Optional[Product] = None

        self._account_black_list: Set[str] = set()
        self._portfolio_black_list: Set[str] = set()
        self._asset_unit_black_list: Set[str] = set()

        add_enter_press_event(
            (self.ui.lineEdit_account, self.ui.lineEdit_name),
            lambda: self._on_create_button_clicked() if self.ui.pushButton_create.isEnabled() else None
        )

    def setup(
            self, client: RQAMSClient, account_black_list: Set[str], portfolio_black_list: Set[str],
            asset_unit_black_list: Set[str]
    ):
        self._client = client
        self._brokers = self._asset_units = self._portfolios = self._product = None
        self._account_black_list = account_black_list
        self._portfolio_black_list = portfolio_black_list
        self._asset_unit_black_list = asset_unit_black_list

        for lineEdit in (self.ui.lineEdit_name, self.ui.lineEdit_account, self.ui.lineEdit_products):
            lineEdit.clear()
        self.ui.lineEdit_products.setReadOnly(True)
        for comboBox in (self.ui.comboBox_assetUnits, self.ui.comboBox_portfolios, self.ui.comboBox_broker):
            _disable_combo_box(comboBox)
        disable_widget(self.ui.pushButton_create, "请输入/选择所有字段")

        Future(self, lambda c: list(c.brokers.values()), (client, ), self._update_brokers).run()
        Future(self, lambda c: list(c.asset_units.values()), (client, ), self._update_asset_units).run()

    @slot
    def _on_asset_unit_changed(self, index):
        self.ui.lineEdit_products.setText("")
        if self._asset_units:
            _disable_combo_box(self.ui.comboBox_portfolios)
            Future(
                self, lambda a: (list(a.portfolios.values()), a.product), (self._asset_units[index], ),
                self._update_portfolios_and_product
            ).run()

    @slot
    def _on_create_button_clicked(self):
        account = Account(
            name=self.ui.lineEdit_name.text(),
            account=self.ui.lineEdit_account.text(),
            broker=self._brokers[self.ui.comboBox_broker.currentIndex()],
            portfolio=self._portfolios[self.ui.comboBox_portfolios.currentIndex()],
            asset_unit=self._asset_units[self.ui.comboBox_assetUnits.currentIndex()],
            product=self._product,
            client=self._client,
        )
        self.account_created.emit(account)

    def _update_brokers(self, brokers: Sequence[Broker]):
        self._brokers = brokers
        _enable_combo_box(self.ui.comboBox_broker, [b.name for b in brokers])
        self._check_form()

    def _update_asset_units(self, asset_units: Sequence[AssetUnit]):
        self._asset_units = [a for a in asset_units if a.id not in self._asset_unit_black_list]
        _enable_combo_box(self.ui.comboBox_assetUnits, [a.name for a in self._asset_units])
        self._check_form()

    def _update_portfolios_and_product(self, result: Tuple[Sequence[Portfolio], Optional[Product]]):
        portfolios, product = result
        self._portfolios = [p for p in portfolios if p.id not in self._portfolio_black_list]
        self._product = product
        _enable_combo_box(self.ui.comboBox_portfolios, [p.name for p in self._portfolios])
        if product:
            self.ui.lineEdit_products.setText(product.name)
        self._check_form()

    @slot
    def _check_form(self, *_):
        account_text = self.ui.lineEdit_account.text()
        if not (
            self.ui.lineEdit_name.text() and
            account_text and
            self.ui.comboBox_broker.isEnabled() and
            self.ui.comboBox_assetUnits.currentIndex() >= 0 and
            self.ui.comboBox_portfolios.currentIndex() >= 0
        ):
            disable_widget(self.ui.pushButton_create, "请输入/选择所有字段")
        elif account_text in self._account_black_list:
            disable_widget(self.ui.pushButton_create, "资金账号重复")
        elif not re.match(r"^[0-9a-zA-Z]+$", account_text):
            disable_widget(self.ui.pushButton_create, "资金账号不合法")
        else:
            enabled_widget(self.ui.pushButton_create)

    @slot
    def _reset(self):
        self.setup(self._client, self._account_black_list, self._portfolio_black_list, self._asset_unit_black_list)
