"""Sol panel — proje kartı, dosya ağacı, venv durumu."""
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTreeWidget, QTreeWidgetItem,
)

from theme import C
from icons import make_icon


class FileBadge(QLabel):
    def __init__(self, score: int, severity: str = None):
        super().__init__(str(score))
        self.setFixedHeight(16)
        self.setMinimumWidth(28)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sev = severity or ("good" if score >= 85 else "warn" if score >= 70 else "bad")
        bg = {"good": C.GOOD_SOFT, "warn": C.WARN_SOFT, "bad": C.BAD_SOFT}[sev]
        fg = {"good": C.GOOD, "warn": C.WARN, "bad": C.BAD}[sev]
        self.setStyleSheet(
            f"background:{bg}; color:{fg}; border-radius:8px; "
            f"font-family:'JetBrains Mono',monospace; font-size:10px; font-weight:700; padding:0 6px;"
        )


class Sidebar(QFrame):
    file_selected = pyqtSignal(str)
    reload_requested = pyqtSignal()
    open_new_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self._pending_badges: list = []

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # ── WORKSPACE bölümü ──
        ws_row = QHBoxLayout()
        ws_row.setContentsMargins(14, 10, 10, 4)
        ws_row.setSpacing(4)
        ws_lbl = QLabel("WORKSPACE"); ws_lbl.setObjectName("sectionLabel")
        ws_row.addWidget(ws_lbl, 1)

        btn_reload = QPushButton()
        btn_reload.setObjectName("tbIconBtn")
        btn_reload.setIcon(make_icon("refresh", C.TEXT_3, 11))
        btn_reload.setFixedSize(20, 20)
        btn_reload.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_reload.setToolTip("Klasörü Yenile")
        btn_reload.clicked.connect(self.reload_requested.emit)
        ws_row.addWidget(btn_reload)

        btn_new = QPushButton()
        btn_new.setObjectName("tbIconBtn")
        btn_new.setIcon(make_icon("plus", C.TEXT_3, 11))
        btn_new.setFixedSize(20, 20)
        btn_new.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_new.setToolTip("Dosya Aç")
        btn_new.clicked.connect(self.open_new_requested.emit)
        ws_row.addWidget(btn_new)

        lay.addLayout(ws_row)

        # ── Proje kartı ──
        card = QFrame(); card.setObjectName("projectCard")
        cl = QHBoxLayout(card); cl.setContentsMargins(8, 8, 8, 8); cl.setSpacing(8)
        self._avatar_lbl = QLabel(); self._avatar_lbl.setFixedSize(28, 28)
        self._avatar_lbl.setPixmap(make_icon("shield", C.ACCENT, 28, 2.0).pixmap(28, 28))
        info = QVBoxLayout(); info.setSpacing(0)
        self._name_lbl = QLabel("—"); self._name_lbl.setObjectName("projectName")
        self._meta_lbl = QLabel("klasör veya dosya aç"); self._meta_lbl.setObjectName("projectMeta")
        info.addWidget(self._name_lbl); info.addWidget(self._meta_lbl)
        cl.addWidget(self._avatar_lbl); cl.addLayout(info, 1)
        proj_wrap = QFrame()
        QVBoxLayout(proj_wrap).setContentsMargins(8, 0, 8, 8)
        proj_wrap.layout().addWidget(card)
        lay.addWidget(proj_wrap)

        # ── FILES bölümü ──
        files_row = QHBoxLayout()
        files_row.setContentsMargins(14, 10, 10, 4)
        files_row.setSpacing(4)
        files_lbl = QLabel("FILES"); files_lbl.setObjectName("sectionLabel")
        files_row.addWidget(files_lbl, 1)
        btn_search = QPushButton()
        btn_search.setObjectName("tbIconBtn")
        btn_search.setIcon(make_icon("search", C.TEXT_3, 11))
        btn_search.setFixedSize(20, 20)
        btn_search.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_search.setToolTip("Dosya Ara")
        files_row.addWidget(btn_search)
        lay.addLayout(files_row)

        # ── Dosya ağacı ──
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(14)
        self.tree.setRootIsDecorated(True)
        self.tree.setColumnCount(2)
        self.tree.setColumnWidth(0, 170)
        self.tree.setAnimated(True)
        self.tree.itemClicked.connect(self._on_item_clicked)
        lay.addWidget(self.tree, 1)

        # ── Venv kartı ──
        self._venv_wrap = QFrame()
        self._venv_wrap.setStyleSheet(f"QFrame {{ border-top: 1px solid {C.BORDER}; }}")
        vl_outer = QVBoxLayout(self._venv_wrap)
        vl_outer.setContentsMargins(10, 8, 10, 12)

        venv = QFrame(); venv.setObjectName("venvCard")
        vl = QVBoxLayout(venv); vl.setContentsMargins(10, 8, 10, 8); vl.setSpacing(3)

        self._venv_val_labels: list[QLabel] = []
        for row_lbl, dot_color in [("runtime", C.GOOD), ("venv", None), ("deps", None)]:
            row = QHBoxLayout(); row.setSpacing(8)
            dot = QLabel(); dot.setFixedSize(8, 8)
            if dot_color:
                dot.setStyleSheet(f"background:{dot_color}; border-radius:4px;")
            key_lbl = QLabel(row_lbl); key_lbl.setObjectName("venvLbl"); key_lbl.setMinimumWidth(50)
            val_lbl = QLabel("—"); val_lbl.setObjectName("venvVal")
            row.addWidget(dot); row.addWidget(key_lbl); row.addWidget(val_lbl, 1)
            vl.addLayout(row)
            self._venv_val_labels.append(val_lbl)

        vl_outer.addWidget(venv)
        lay.addWidget(self._venv_wrap)
        self._venv_wrap.setVisible(False)

    # ---------- Proje yükleme ----------

    def load_project(self, tree_nodes: list, project_info: dict):
        name = project_info.get("name", "—")
        py = project_info.get("python", "")
        pkg = project_info.get("pkg", "")

        self._name_lbl.setText(name)
        meta_parts = [x for x in [py, pkg] if x]
        self._meta_lbl.setText(" · ".join(meta_parts) if meta_parts else "proje açıldı")

        # Venv
        has_env = bool(py or project_info.get("venv") or pkg)
        self._venv_wrap.setVisible(has_env)
        if has_env:
            for val_lbl, val in zip(self._venv_val_labels, [
                f"python {py}" if py else "—",
                project_info.get("venv", "—") or "—",
                pkg or "—",
            ]):
                val_lbl.setText(val)

        # Ağacı yenile
        self.tree.clear()
        self._pending_badges = []
        self._populate(self.tree.invisibleRootItem(), tree_nodes, "")
        self.tree.expandToDepth(1)
        QTimer.singleShot(0, self._flush_badges)

    # ---------- Dahili ----------

    def _flush_badges(self):
        for it, badge in self._pending_badges:
            self.tree.setItemWidget(it, 1, badge)
        self._pending_badges = []

    def showEvent(self, e):
        super().showEvent(e)
        self._flush_badges()

    def _populate(self, parent_item, nodes, parent_path):
        for n in nodes:
            abs_path = n.get("abs_path")
            rel_path = f"{parent_path}/{n['name']}" if parent_path else n["name"]
            emit_path = abs_path if abs_path else rel_path

            it = QTreeWidgetItem(parent_item)
            if n["type"] == "folder":
                it.setIcon(0, make_icon("folder", "#d9c373", 13))
                it.setText(0, n["name"])
                it.setData(0, Qt.ItemDataRole.UserRole, {"type": "folder", "path": rel_path})
                if n.get("open"):
                    it.setExpanded(True)
                self._populate(it, n.get("children", []), rel_path)
            else:
                ext = n["name"].rsplit(".", 1)[-1].lower() if "." in n["name"] else ""
                icon_name = "py" if ext == "py" else "file"
                clr = C.ACCENT if ext == "py" else C.TEXT_3
                it.setIcon(0, make_icon(icon_name, clr, 12))
                it.setText(0, n["name"])
                it.setData(0, Qt.ItemDataRole.UserRole, {"type": "file", "path": emit_path})
                if n.get("score") is not None:
                    self._pending_badges.append((it, FileBadge(n["score"], n.get("severity"))))

    def _on_item_clicked(self, item: QTreeWidgetItem, col: int):
        data = item.data(0, Qt.ItemDataRole.UserRole) or {}
        if data.get("type") == "file":
            self.file_selected.emit(data["path"])
        elif data.get("type") == "folder":
            item.setExpanded(not item.isExpanded())
