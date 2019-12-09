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
import sys
from typing import Set, List, Tuple, Optional, Dict
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import QObject, Signal, QCoreApplication, Qt

from rqams_client.client import RQAMSClient
from rqams_client.models import Account, Trade, Portfolio
from rqams_client.utils import ReqestException

from rqams_helper.windows import LoginWindow, MainWindow, CreateAccountWindow, ModifyAccountWindow
from rqams_helper.utils.slot import slot
from rqams_helper.utils.logger import logger
from rqams_helper.utils.exceptions import RQAmsHelperException, LoginExpiredException
from rqams_helper.ctp_controller import CtpController, CtpAccount
from rqams_helper.persister import Persister


class RQAmsHelper(QObject):
    login = Signal(RQAMSClient)
    logout = Signal()

    def __init__(self):
        # TODO: 上传结算单
        logger.info("start")

        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

        super(RQAmsHelper, self).__init__()

        self._ctp_controller = CtpController()
        self._ctp_controller.update_state_info.connect(self._update_account_state_info)
        self._ctp_controller.on_trades.connect(self._on_trades)
        self._persister = Persister()

        self._app = QApplication()
        self._main_window = MainWindow(self._persister)
        self._login_window = LoginWindow()
        self._create_account_window = CreateAccountWindow()
        self._modify_account_window = ModifyAccountWindow()

        self._login_window.login.connect(self._login)
        self._main_window.logout_button_pushed.connect(self._switch_to_login_window)
        self._main_window.create_button_pushed.connect(self._open_create_account_window)
        self._main_window.modify_button_pushed.connect(self._open_modify_account_window)
        self._main_window.connect_account.connect(self._connect_account)
        self._main_window.disconnect_account.connect(self._disconnect_account)
        self._modify_account_window.account_modified.connect(self._account_modified)
        self._create_account_window.account_created.connect(self._account_created)
        self._server_url = os.environ.get("RQAMS_URL", "https://www.ricequant.com")

        self._uploaded_exec_ids = set(self._persister.get_uploaded_exec_ids())

        LoginExpiredException.after_msg_box_slot = self._switch_to_login_window

    @slot
    def _login(self, username: str, password: str, auto_login: bool):
        try:
            client = RQAMSClient(
                username=username, password=password, remember_me=auto_login, server_url=self._server_url, logger=logger
            )
        except ReqestException as e:
            if e.response.status_code == 403:
                raise RQAmsHelperException("用户名或密码错误", "登录失败")
            raise
        self._persister.login(username, client.user_id, client.sid, auto_login)
        self._main_window.setup(client, username, client.user_id)
        self._main_window.show()
        self._login_window.close()

    @slot
    def _switch_to_login_window(self):
        if self._main_window.close():
            self._persister.logout()
            self._login_window.setup()
            self._login_window.show()
            self._create_account_window.close()

    @slot
    def _open_create_account_window(
            self, client: RQAMSClient, account_black_list: Set[str], portfolio_black_list: Set[str],
            asset_unit_black_list: Set[str]
    ):
        self._create_account_window.setup(client, account_black_list, portfolio_black_list, asset_unit_black_list)
        self._create_account_window.show()

    @slot
    def _open_modify_account_window(self, account: Account):
        self._modify_account_window.setup(account)
        self._modify_account_window.show()

    @slot
    def _account_created(self, account: Account):
        self._main_window.create_account(account)
        self._create_account_window.close()

    @slot
    def _account_modified(self, account: str, portfolio: Portfolio):
        self._main_window.modify_account(account, portfolio)
        self._modify_account_window.close()

    @slot
    def _connect_account(self, ctp_account: CtpAccount):
        self._create_account_window.close()
        self._ctp_controller.connect_account(ctp_account)

    @slot
    def _disconnect_account(self, account: str):
        self._ctp_controller.disconnect_account(account)
    
    @slot
    def _update_account_state_info(self, account: str, connected: bool, info: str):
        self._main_window.update_account_state_info(account, connected, info)

    @slot
    def _on_trades(self, trades: List[Tuple[str, Trade]]):
        trade_dicts = {}
        exec_ids = set()
        for account, trade in trades:
            if trade.exec_id in self._uploaded_exec_ids:
                continue
            trade_dicts.setdefault(account, {})[trade.exec_id] = trade
            exec_ids.add(trade.exec_id)

        for account, trade_dict in trade_dicts.items():
            current_accounts = self._main_window.current_accounts
            if account in current_accounts:
                current_accounts[account].portfolio.trades.update(trade_dict)
                logger.info(f"trades pushed: {trade_dict}")
        self._persister.save_upload_exec_id(exec_ids)
        self._uploaded_exec_ids.update(exec_ids)

    def run(self):
        def _login():
            self._login_window.setup()
            self._login_window.show()

        self._ctp_controller.run()

        last_login = self._persister.get_last_login()
        if not last_login:
            _login()
        else:
            username, user_id, sid = last_login
            client = RQAMSClient(sid=sid, server_url=self._server_url, logger=logger)
            self._main_window.setup(client, username, user_id)
            self._main_window.show()

        code = self._app.exec_()
        self._ctp_controller.stop()
        sys.exit(code)


if __name__ == "__main__":
    RQAmsHelper().run()
