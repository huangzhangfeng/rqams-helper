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
import pickle
from typing import Tuple, Iterable, List
from operator import itemgetter
from datetime import datetime, date, timedelta
import sqlite3

from win32crypt import CryptProtectData, CryptUnprotectData
import pywintypes


def adapt_datetime(dt: datetime):
    return dt.microsecond


class Persister:
    DIR = os.path.join(os.path.expanduser("~"), ".rqams-helper")

    LOGIN_DIR = os.path.join(DIR, "login.pkl")
    KEY_DIR = os.path.join(DIR, "")
    DB_DIR = os.path.join(os.path.join(DIR, "rqams-helper.db"))

    def __init__(self):
        if not os.path.exists(self.DIR):
            os.mkdir(self.DIR)

        self._conn = sqlite3.connect(self.DB_DIR)
        self._conn.row_factory = sqlite3.Row
        self._conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS password
                (
                    type text default ctp,
                    user_id int,
                    account text,
                    password blob,
                    constraint password_pk primary key (user_id, account, type)
                );
        """)
        self._conn.cursor().execute("""
            CREATE TABLE IF NOT EXISTS "trades"
            (
                exec_id text,
                date int,
                constraint trades_pk primary key (exec_id)
            );
        """)
        self._clear()

    def get_last_login(self) -> Tuple[str, int, str]:
        if os.path.exists(self.LOGIN_DIR):
            with open(self.LOGIN_DIR, "rb") as f:
                return itemgetter("username", "user_id", "sid")(pickle.loads(f.read()))

    def login(self, username: str, user_id: int, sid: str, save: bool):
        if not save:
            self.logout()
        else:
            with open(self.LOGIN_DIR, "wb") as f:
                f.write(pickle.dumps({
                    "username": username,
                    "user_id": user_id,
                    "sid": sid
                }))

    def logout(self):
        if os.path.exists(self.LOGIN_DIR):
            os.remove(self.LOGIN_DIR)

    def save_password(self, user_id: int, account: str, password: str):
        password_blob = CryptProtectData(
            password.encode("utf-8"),
            OptionalEntropy=(str(user_id) + account).encode("utf-8")
        )
        self._conn.cursor().execute(
            "INSERT OR REPLACE INTO password (type, user_id, account, password) VALUES (?, ?, ?, ?)",
            ("ctp", user_id, account, password_blob)
        )
        self._conn.commit()

    def clear_password(self, user_id: int, accounts: List[str]):
        accounts_len = len(accounts)
        if accounts_len <= 0:
            return
        elif accounts_len == 1:
            self._conn.cursor().execute("DELETE FROM password WHERE user_id=? AND account=?", (user_id, accounts[0]))
        else:
            self._conn.cursor().execute(
                "DELETE FROM password WHERE user_id=? AND account IN ({})".format(",".join("?" * accounts_len)),
                [user_id] + accounts
            )
        self._conn.commit()

    def get_password(self, user_id: int, account: str):
        cur = self._conn.cursor()
        cur.execute(
            "SELECT password FROM password WHERE user_id=? AND account=? AND type=?",
            (user_id, account, "ctp")
        )
        result = cur.fetchone()
        if result:
            try:
                return CryptUnprotectData(result["password"], (str(user_id) + account).encode("utf-8"))[1].decode("utf-8")
            except pywintypes.error:
                from traceback import format_exc
                print(format_exc())
                return

    def get_uploaded_exec_ids(self):
        cur = self._conn.cursor()
        cur.execute("select exec_id from trades")
        return [r["exec_id"] for r in cur.fetchall()]

    def save_upload_exec_id(self, exec_ids: Iterable[str]):
        today = date.today()
        cur = self._conn.cursor()
        for exec_id in exec_ids:
            cur.execute(
                "INSERT OR REPLACE INTO trades (exec_id, date) values (?, ?)",
                (exec_id, today.day + today.month * 100 + today.year * 10000)
            )
        self._conn.commit()

    def _clear(self):
        dt = date.today() - timedelta(3)
        cur = self._conn.cursor()
        cur.execute("DELETE FROM trades WHERE date < ?", (dt.month * 100 + dt.year * 10000, ))
