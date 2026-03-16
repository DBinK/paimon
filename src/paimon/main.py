# main.py

import sys

from PySide6.QtWidgets import QApplication

from paimon.panel import Panel
from paimon.data import DataSource


def main():

    app = QApplication(sys.argv)

    # 创建UI
    panel = Panel()

    panel.show()

    # 创建数据源
    data_source = DataSource()

    # 连接信号
    data_source.data_updated.connect(panel.update_data)

    sys.exit(app.exec())


if __name__ == "__main__":

    main()