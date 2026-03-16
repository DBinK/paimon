from PySide6.QtCore import QObject, Signal, QTimer, QRunnable, QThreadPool

from paimon.schema import DataItem
from paimon.config import load_config
from paimon.network import run_probe


class ProbeWorker(QRunnable):
    """
    单个 probe 任务
    """

    def __init__(self, probe: dict, callback):
        super().__init__()

        self.probe = probe
        self.callback = callback

    def run(self):

        r = run_probe(self.probe)

        label = self.probe.get("label")

        item = DataItem(
            r.text(),
            r.color()
        )

        self.callback(self.probe, label, item)  # 传递 probe 信息


class DataSource(QObject):

    data_updated = Signal(list, dict)  # (ordered_keys, data_dict) 同时传递顺序和数据

    def __init__(self):
        super().__init__()

        self.config: dict = load_config()
        self.probes: list[dict] = self.config["probes"]
     
        self.data = {}
        self.ordered_keys = []  # 显式保存顺序
        for probe in self.probes:
            label = probe.get("label")
            self.ordered_keys.append(label)
            self.data[label] = DataItem("...", "gray") 
        
        # 发送初始状态
        self.data_updated.emit(self.ordered_keys, self.data)

        interval: int = self.config.get("interval", 1)
        self.pool = QThreadPool()
        self.pool.setMaxThreadCount(10)
        self.pending = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_data)
        self.timer.start(interval * 1000)

    def _update_data(self):

        if self.pending != 0:
            return

        self.pending = len(self.probes)

        for p in self.probes:

            worker = ProbeWorker(
                p,
                self._probe_done
            )

            self.pool.start(worker)

    def _probe_done(self, probe, label, item):

        # 直接更新对应键的值
        self.data[label] = item

        self.pending -= 1

        if self.pending == 0:
        
            self.data_updated.emit(self.ordered_keys, self.data)