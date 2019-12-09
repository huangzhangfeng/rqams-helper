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

from typing import Sequence

from PySide2.QtWidgets import QMainWindow
from PySide2.QtCore import Signal, Qt

from rqams_client.models import Portfolio, Account

from rqams_helper.utils.slot import slot
from rqams_helper.utils.widgets import disable_widget, enabled_widget, MessageBox
from rqams_helper.utils.future import Future
from .ui.modifyAccountWindow import Ui_modifyAccountWindow
from .resources import get_icon


def _set_portfolio(account: Account, portfolio: Portfolio):
    account.portfolio = portfolio


class ModifyAccountWindow(QMainWindow):
    account_modified = Signal(str, Portfolio)

    def __init__(self):
        super(ModifyAccountWindow, self).__init__(None, Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.ui = Ui_modifyAccountWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_done.clicked.connect(self._on_done_button_clicked)
        self.ui.pushButton_reset.clicked.connect(self._on_reset_button_clicked)

        self.setWindowIcon(get_icon())

        self._account = None
        self._portfolios = None

    def setup(self, account: Account):
        self._account = account
        self.ui.label_name.setText(account.name)
        self.ui.label_broker.setText(account.broker.name)
        self.ui.label_account.setText(account.account)
        self.ui.label_assetUnit.setText(account.asset_unit.name)
        disable_widget(self.ui.comboBox_portfolios, "请选择组合")
        self.ui.comboBox_portfolios.clear()
        Future(self, lambda: list(account.asset_unit.portfolios.values()), callback=self._update_portfolios).run()

    def _update_portfolios(self, portfolios: Sequence[Portfolio]):
        self._portfolios = portfolios
        self.ui.comboBox_portfolios.addItems([p.name for p in portfolios])
        for index, portfolio in enumerate(portfolios):
            if self._account.portfolio == portfolio:
                self.ui.comboBox_portfolios.setCurrentIndex(index)
                break
        else:
            MessageBox(
                MessageBox.Warning, "组合数据异常",
                "资金账户当前绑定的组合\"{}\"已和资产单元\"{}\"接触绑定，请重新为资金账号绑定组合".format(
                    self._account.portfolio.name, self._account.asset_unit.name
                )
            ).exec_()
        enabled_widget(self.ui.comboBox_portfolios)

    @slot
    def _on_done_button_clicked(self):
        portfolio = self._portfolios[self.ui.comboBox_portfolios.currentIndex()]
        self.account_modified.emit(self._account.account, portfolio)
        Future(self, _set_portfolio, (self._account, portfolio)).run()

    @slot
    def _on_reset_button_clicked(self):
        self.setup(self._account)
