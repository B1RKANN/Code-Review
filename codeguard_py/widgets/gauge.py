"""Animasyonlu dairesel gauge widget'ı."""
from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QEasingCurve, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QFont, QFontMetrics
from PyQt6.QtWidgets import QWidget

from theme import C, color_for_score


class Gauge(QWidget):
    """Dairesel skor göstergesi. setValue() ile animasyonla yeni değere geçer."""

    def __init__(self, value: int = 0, size: int = 120, label: str = "skor", parent=None):
        super().__init__(parent)
        self._value = 0.0
        self._target = value
        self._label = label
        self._size = size
        self.setFixedSize(size, size)
        self._anim = QPropertyAnimation(self, b"animValue")
        self._anim.setDuration(1400)
        self._anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.set_target(value, animate=True)

    def set_label(self, text: str):
        self._label = text
        self.update()

    def set_target(self, value: int, animate: bool = True):
        self._target = max(0, min(100, value))
        if animate:
            self._anim.stop()
            self._anim.setStartValue(0.0)
            self._anim.setEndValue(float(self._target))
            self._anim.start()
        else:
            self._value = float(self._target)
            self.update()

    def replay(self):
        self.set_target(self._target, animate=True)

    @pyqtProperty(float)
    def animValue(self):
        return self._value

    @animValue.setter
    def animValue(self, v):
        self._value = v
        self.update()

    def paintEvent(self, _):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = self.rect()
        size = min(rect.width(), rect.height())
        margin = 10
        ring_rect = QRectF(margin, margin, size - 2 * margin, size - 2 * margin)

        stroke = 10

        # Track
        pen = QPen(QColor(C.BG_3), stroke, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        p.drawArc(ring_rect, 0, 360 * 16)

        # Arc
        color = QColor(color_for_score(int(self._target)))
        pen = QPen(color, stroke, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
        p.setPen(pen)
        # 90° (top) start, span = -value/100*360 (clockwise)
        start_angle = 90 * 16
        span = int(-(self._value / 100.0) * 360 * 16)
        p.drawArc(ring_rect, start_angle, span)

        # Center text
        big = QFont("JetBrains Mono", int(size * 0.18))
        big.setWeight(QFont.Weight.Bold)
        small = QFont("JetBrains Mono", max(7, int(size * 0.07)))

        p.setPen(QColor(C.TEXT_1))
        p.setFont(big)
        num_txt = str(int(round(self._value)))
        fm = QFontMetrics(big)
        num_w = fm.horizontalAdvance(num_txt)
        num_h = fm.height()
        cx = size / 2
        cy = size / 2
        p.drawText(int(cx - num_w / 2), int(cy + num_h / 4), num_txt)

        p.setPen(QColor(C.TEXT_3))
        p.setFont(small)
        fm2 = QFontMetrics(small)
        lbl_w = fm2.horizontalAdvance(self._label)
        p.drawText(int(cx - lbl_w / 2), int(cy + num_h / 4 + fm2.height() + 2), self._label)
