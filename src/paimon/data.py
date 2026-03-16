# data.py

import random

from PySide6.QtCore import QObject, Signal, QTimer

from paimon.schema import DataItem


class DataSource(QObject):
    # 数据更新信号
    data_updated = Signal(dict)

    def __init__(self):

        super().__init__()

        self.data = {
            "server1": DataItem("10 ms"),
            "server2": DataItem("20 ms"),
            "server3": DataItem("30 ms"),
            "uptime": DataItem("1d 1h 1m 1s")
        }

        # 定时更新
        self.timer = QTimer()

        self.timer.timeout.connect(self._update_data)

        self.timer.start(1000)

    def _update_data(self):

        ping = random.randint(10,100)

        if ping < 40:
            color = "green"
        elif ping < 70:
            color = "orange"
        else:
            color = "red"

        self.data["server1"] = DataItem(f"{ping} ms", color)

        cpu = random.randint(0,100)

        cpu_color = "green" if cpu < 70 else "red"

        self.data["cpu"] = DataItem(f"{cpu} %", cpu_color)

        self.data_updated.emit(self.data)