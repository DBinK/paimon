# panel.py

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QMenu, QApplication
)

from PySide6.QtCore import Qt, QPoint, Slot
from PySide6.QtGui import QPainter, QColor

from paimon.schema import DataItem


class Panel(QWidget):

    def __init__(self):

        super().__init__()

        self.drag_pos = QPoint()

        self.labels = {}

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |     # 无边框
            Qt.WindowType.WindowStaysOnTopHint |    # 窗口置顶
            Qt.WindowType.Tool|                     # 让窗口不出现在任务栏 
            Qt.WindowType.WindowDoesNotAcceptFocus  # 不允许获取焦点
        )

        self._layout = QFormLayout()

        self._layout.setContentsMargins(6, 4, 6, 4)

        self._layout.setHorizontalSpacing(20)

        self._layout.setVerticalSpacing(2)

        self.setLayout(self._layout)

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setObjectName("panel")

        self.setStyleSheet("""
        #panel {
            background: rgba(30,30,30,120);
        }

        QLabel {
            background: transparent;
            color: white;
            font-family: "Cascadia Code", "Courier New", Courier, monospace;
        }
        """)

    # 绘制半透明背景
    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(30, 30, 30, 160)

        painter.setBrush(color)

        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRoundedRect(self.rect(), 4, 4)


    # 修改槽函数签名
    @Slot(list, dict)
    def update_data(self, ordered_keys: list, data: dict):
        # 先移除不再存在的项
        for key in list(self.labels.keys()):
            if key not in data:
                key_label, value_label = self.labels[key]
                self._layout.removeWidget(key_label)
                self._layout.removeWidget(value_label)
                key_label.deleteLater()
                value_label.deleteLater()
                del self.labels[key]

        # 按照 ordered_keys 的顺序添加或更新
        current_row = 0
        for key in ordered_keys:
            if key not in data:
                continue

            item: DataItem = data[key]
            if key not in self.labels:
                key_label = QLabel(str(key))
                value_label = QLabel(str(item.text))  # 注意：这里应使用 item.text
                key_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                value_label.setAlignment(Qt.AlignmentFlag.AlignRight)
                value_label.setStyleSheet(f"color: {item.color}")
                self.labels[key] = (key_label, value_label)
                # 插入到指定行
                self._layout.insertRow(current_row, key_label, value_label)
            else:
                key_label, value_label = self.labels[key]
                value_label.setText(item.text)
                value_label.setStyleSheet(f"color: {item.color}")

            current_row += 1

        self.adjustSize()
            

    # 拖动窗口
    def mousePressEvent(self, event):

        if event.button() == Qt.MouseButton.LeftButton:

            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):

        if event.buttons() == Qt.MouseButton.LeftButton:

            delta = event.globalPosition().toPoint() - self.drag_pos

            self.move(self.pos() + delta)

            self.drag_pos = event.globalPosition().toPoint()

    # 右键菜单
    def contextMenuEvent(self, event):

        menu = QMenu(self)

        exit_action = menu.addAction("退出")

        action = menu.exec(event.globalPos())

        if action == exit_action:

            QApplication.quit()