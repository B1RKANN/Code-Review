"""Üst bar — logo, breadcrumb, panel toggle, terminal, komut paleti."""
import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy,
)

from theme import C
from icons import make_icon


def _vline() -> QFrame:
    f = QFrame()
    f.setFrameShape(QFrame.Shape.VLine)
    f.setFixedWidth(1)
    f.setStyleSheet(f"background:{C.BORDER}; margin:7px 3px;")
    return f


class TitleBar(QFrame):
    cmdk_requested = pyqtSignal()
    close_folder_requested = pyqtSignal()
    open_terminal_requested = pyqtSignal()
    toggle_sidebar_requested = pyqtSignal()
    toggle_chat_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("titlebar")
        self.setFixedHeight(40)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 0, 8, 0)
        lay.setSpacing(4)

        # ── Sol: logo + marka ──
        logo = QLabel()
        logo.setFixedSize(20, 20)
        logo.setPixmap(make_icon("shield", C.ACCENT, 20, 2.0).pixmap(20, 20))
        brand = QLabel("CodeGuard")
        brand.setObjectName("brandLabel")
        lay.addWidget(logo)
        lay.addWidget(brand)
        lay.addSpacing(10)

        # ── Breadcrumb ──
        self._bc_layout = QHBoxLayout()
        self._bc_layout.setSpacing(2)
        self._bc_layout.setContentsMargins(0, 0, 0, 0)
        bc_wrap = QFrame()
        bc_wrap.setLayout(self._bc_layout)
        lay.addWidget(bc_wrap)

        lay.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        # ── Sağ: aksiyon grubu 1 — panel toggle ──
        self._btn_sidebar = self._icon_btn("sidebarL", "Kenar Çubuğunu Aç/Kapat  Ctrl+B")
        self._btn_sidebar.clicked.connect(self.toggle_sidebar_requested.emit)
        lay.addWidget(self._btn_sidebar)

        self._btn_chat = self._icon_btn("sidebarR", "Chat Panelini Aç/Kapat  Ctrl+J")
        self._btn_chat.clicked.connect(self.toggle_chat_requested.emit)
        lay.addWidget(self._btn_chat)

        lay.addWidget(_vline())

        # ── Aksiyon grubu 2 — terminal + kapat ──
        btn_terminal = self._icon_btn("terminal", "Terminal Aç")
        btn_terminal.clicked.connect(self.open_terminal_requested.emit)
        lay.addWidget(btn_terminal)

        btn_close = self._icon_btn("folderUp", "Klasörü Kapat")
        btn_close.clicked.connect(self.close_folder_requested.emit)
        lay.addWidget(btn_close)

        lay.addWidget(_vline())

        # ── Ctrl+K ──
        self.cmdk_btn = QPushButton("  Ara…          Ctrl+K")
        self.cmdk_btn.setObjectName("cmdkBtn")
        self.cmdk_btn.setIcon(make_icon("search", C.TEXT_3, 12))
        self.cmdk_btn.setMinimumWidth(200)
        self.cmdk_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.cmdk_btn.clicked.connect(self.cmdk_requested.emit)
        lay.addWidget(self.cmdk_btn)

        lay.addWidget(_vline())

        # ── Git + bildirim + ayar ──
        for ico, tip in (("branch", "Git Dalı"), ("bell", "Bildirimler"), ("settings", "Ayarlar")):
            lay.addWidget(self._icon_btn(ico, tip))

    # ---------- Yardımcı ----------

    def _icon_btn(self, icon: str, tooltip: str = "") -> QPushButton:
        b = QPushButton()
        b.setObjectName("tbIconBtn")
        b.setIcon(make_icon(icon, C.TEXT_3, 14))
        b.setFixedSize(28, 28)
        b.setCursor(Qt.CursorShape.PointingHandCursor)
        if tooltip:
            b.setToolTip(tooltip)
        return b

    def set_breadcrumb(self, path: str, project_name: str = ""):
        while self._bc_layout.count():
            item = self._bc_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        if not path:
            return

        if os.path.isabs(path):
            fname = os.path.basename(path)
            segs = [project_name, fname] if project_name and project_name != fname else [fname]
        else:
            parts = [s for s in path.split("/") if s]
            segs = ([project_name] if project_name else []) + parts

        for i, s in enumerate(segs):
            if i > 0:
                sep = QLabel("/")
                sep.setObjectName("bcSep")
                self._bc_layout.addWidget(sep)
            lbl = QLabel(s)
            lbl.setObjectName("bcSegActive" if i == len(segs) - 1 else "bcSeg")
            self._bc_layout.addWidget(lbl)

    def set_sidebar_active(self, hidden: bool):
        self._btn_sidebar.setObjectName("tbIconBtnActive" if hidden else "tbIconBtn")
        self._btn_sidebar.setIcon(make_icon(
            "sidebarL",
            C.ACCENT if hidden else C.TEXT_3, 14
        ))
        self._btn_sidebar.style().unpolish(self._btn_sidebar)
        self._btn_sidebar.style().polish(self._btn_sidebar)

    def set_chat_active(self, hidden: bool):
        self._btn_chat.setObjectName("tbIconBtnActive" if hidden else "tbIconBtn")
        self._btn_chat.setIcon(make_icon(
            "sidebarR",
            C.ACCENT if hidden else C.TEXT_3, 14
        ))
        self._btn_chat.style().unpolish(self._btn_chat)
        self._btn_chat.style().polish(self._btn_chat)
