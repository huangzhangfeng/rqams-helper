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

from queue import Queue, Empty

from PySide2.QtCore import QObject, Signal, Slot, QThread

from rqams_helper.utils.logger import logger
from rqams_helper.utils.exceptions import RQAmsHelperException
from rqams_helper.utils.exceptions import convert_exception


class QueueConsumerWorker(QObject):
    finished = Signal()
    on_result = Signal(object)
    error = Signal(object)

    def __init__(self, queue: Queue):
        super(QueueConsumerWorker, self).__init__()
        self._queue = queue
        self._running = True

    @Slot()
    def run(self):

        @convert_exception
        def _run():
            while self._running:
                try:
                    msgs = [self._queue.get(timeout=1)]
                except Empty:
                    continue
                while True:
                    try:
                        msgs.append(self._queue.get_nowait())
                    except Empty:
                        break
                self.on_result.emit(msgs)

        try:
            _run()
        except Exception as e:
            self.error.emit(e)
        finally:
            self.finished.emit()

    def stop(self):
        self._running = False


class QueueConsumer(QObject):
    on_result = Signal(object)

    def __init__(self, queue: Queue):
        super(QueueConsumer, self).__init__()
        self._queue = queue
        self._worker = None
        self._thread: QThread = None

    def start(self):
        self._worker = QueueConsumerWorker(self._queue)
        self._thread = QThread()
        self._worker.moveToThread(self._thread)
        self._worker.finished.connect(self._thread.quit)
        self._worker.error.connect(self._handle_exception)
        self._worker.on_result.connect(self._on_result)
        self._thread.started.connect(self._worker.run)
        self._thread.start()

    def stop(self):
        if not (self._worker and self._thread):
            raise RuntimeError("not started yet")
        self._worker.stop()
        if self._thread.isRunning():
            self._thread.quit()
            self._thread.wait()

    @Slot()
    def _handle_exception(self, e):
        if isinstance(e, RQAmsHelperException):
            e.exec_msg_box()
        else:
            logger.error("consumer failed: " + str(e))
        logger.info("restart consumer")
        self.stop()
        self.start()

    @Slot()
    def _on_result(self, result):
        self.on_result.emit(result)
