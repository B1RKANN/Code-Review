"""Sağ alt köşe toast bildirimleri — auto-dismiss."""
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QPoint
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QLabel

from theme import C
from icons import make_icon


class _Toast(QFrame):
    def __init__(self, title: str, desc: str, kind: str, parent=None):
        super().__init__(parent)
        obj = {"good":"toastGood","warn":"toastWarn"}.get(kind, "toast")
        self.setObjectName(obj)
        bl = {"good":C.GOOD,"warn":C.WARN}.get(kind, C.ACCENT)
        self.setStyleSheet(
            f"QFrame {{ background:{C.BG_2}; border:1px solid {C.BORDER}; "
            f"border-left:3px solid {bl}; border-radius:8px; }}"
        )
        self.setFixedWidth(280)

        lay = QHBoxLayout(self); lay.setContentsMargins(12, 10, 14, 10); lay.setSpacing(10)
        ico = QLabel()
        ico_name = "check" if kind == "good" else "bug" if kind == "warn" else "sparkle"
        ico.setPixmap(make_icon(ico_name, bl, 16, stroke_w=2.2).pixmap(16, 16))
        lay.addWidget(ico, 0, Qt.AlignmentFlag.AlignTop)

        text = QVBoxLayout(); text.setSpacing(2)
        t = QLabel(title); t.setObjectName("toastTitle")
        t.setStyleSheet(f"color:{C.TEXT_1}; font-size:12px; font-weight:600; background:transparent; border:none;")
        text.addWidget(t)
        if desc:
            d = QLabel(desc); d.setObjectName("toastDesc")
            d.setStyleSheet(f"color:{C.TEXT_3}; font-size:11px; background:transparent; border:none;")
            d.setWordWrap(True)
            text.addWidget(d)
        lay.addLayout(text, 1)


class ToastManager:
    def __init__(self, host_window):
        self.host = host_window
        self.toasts = []  # list of (frame, timer)

    def push(self, title: str, desc: str = "", kind: str = "info"):
        t = _Toast(title, desc, kind, parent=self.host)
        t.show()
        t.adjustSize()
        self.toasts.append(t)
        self._reposition()

        # Slide-in
        anim = QPropertyAnimation(t, b"pos")
        anim.setDuration(220)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        end = t.pos()
        anim.setStartValue(QPoint(end.x() + 30, end.y()))
        anim.setEndValue(end)
        anim.start()
        t._anim = anim

        QTimer.singleShot(3800, lambda: self._dismiss(t))

    def _dismiss(self, t):
        if t in self.toasts:
            self.toasts.remove(t)
        t.deleteLater()
        self._reposition()

    def _reposition(self):
        host_rect = self.host.geometry()
        margin = 16
        y = self.host.height() - 36 - margin  # above status bar
        for t in reversed(self.toasts):
            y -= t.height() + 8
            x = self.host.width() - t.width() - margin
            t.move(x, y)
