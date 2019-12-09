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

from functools import wraps
from traceback import format_exc

from requests.exceptions import Timeout, ConnectionError
from PySide2.QtWidgets import QMessageBox

from rqams_client.utils import ReqestException
from rqams_helper.utils.widgets import MessageBox, DetailMessageBox
from rqams_helper.utils.logger import logger


class RQAmsHelperException(Exception):
    def __init__(self, msg, title=None, detail=None):
        super(RQAmsHelperException, self).__init__(msg)
        self.msg = msg
        self.title = title or msg
        self.detail = detail

    def _msg_box(self):
        if self.detail:
            return DetailMessageBox(QMessageBox.Warning, self.title, self.msg, self.detail)
        else:
            return MessageBox(QMessageBox.Warning, self.title, self.msg)

    def exec_msg_box(self):
        self._msg_box().exec_()


class LoginExpiredException(RQAmsHelperException):
    after_msg_box_slot = None

    def __init__(self):
        super(LoginExpiredException, self).__init__("登录过期，请重新登录", "登录过期")

    def exec_msg_box(self):
        msg_box = self._msg_box()
        msg_box.exec_()
        self.after_msg_box_slot()


def convert_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ConnectionError, Timeout):
            logger.error(format_exc())
            raise RQAmsHelperException("与服务器通信失败，请检查网络连接或联系 Ricequant", "网络连接异常", format_exc())
        except ReqestException as e:
            if e.response.status_code == 401:
                raise LoginExpiredException()
            else:
                logger.error(format_exc())
                raise RQAmsHelperException("RQAms 助手运行遇到异常，请重试或联系 Ricequant", "错误", format_exc())
        except Exception as e:
            logger.error(format_exc())
            if not isinstance(e, RQAmsHelperException):
                raise RQAmsHelperException("RQAms 助手运行遇到异常，请重试或联系 Ricequant", "错误", format_exc())
            raise
    return wrapper