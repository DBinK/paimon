# data.py

from PySide6.QtCore import QObject, Signal, QTimer

from paimon.schema import DataItem

from paimon.config import load_config
from paimon.network import run_probe

class DataSource(QObject):
  
    data_updated = Signal(dict)  # 数据更新信号

    def __init__(self):

        super().__init__()

        self.data = {}

        self.config: dict = load_config()
        self.probes: list[dict] = self.config["probes"]
        interval: int = self.config.get("interval", 2)

        # 定时更新
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_data)
        self.timer.start(interval * 1000)

    def _update_data(self):

        for p in self.probes:

            r = run_probe(p)

            label = p.get("label", p["name"])

            item = DataItem(
                r.text(),
                r.color()
            )
            self.data[label] = item

        self.data_updated.emit(self.data)