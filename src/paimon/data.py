# data.py

import random
from PySide6.QtCore import QTimer


class DataSource:
    def __init__(self):
        
        # 数据字典
        self.data = {}

        # 定时更新
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)

    def update_data(self):
        """
        模拟外部数据更新
        """
        self.data["server1"] = f"{random.randint(10,100)} ms"
        self.data["cpu"] = f"{random.randint(0,100)} %"

    def get_data(self):
        """
        返回数据
        """

        return self.data