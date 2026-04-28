"""Hoş geldin ekranı — ilk açılışta gösterilir."""
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from theme import C
from icons import make_icon


class WelcomeScreen(QFrame):
    open_file_requested = pyqtSignal()
    open_folder_requested = pyqtSignal()
    mock_data_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("welcomeScreen")

        lay = QVBoxLayout(self)
        lay.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.setSpacing(0)

        # Logo
        logo = QLabel()
        logo.setPixmap(make_icon("shield", C.ACCENT, 56, 2.5).pixmap(56, 56))
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(logo)
        lay.addSpacing(16)

        # Başlık
        title = QLabel("CodeGuard")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(title)
        lay.addSpacing(6)

        sub = QLabel("Python kod sağlamlık analizi")
        sub.setObjectName("welcomeSub")
        sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(sub)
        lay.addSpacing(52)

        # Ana butonlar
        btn_row = QHBoxLayout()
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_row.setSpacing(10)

        btn_file = QPushButton("  Dosya Aç")
        btn_file.setObjectName("welcomeBtn")
        btn_file.setIcon(make_icon("file", C.TEXT_2, 14))
        btn_file.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_file.setFixedSize(148, 40)
        btn_file.clicked.connect(self.open_file_requested.emit)
        btn_row.addWidget(btn_file)

        btn_folder = QPushButton("  Klasör Aç")
        btn_folder.setObjectName("welcomeBtnPrimary")
        btn_folder.setIcon(make_icon("folder", "#d9c373", 14))
        btn_folder.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_folder.setFixedSize(148, 40)
        btn_folder.clicked.connect(self.open_folder_requested.emit)
        btn_row.addWidget(btn_folder)

        lay.addLayout(btn_row)
        lay.addSpacing(40)

        # Ayraç
        sep = QLabel("─────  veya örnek proje ile dene  ─────")
        sep.setObjectName("welcomeSepLbl")
        sep.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(sep)
        lay.addSpacing(14)

        # Mock data butonu
        mock_row = QHBoxLayout()
        mock_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btn_mock = QPushButton("  fastapi-payments  ·  Örnek Projeyi Aç")
        btn_mock.setObjectName("welcomeMockBtn")
        btn_mock.setIcon(make_icon("shield", C.ACCENT, 13))
        btn_mock.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_mock.setFixedHeight(36)
        btn_mock.clicked.connect(self.mock_data_requested.emit)
        mock_row.addWidget(btn_mock)
        lay.addLayout(mock_row)

        lay.addSpacing(80)

        ver = QLabel("CodeGuard 1.2.0")
        ver.setObjectName("welcomeVer")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lay.addWidget(ver)
