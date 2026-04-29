"""CodeGuard — Python kod sağlamlık analizi masaüstü uygulaması.

Çalıştırma:
    pip install PyQt6
    python main.py
"""
import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QStackedWidget, QFileDialog, QSplitter,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence, QShortcut

from theme import apply_theme
from widgets.titlebar import TitleBar
from widgets.sidebar import Sidebar
from widgets.center import CenterPane
from widgets.chat import ChatPanel
from widgets.statusbar import StatusBar
from widgets.command_palette import CommandPalette
from widgets.toast import ToastManager
from widgets.welcome import WelcomeScreen
from data import PROJECT, FILE_TREE, FILE_SCORES
from api_client import analyze_file
from PyQt6.QtCore import QThread, pyqtSignal

class ScanWorker(QThread):
    finished = pyqtSignal(dict)
    
    def __init__(self, file_path: str):
        super().__init__()
        self.file_path = file_path
        
    def run(self):
        result = analyze_file(self.file_path)
        self.finished.emit(result if result else {})


# ---------- Yardımcı ----------

# Gösterilecek uzantılar
_SHOW_EXTS = {
    '.py', '.pyx', '.pxd', '.pyi',
    '.js', '.jsx', '.ts', '.tsx', '.vue', '.svelte',
    '.html', '.htm', '.css', '.scss', '.sass', '.less',
    '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg', '.conf',
    '.md', '.txt', '.rst', '.csv', '.log',
    '.sh', '.bash', '.zsh', '.fish', '.ps1', '.bat', '.cmd',
    '.sql', '.graphql',
    '.rb', '.go', '.rs', '.java', '.kt', '.swift',
    '.c', '.cpp', '.cc', '.h', '.hpp',
    '.php', '.r', '.lua', '.ex', '.exs', '.hs', '.elm', '.scala',
    '.xml', '.xsl', '.tex', '.env',
    '.gitignore', '.dockerignore', '.editorconfig',
}

_NO_EXT_SHOW = {
    'makefile', 'dockerfile', 'procfile', 'gemfile', 'rakefile',
    'brewfile', 'vagrantfile', 'jenkinsfile', 'requirements', 'pipfile',
}

_SKIP_DIRS = {
    '__pycache__', '.git', 'node_modules', '.venv', 'venv',
    '.mypy_cache', '.tox', 'dist', 'build', '.pytest_cache',
    '.ruff_cache', 'target', '.idea', '.vs', '.vscode',
}


def _build_file_tree(folder_path: str) -> list:
    def scan(path: str, name: str, depth: int = 0):
        if depth > 4:
            return None
        children = []
        try:
            entries = sorted(os.scandir(path), key=lambda e: (e.is_file(), e.name.lower()))
        except PermissionError:
            return None
        for e in entries:
            if e.name.startswith('.') and e.name.lower() not in ('.env', '.env.example', '.gitignore', '.dockerignore', '.editorconfig'):
                continue
            if e.name in _SKIP_DIRS:
                continue
            if e.is_dir(follow_symlinks=False):
                child = scan(e.path, e.name, depth + 1)
                if child:
                    children.append(child)
            elif e.is_file():
                ext = os.path.splitext(e.name)[1].lower()
                if ext in _SHOW_EXTS or e.name.lower() in _NO_EXT_SHOW:
                    children.append({
                        "type": "file", "name": e.name,
                        "abs_path": os.path.normpath(e.path),
                        "score": None, "lines": 0,
                    })
        if not children:
            return None
        return {"type": "folder", "name": name, "open": depth == 0, "children": children}

    folder_name = os.path.basename(os.path.normpath(folder_path)) or folder_path
    result = scan(os.path.normpath(folder_path), folder_name)
    return result["children"] if result else []


def _find_first_file(nodes: list) -> str:
    for n in nodes:
        if n["type"] == "file":
            return n.get("abs_path") or n["name"]
        found = _find_first_file(n.get("children", []))
        if found:
            return found
    return ""


# ---------- Ana pencere ----------

class CodeGuardWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CodeGuard")
        self.resize(1440, 900)

        self._project_name = ""
        self._project_root: str | None = None
        self.active_path = ""
        self.view_mode = "scores"
        self.scanning = False
        self._api_cache = {}  # Dosya bazlı tarama sonuçlarını önbellekle

        self.toasts = ToastManager(self)

        # Dış yığın: hoş geldin (0) | editör (1)
        self._stack = QStackedWidget()
        self.setCentralWidget(self._stack)

        # ── Sayfa 0: Hoş Geldin ──
        self.welcome = WelcomeScreen()
        self.welcome.open_file_requested.connect(self.open_file_dialog)
        self.welcome.open_folder_requested.connect(self.open_folder_dialog)
        self.welcome.mock_data_requested.connect(self.load_mock_data)
        self._stack.addWidget(self.welcome)

        # ── Sayfa 1: Editör ──
        editor = QWidget(objectName="root")
        el = QVBoxLayout(editor)
        el.setContentsMargins(0, 0, 0, 0)
        el.setSpacing(0)

        self.titlebar = TitleBar(self)
        self.titlebar.cmdk_requested.connect(self.open_command_palette)
        self.titlebar.close_folder_requested.connect(self.close_folder)
        self.titlebar.open_terminal_requested.connect(self.open_terminal)
        self.titlebar.toggle_sidebar_requested.connect(self.toggle_sidebar)
        self.titlebar.toggle_chat_requested.connect(self.toggle_chat)

        # Yeniden boyutlandırılabilir bölünmüş panel
        self._splitter = QSplitter(Qt.Orientation.Horizontal)
        self._splitter.setObjectName("bodySplitter")
        self._splitter.setHandleWidth(1)
        self._splitter.setChildrenCollapsible(False)

        self.sidebar = Sidebar(self)
        self.sidebar.file_selected.connect(self.on_file_selected)
        self.sidebar.reload_requested.connect(self._reload_folder)
        self.sidebar.open_new_requested.connect(self.open_file_dialog)
        self.sidebar.setMinimumWidth(160)
        self.sidebar.setMaximumWidth(520)

        self.center = CenterPane(self)
        self.center.scan_requested.connect(self.run_scan)
        self.center.view_changed.connect(self.on_view_changed)
        self.center.setMinimumWidth(400)

        self.chat = ChatPanel(self)
        self.chat.open_file_requested.connect(self.on_file_selected)
        self.chat.toast_requested.connect(self.toasts.push)
        self.chat.setMinimumWidth(240)
        self.chat.setMaximumWidth(640)

        self._splitter.addWidget(self.sidebar)
        self._splitter.addWidget(self.center)
        self._splitter.addWidget(self.chat)
        self._splitter.setSizes([248, 832, 360])

        self.statusbar = StatusBar(self)

        el.addWidget(self.titlebar)
        el.addWidget(self._splitter, 1)
        el.addWidget(self.statusbar)
        self._stack.addWidget(editor)

        # Kısayollar
        QShortcut(QKeySequence("Ctrl+K"), self, activated=self.open_command_palette)
        QShortcut(QKeySequence("Meta+K"), self, activated=self.open_command_palette)
        QShortcut(QKeySequence("Ctrl+B"), self, activated=self.toggle_sidebar)
        QShortcut(QKeySequence("Ctrl+J"), self, activated=self.toggle_chat)

    # ---------- Sayfa geçişi ----------

    def _show_editor(self):
        self._stack.setCurrentIndex(1)

    # ---------- Yükleme modları ----------

    def load_mock_data(self):
        self.sidebar.load_project(FILE_TREE, PROJECT)
        self._project_name = PROJECT["name"]
        self._project_root = None
        self.active_path = "app/api/webhooks.py"
        self.refresh_for_path()
        self._show_editor()
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(500, lambda: self.toasts.push(
            "Tarama hazır", "Dosyaya tıklayarak skorlarını gör", kind="info"
        ))

    def open_file_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Dosya Aç", self._project_root or "",
            "Python (*.py);;JavaScript (*.js *.ts *.jsx *.tsx);;Tüm dosyalar (*.*)"
        )
        if not path:
            return
        path = os.path.normpath(path)
        name = os.path.basename(path)
        # Eğer editör zaten açıksa ve proje kökü varsa, sadece dosyayı seç
        if self._stack.currentIndex() == 1 and self._project_root:
            self.on_file_selected(path)
            return
        tree = [{"type": "file", "name": name, "abs_path": path, "score": None, "lines": 0}]
        self.sidebar.load_project(tree, {"name": name})
        self._project_name = name
        self._project_root = os.path.dirname(path)
        self.active_path = path
        self.refresh_for_path()
        self._show_editor()

    def open_folder_dialog(self):
        start = self._project_root or ""
        folder = QFileDialog.getExistingDirectory(self, "Klasör Aç", start)
        if not folder:
            return
        folder = os.path.normpath(folder)
        tree = _build_file_tree(folder)
        folder_name = os.path.basename(folder) or folder
        self.sidebar.load_project(tree, {"name": folder_name})
        self._project_name = folder_name
        self._project_root = folder
        self.active_path = _find_first_file(tree)
        self.setWindowTitle(f"{folder_name} — CodeGuard")
        self.refresh_for_path()
        self._show_editor()
        if not tree:
            self.toasts.push("Boş Klasör", "Desteklenen dosya bulunamadı", kind="warn")
        else:
            count = self._count_files(tree)
            self.toasts.push(
                f"{folder_name} açıldı",
                f"{count} dosya yüklendi",
                kind="good"
            )

    def close_folder(self):
        self._project_name = ""
        self._project_root = None
        self.active_path = ""
        self._api_cache.clear()
        self.setWindowTitle("CodeGuard")
        self._stack.setCurrentIndex(0)

    # ---------- Panel toggle ----------

    def toggle_sidebar(self):
        visible = not self.sidebar.isVisible()
        self.sidebar.setVisible(visible)
        self.titlebar.set_sidebar_active(not visible)

    def toggle_chat(self):
        visible = not self.chat.isVisible()
        self.chat.setVisible(visible)
        self.titlebar.set_chat_active(not visible)

    # ---------- Terminal ----------

    def open_terminal(self):
        cwd = self._project_root or os.path.expanduser("~")
        try:
            if sys.platform == "win32":
                subprocess.Popen(
                    ["cmd", "/k", f"cd /d \"{cwd}\""],
                    creationflags=subprocess.CREATE_NEW_CONSOLE
                )
            elif sys.platform == "darwin":
                script = f'tell application "Terminal" to do script "cd {cwd}"'
                subprocess.Popen(["osascript", "-e", script])
            else:
                for term in ["gnome-terminal", "xfce4-terminal", "konsole", "xterm"]:
                    try:
                        subprocess.Popen([term, f"--working-directory={cwd}"])
                        break
                    except FileNotFoundError:
                        continue
        except Exception as exc:
            self.toasts.push("Terminal açılamadı", str(exc), kind="warn")

    # ---------- Yeniden yükleme ----------

    def _reload_folder(self):
        if not self._project_root or not os.path.isdir(self._project_root):
            return
        tree = _build_file_tree(self._project_root)
        folder_name = os.path.basename(self._project_root)
        self.sidebar.load_project(tree, {"name": folder_name})
        self.toasts.push("Klasör güncellendi", f"{self._count_files(tree)} dosya", kind="info")

    # ---------- Slot'lar ----------

    def on_file_selected(self, path: str):
        self.active_path = path
        self.refresh_for_path()

    def on_view_changed(self, mode: str):
        self.view_mode = mode

    def refresh_for_path(self):
        if not self.active_path:
            return
        
        api_data = self._api_cache.get(self.active_path)
        if api_data:
            score = api_data.get("score", FILE_SCORES["default"])
            overall = score.get("overall", 0)
        elif os.path.isabs(self.active_path):
            overall = 0
        else:
            score = FILE_SCORES.get(self.active_path, FILE_SCORES["default"])
            overall = score["overall"]

        self.titlebar.set_breadcrumb(self.active_path, self._project_name)
        self.center.set_active(self.active_path, api_data)
        self.chat.set_active(self.active_path)
        self.statusbar.set_score(self.active_path, overall)

    def run_scan(self):
        if self.scanning or not self.active_path:
            return
        self.scanning = True
        self.center.set_scanning(True)
        self.toasts.push("Tarama başlatıldı", "Yapay zeka analiz ediyor…", kind="info")
        
        # Sadece mock data çalışırken yapay delay (path absolute değilse)
        if not os.path.isabs(self.active_path):
            from PyQt6.QtCore import QTimer
            QTimer.singleShot(2000, self._scan_done)
            return

        self._worker = ScanWorker(self.active_path)
        self._worker.finished.connect(self._scan_done)
        self._worker.start()

    def _scan_done(self, api_data: dict = None):
        print(f"_scan_done called with api_data: {bool(api_data)} for {self.active_path}")
        if api_data:
            print(f"api_data keys: {api_data.keys()}")
            
        self.scanning = False
        self.center.set_scanning(False)
        
        if api_data:
            self._api_cache[self.active_path] = api_data
            self.center.set_active(self.active_path, api_data)
            score = api_data.get("score", {})
            self.statusbar.set_score(self.active_path, score.get("overall", 0))
            self.toasts.push("Tarama tamamlandı", "Skorlar gerçek verilerle güncellendi", kind="good")
        else:
            self.center.replay_animations()
            self.toasts.push("Tarama başarısız", "Sunucudan veri alınamadı veya hata oluştu", kind="bad")

    def open_command_palette(self):
        if self._stack.currentIndex() != 1:
            return
        dlg = CommandPalette(self)
        dlg.command_picked.connect(self.handle_command)
        dlg.exec()

    def handle_command(self, cmd: dict):
        kind = cmd.get("kind")
        if kind == "file":
            self.on_file_selected(cmd["path"])
        elif kind == "view":
            self.center.set_view(cmd["view"])
        elif kind == "action" and "tara" in cmd["label"].lower():
            self.run_scan()

    # ---------- Yardımcı ----------

    @staticmethod
    def _count_files(nodes: list) -> int:
        count = 0
        for n in nodes:
            if n["type"] == "file":
                count += 1
            else:
                count += CodeGuardWindow._count_files(n.get("children", []))
        return count


def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    win = CodeGuardWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
