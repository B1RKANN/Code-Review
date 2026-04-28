"""Cmd+K komut paleti."""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget,
    QListWidgetItem, QFrame, QLabel, QSizePolicy
)

from theme import C
from icons import make_icon
from data import COMMANDS


class CommandPalette(QDialog):
    command_picked = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("cmdkDialog")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setModal(True)

        outer = QVBoxLayout(self); outer.setContentsMargins(0,0,0,0); outer.setSpacing(0)

        box = QFrame(); box.setObjectName("cmdkBox")
        box.setFixedWidth(560)
        bl = QVBoxLayout(box); bl.setContentsMargins(0,0,0,0); bl.setSpacing(0)

        # Input
        inp = QFrame(); inp.setObjectName("cmdkInput")
        il = QHBoxLayout(inp); il.setContentsMargins(14, 12, 14, 12); il.setSpacing(10)
        ico = QLabel(); ico.setPixmap(make_icon("search", C.TEXT_3, 14).pixmap(14, 14))
        il.addWidget(ico)
        self.line = QLineEdit(); self.line.setObjectName("cmdkLine")
        self.line.setPlaceholderText("Komut, dosya, eylem ara…")
        self.line.textChanged.connect(self._refilter)
        self.line.returnPressed.connect(self._on_enter)
        il.addWidget(self.line, 1)
        kbd = QLabel("esc"); kbd.setStyleSheet(
            f"color:{C.TEXT_3}; background:{C.BG_3}; border:1px solid {C.BORDER}; "
            f"border-radius:3px; padding:1px 5px; font-family:'JetBrains Mono'; font-size:10px;"
        )
        il.addWidget(kbd)
        bl.addWidget(inp)

        # List
        self.lst = QListWidget(); self.lst.setObjectName("cmdkList")
        self.lst.setFixedHeight(320)
        self.lst.itemActivated.connect(self._on_pick)
        self.lst.itemClicked.connect(self._on_pick)
        bl.addWidget(self.lst)

        outer.addStretch()
        center = QHBoxLayout(); center.addStretch(); center.addWidget(box); center.addStretch()
        outer.addLayout(center)
        outer.addStretch()

        self.resize(900, 600)
        self._populate(COMMANDS)
        self.line.setFocus()

    def _populate(self, items):
        self.lst.clear()
        for c in items:
            it = QListWidgetItem(c["label"])
            it.setIcon(make_icon(c["icon"], C.TEXT_2, 14))
            it.setData(Qt.ItemDataRole.UserRole, c)
            self.lst.addItem(it)
        if self.lst.count() > 0:
            self.lst.setCurrentRow(0)

    def _refilter(self, q: str):
        ql = q.lower()
        filtered = [c for c in COMMANDS if ql in c["label"].lower()]
        self._populate(filtered)

    def _on_enter(self):
        it = self.lst.currentItem()
        if it:
            self._on_pick(it)

    def _on_pick(self, item):
        if not item:
            return
        c = item.data(Qt.ItemDataRole.UserRole)
        if c:
            self.command_picked.emit(c)
        self.accept()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key.Key_Escape:
            self.reject(); return
        if e.key() == Qt.Key.Key_Down:
            self.lst.setCurrentRow(min(self.lst.count()-1, self.lst.currentRow()+1)); return
        if e.key() == Qt.Key.Key_Up:
            self.lst.setCurrentRow(max(0, self.lst.currentRow()-1)); return
        super().keyPressEvent(e)

    def mousePressEvent(self, e):
        # Click outside box → close
        if not self.childAt(e.pos()):
            self.reject()
        super().mousePressEvent(e)
