"""Alt status bar."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel

from theme import C, color_for_score
from icons import make_icon
from data import PROJECT


class StatusBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statusbar")
        self.setFixedHeight(26)
        lay = QHBoxLayout(self); lay.setContentsMargins(12, 0, 12, 0); lay.setSpacing(14)

        def item(text, kind="default", icon=None):
            wrap = QFrame()
            l = QHBoxLayout(wrap); l.setContentsMargins(0,0,0,0); l.setSpacing(5)
            if icon:
                ic = QLabel()
                color = C.GOOD if kind == "good" else C.TEXT_3
                ic.setPixmap(make_icon(icon, color, 11).pixmap(11, 11))
                l.addWidget(ic)
            lbl = QLabel(text)
            lbl.setObjectName({"good":"sbItemGood","hot":"sbItemHot"}.get(kind, "sbItem"))
            l.addWidget(lbl)
            return wrap

        lay.addWidget(item(PROJECT["branch"], icon="branch"))
        lay.addWidget(item(f"@{PROJECT['commit']}"))
        lay.addWidget(item("venv aktif", kind="good", icon="check"))
        lay.addWidget(item(f"python {PROJECT['python']}"))
        lay.addStretch()
        self._file_label = QLabel("")
        self._file_label.setObjectName("sbItem")
        lay.addWidget(self._file_label)

        self._score_dot = QLabel(); self._score_dot.setFixedSize(8, 8)
        self._score_lbl = QLabel("")
        self._score_lbl.setObjectName("sbItem")
        lay.addWidget(self._score_dot)
        lay.addWidget(self._score_lbl)

        ver = QLabel("CodeGuard 1.2.0"); ver.setObjectName("sbItemHot")
        lay.addWidget(ver)

    def set_score(self, path: str, overall: int):
        self._file_label.setText(path.split("/")[-1])
        c = color_for_score(overall)
        self._score_dot.setStyleSheet(f"background:{c}; border-radius:4px;")
        self._score_lbl.setText(f"skor {overall}")
