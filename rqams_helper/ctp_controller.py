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
from time import time
from functools import lru_cache
from datetime import datetime, date
from typing import NamedTuple, List, Dict, Tuple
from queue import Queue
from threading import Lock

from PySide2.QtCore import QObject, Signal, QTimer, Slot

from rqctp.trader_api import TraderApi
from rqctp.structs import ReqUserLogin, RspInfo, RspUserLogin, Trade as CtpTrade, ReqAuthenticate
from rqctp.consts import RESUME_TYPE, Direction, OffsetFlag

from rqams_client.models import Trade, Side

from rqams_helper.utils.slot import slot
from rqams_helper.utils.logger import logger
from rqams_helper.utils.thread import QueueConsumer


class CtpAccount(NamedTuple):
    fronts: List[str]
    broker_id: str
    account: str
    password: str
    user_product_info: str
    auth_code: str
    app_id: str


@lru_cache()
def is_future(symbol: str):
    if symbol is None:
        return False
    return re.match('^[a-zA-Z]+[0-9]+$', symbol) is not None


YEAR_UNIT_PLACE = date.today().year % 10
YEAR_TEN_PLACE = int(date.today().year % 100 / 10)


@lru_cache()
def make_order_book_id(symbol: str):
    if len(symbol) < 4:
        return None
    if symbol[-4] not in '0123456789':
        if int(symbol[-3]) < YEAR_UNIT_PLACE:
            order_book_id = symbol[:2] + str(YEAR_TEN_PLACE + 1) + symbol[-3:]
        else:
            order_book_id = symbol[:2] + str(YEAR_TEN_PLACE) + symbol[-3:]
    else:
        order_book_id = symbol
    return order_book_id.upper()


class CtpTraderApi(TraderApi):
    """
    NOT_INITED  →   LOGGED_IN
        ↓
    FAILED
    """
    CONNECT_STATE_OFF = -1
    CONNECT_STATE_ON = 1

    LOGIN_STATE_NOT_INITED = 0
    LOGIN_STATE_LOGGED_IN = 1
    LOGIN_STATE_FAILED = -1

    def __init__(self, account: CtpAccount, state_queue: Queue, trade_queue: Queue, init_msg="连接中"):
        super().__init__()

        self._account = account
        self._state_queue = state_queue
        self._trade_queue = trade_queue

        self._req_id = 0
        self._lock = Lock()

        self._err_msg = init_msg
        self._connect_state = self.CONNECT_STATE_OFF
        self._login_state = self.LOGIN_STATE_NOT_INITED

        self._update_state_info()

        self.need_re_login = False
        self.init_time = time()

        self.SubscribePrivateTopic(RESUME_TYPE.RESTART)
        self.SubscribePublicTopic(RESUME_TYPE.RESTART)
        for front in account.fronts:
            self.RegisterFront(front)
        self.Init()
        self._log_info("Init")

    @property
    def req_id(self):
        self._req_id += 1
        return self._req_id

    @property
    def is_connected(self):
        return self._connect_state == self.CONNECT_STATE_ON

    @property
    def state_info(self):
        return (self.is_connected and self._login_state == self.LOGIN_STATE_LOGGED_IN), self._err_msg

    def _log_info(self, msg: str):
        logger.info("{}__{}__{}: {}".format(
            self._account.account, self._connect_state, self._login_state, msg
        ))

    def OnFrontConnected(self):
        with self._lock:
            self._log_info("OnFrontConnected")
            self._connect_state = self.CONNECT_STATE_ON

            if self._login_state == self.LOGIN_STATE_NOT_INITED:
                if self._account.app_id and self._account.auth_code:
                    req = ReqAuthenticate(
                        BrokerID=self._account.broker_id,
                        UserID=self._account.account,
                        UserProductInfo=self._account.user_product_info or "",
                        AuthCode=self._account.auth_code,
                        AppID=self._account.app_id
                    )
                    result = self.ReqAuthenticate(req, self.req_id)
                    if result !=0:
                        self._err_msg = f"ReqAuthenticate failed: {result}"
                        self._login_state = self.LOGIN_STATE_FAILED

                else:
                    result = self.ReqUserLogin(ReqUserLogin(
                        BrokerID=self._account.broker_id,
                        UserID=self._account.account,
                        Password=self._account.password
                    ), self.req_id)
                    if result != 0:
                        self._err_msg = f"ReqUserLogin failed: {result}"
                        self._login_state = self.LOGIN_STATE_FAILED
            elif self._login_state == self.LOGIN_STATE_LOGGED_IN:
                self._err_msg = ""
            self._update_state_info()

    def OnRspAuthenticate(self, pRspAuthenticateField, pRspInfo, nRequestID, bIsLast):
        self._log_info(f"OnRspAuthenticate: {pRspInfo}")
        with self._lock:
            if pRspInfo.ErrorID == 0:
                req = ReqUserLogin(
                    BrokerID=self._account.broker_id,
                    UserID=self._account.account,
                    Password=self._account.password
                )
                result = self.ReqUserLogin(req, self.req_id)
                if result != 0:
                    self._err_msg = f"ReqUserLogin failed: {result}"
                    self._login_state = self.LOGIN_STATE_FAILED
            else:
                if pRspInfo.ErrorID in (7, 8):
                    self.need_re_login = True
                    self._err_msg = "{}: {}，稍后将尝试重新登录".format(pRspInfo.ErrorID, pRspInfo.ErrorMsg)
                else:
                    self._err_msg = "{}: {}".format(pRspInfo.ErrorID, pRspInfo.ErrorMsg)
                self._login_state = self.LOGIN_STATE_FAILED
            self._update_state_info()

    def OnRspUserLogin(self, pRspUserLogin: RspUserLogin, pRspInfo: RspInfo, nRequestID, bIsLast):
        self._log_info(f"OnRspUserLogin: {pRspInfo}")
        with self._lock:
            if self._login_state == self.LOGIN_STATE_NOT_INITED:
                if pRspInfo.ErrorID == 0:
                    self._err_msg = ""
                    self._login_state = self.LOGIN_STATE_LOGGED_IN
                else:
                    if pRspInfo.ErrorID in (7, 8):
                        self.need_re_login = True
                        self._err_msg = "{}: {}，稍后将尝试重新登录".format(pRspInfo.ErrorID, pRspInfo.ErrorMsg)
                    else:
                        self._err_msg = "{}: {}".format(pRspInfo.ErrorID, pRspInfo.ErrorMsg)
                    self._login_state = self.LOGIN_STATE_FAILED
            else:
                # TODO error log
                pass

            self._update_state_info()

    DISCONNECT_REASON = {
        0x1001: "网络读失败",
        0x1002: "网络写失败",
        0x2001: "接收心跳超时",
        0x2002: "发送心跳失败",
        0x2003: "收到错误报文"
    }

    def OnFrontDisconnected(self, nReason: int):
        self._log_info(f"OnFrontDisconnected: {nReason}")
        with self._lock:
            self._err_msg = self.DISCONNECT_REASON.get(nReason, "连接断开：{}".format(nReason))
            self._connect_state = self.CONNECT_STATE_OFF
            self._update_state_info()

    SIDE_MAP = {
        (Direction.Buy, OffsetFlag.Open): Side.BUY_OPEN,
        (Direction.Buy, OffsetFlag.Close): Side.BUY_CLOSE,
        (Direction.Buy, OffsetFlag.CloseYesterday): Side.BUY_CLOSE,
        (Direction.Buy, OffsetFlag.ForceClose): Side.BUY_CLOSE,
        (Direction.Buy, OffsetFlag.LocalForceClose): Side.BUY_CLOSE,
        (Direction.Buy, OffsetFlag.CloseToday): Side.BUY_CLOSE_TODAY,
    }

    def OnRtnTrade(self, pTrade: CtpTrade):
        if not is_future(pTrade.InstrumentID):
            return

        if pTrade.OffsetFlag == OffsetFlag.Open:
            side = Side.BUY_OPEN if pTrade.Direction == Direction.Buy else Side.SELL_OPEN
        elif pTrade.OffsetFlag == OffsetFlag.CloseToday:
            side = Side.BUY_CLOSE_TODAY if pTrade.Direction == Direction.Buy else Side.SELL_CLOSE_TODAY
        else:
            side = Side.BUY_CLOSE if pTrade.Direction == Direction.Buy else Side.SELL_CLOSE

        trade = Trade(
            exec_id=self._account.account.strip() + pTrade.TradeDate + pTrade.TradeID.strip() + pTrade.Direction,
            datetime=datetime.strptime(pTrade.TradeDate + "T" + pTrade.TradeTime, "%Y%m%dT%H:%M:%S"),
            order_book_id=make_order_book_id(pTrade.InstrumentID),
            side=side,
            last_quantity=pTrade.Volume,
            last_price=pTrade.Price,
            transaction_cost=0
        )
        self._trade_queue.put((self._account.account, trade))

    def _update_state_info(self):
        self._log_info(f"update state info: {self.state_info}")
        self._state_queue.put((self._account.account, *self.state_info))


class CtpController(QObject):
    update_state_info = Signal(str, bool, str)
    on_trades = Signal(list)

    def __init__(self):
        super(CtpController, self).__init__()
        self._api_pool: Dict[str, CtpTraderApi]= {}
        self._account_cache: Dict[str, CtpAccount] = {}
        self._state_queue = Queue()
        self._trade_queue = Queue()

        self._lock = Lock()

        self._timer = QTimer()
        self._timer.timeout.connect(self._on_timer)
        self._state_queue_consumer = QueueConsumer(self._state_queue)
        self._state_queue_consumer.on_result.connect(self._update_state_info)
        self._trade_queuq_consumer = QueueConsumer(self._trade_queue)
        self._trade_queuq_consumer.on_result.connect(self._on_trades)

    def connect_account(self, ctp_account: CtpAccount):
        logger.info(f"create account {ctp_account.account}")
        account = ctp_account.account
        with self._lock:
            self._account_cache[account] = ctp_account
            if account in self._api_pool:
                self.update_state_info.emit(account, *self._api_pool[account].state_info)
            else:
                self._api_pool[account] = CtpTraderApi(ctp_account, self._state_queue, self._trade_queue)

    def disconnect_account(self, account: str):
        logger.info(f"disconnect account {account}")
        with self._lock:
            if account in self._api_pool:
                self._api_pool.pop(account).Release()
            self.update_state_info.emit(account, False, "已断开")

    def run(self):
        self._timer.start(1000 * 20)
        self._state_queue_consumer.start()
        self._trade_queuq_consumer.start()

    def stop(self):
        self._state_queue_consumer.stop()
        self._trade_queuq_consumer.stop()

    @slot
    def _update_state_info(self, args_list):
        for account, connected, info in args_list:
            self.update_state_info.emit(account, connected, info)

    @slot
    def _on_timer(self):
        with self._lock:
            accounts_need_to_re_login = [account for account, api in self._api_pool.items() if api.need_re_login]
            for account in accounts_need_to_re_login:
                api = self._api_pool.pop(account)
                api.Release()
                self._api_pool[account] = CtpTraderApi(
                    self._account_cache[account], self._state_queue, self._trade_queue
                )

            current_time = time()
            current_time_str = datetime.fromtimestamp(current_time).strftime("%H:%M:%S")
            timeout_accounts = [
                account for account, api in self._api_pool.items() if (
                    not api.is_connected and current_time - api.init_time > 30
                )
            ]
            for account in timeout_accounts:
                api = self._api_pool.pop(account)
                api.Release()
                self._api_pool[account] = CtpTraderApi(
                    self._account_cache[account], self._state_queue, self._trade_queue,
                    init_msg=f"连接超时，于 {current_time_str} 尝试重新连接"
                )

    @slot
    def _on_trades(self, trades: List[Tuple[str, Trade]]):
        self.on_trades.emit(trades)
