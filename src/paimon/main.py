# main.py

import sys

from PySide6.QtWidgets import QApplication

from paimon.panel import Panel
from paimon.data import DataSource


def main():

    app = QApplication(sys.argv)

    # 创建数据源
    data_source = DataSource()

    # 创建UI
    window = Panel(data_source.get_data())

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()