# panel.py

from PySide6.QtWidgets import (
    QWidget, QFormLayout, QLabel, QMenu, QApplication
)

from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QPainter, QColor


class Panel(QWidget):

    def __init__(self, data_dict):
        super().__init__()

        self.data = data_dict
        self.drag_pos = QPoint()
        self.labels = {}

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
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
        }
        """)

        # 定时刷新UI
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(500)

        self.refresh()

    # 绘制半透明背景
    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        color = QColor(30, 30, 30, 160)

        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawRoundedRect(self.rect(), 4, 4)

    def refresh(self):

        for k, v in self.data.items():

            if k not in self.labels:

                key_label = QLabel(str(k))
                value_label = QLabel(str(v))

                key_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                value_label.setAlignment(Qt.AlignmentFlag.AlignRight)

                self._layout.addRow(key_label, value_label)

                self.labels[k] = (key_label, value_label)

                self.adjustSize()

            else:

                key_label, value_label = self.labels[k]
                value_label.setText(str(v))

        for k in list(self.labels.keys()):

            if k not in self.data:

                key_label, value_label = self.labels[k]

                self._layout.removeWidget(key_label)
                self._layout.removeWidget(value_label)

                key_label.deleteLater()
                value_label.deleteLater()

                del self.labels[k]

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