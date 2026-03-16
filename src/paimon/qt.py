import sys
from PySide6.QtWidgets import (
    QApplication, QSizePolicy, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem,
    QAbstractItemView, QMenu, QHeaderView
)
from PySide6.QtCore import Qt, QPoint, QEvent


class Panel(QWidget):

    def __init__(self):
        super().__init__()

        self.drag_pos = QPoint()

        # 无边框 + 置顶
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )

        layout = QVBoxLayout()
        layout.setContentsMargins(2, 2, 2, 2)  # 紧凑一点

        data = [
            ("server1", "23 ms"),
            ("server2", "51 ms"),
            ("server3", "12 ms"),
        ]

        table = QTableWidget()
        table.setColumnCount(2)
        # table.setHorizontalHeaderLabels(["名称", "延迟"])
        table.horizontalHeader().setVisible(False)
        table.setRowCount(len(data))

        # 表格根据内容调整大小
        table.setSizeAdjustPolicy(QTableWidget.SizeAdjustPolicy.AdjustToContents)

        # 不要自动扩展
        table.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        
        # 表格优化
        table.setShowGrid(False)  # 去掉表格线
        table.verticalHeader().setVisible(False)  # 去掉列头
        table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # 禁止编辑
        # table.horizontalHeader().setStretchLastSection(True)  # 最后一列填满
        table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        # 优化1：去掉焦点框
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # 优化2：行高更紧凑
        table.verticalHeader().setDefaultSectionSize(18)

        # 填充数据
        for i, (name, delay) in enumerate(data):
            table.setItem(i, 0, QTableWidgetItem(name))
            table.setItem(i, 1, QTableWidgetItem(delay))

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        layout.addWidget(table)

        self.setLayout(layout)

        self.adjustSize()
        # self.resize(200, 120)


        # 透明背景
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("""
            background: rgba(30,30,30,10);
            color: white;
        """)

        # 关键：安装事件过滤器（解决拖动问题）
        # table.installEventFilter(self)
        table.viewport().installEventFilter(self)

    # 事件过滤器（处理拖动）
    def eventFilter(self, obj, event):

        if event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag_pos = event.globalPosition().toPoint()

        if event.type() == QEvent.Type.MouseMove:
            if event.buttons() == Qt.MouseButton.LeftButton:
                delta = event.globalPosition().toPoint() - self.drag_pos
                self.move(self.pos() + delta)
                self.drag_pos = event.globalPosition().toPoint()

        return super().eventFilter(obj, event)

    # 右键菜单
    def contextMenuEvent(self, event):

        menu = QMenu(self)
        exit_action = menu.addAction("退出")

        action = menu.exec(event.globalPos())

        if action == exit_action:
            QApplication.quit()


app = QApplication(sys.argv)

window = Panel()
window.show()

sys.exit(app.exec())