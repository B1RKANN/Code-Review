from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from theme import C
from api_client import login_user, register_user

class AuthScreen(QWidget):
    login_success = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("authScreen")
        self.setStyleSheet(f"QWidget#authScreen {{ background-color: {C.BG_0}; }}")
        
        self.is_login_mode = True
        
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.card = QFrame()
        self.card.setFixedWidth(400)
        self.card.setStyleSheet(f"""
            QFrame {{
                background-color: {C.BG_1};
                border: 1px solid {C.BORDER};
                border-radius: 12px;
            }}
        """)
        
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(32, 32, 32, 32)
        card_layout.setSpacing(16)
        
        self.title = QLabel("Giriş Yap")
        self.title.setStyleSheet(f"color: {C.TEXT_1}; font-size: 24px; font-weight: bold; border: none;")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.title)
        
        self.error_label = QLabel("")
        self.error_label.setStyleSheet(f"color: {C.BAD}; font-size: 13px; border: none;")
        self.error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.error_label.hide()
        card_layout.addWidget(self.error_label)
        
        # Name Input (Only for Register)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Ad Soyad")
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {C.BG_2};
                border: 1px solid {C.BORDER};
                border-radius: 6px;
                padding: 10px;
                color: {C.TEXT_1};
            }}
            QLineEdit:focus {{ border: 1px solid {C.ACCENT}; }}
        """)
        self.name_input.hide()
        card_layout.addWidget(self.name_input)
        
        # Email Input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("E-posta")
        self.email_input.setStyleSheet(self.name_input.styleSheet())
        card_layout.addWidget(self.email_input)
        
        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Şifre")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet(self.name_input.styleSheet())
        card_layout.addWidget(self.password_input)
        
        # Action Button
        self.action_btn = QPushButton("Giriş Yap")
        self.action_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {C.ACCENT};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-weight: bold;
                font-size: 14px;
            }}
            QPushButton:hover {{ background-color: {C.ACCENT_STRONG}; }}
        """)
        self.action_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.action_btn.clicked.connect(self.handle_action)
        card_layout.addWidget(self.action_btn)
        
        # Toggle Button
        self.toggle_btn = QPushButton("Hesabın yok mu? Kayıt Ol")
        self.toggle_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: transparent;
                color: {C.TEXT_3};
                border: none;
                font-size: 13px;
            }}
            QPushButton:hover {{ color: {C.ACCENT}; text-decoration: underline; }}
        """)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.clicked.connect(self.toggle_mode)
        card_layout.addWidget(self.toggle_btn)
        
        main_layout.addWidget(self.card)

    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        self.error_label.hide()
        self.email_input.clear()
        self.password_input.clear()
        self.name_input.clear()
        
        if self.is_login_mode:
            self.title.setText("Giriş Yap")
            self.action_btn.setText("Giriş Yap")
            self.toggle_btn.setText("Hesabın yok mu? Kayıt Ol")
            self.name_input.hide()
        else:
            self.title.setText("Kayıt Ol")
            self.action_btn.setText("Kayıt Ol")
            self.toggle_btn.setText("Zaten hesabın var mı? Giriş Yap")
            self.name_input.show()

    def handle_action(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        name = self.name_input.text().strip()
        
        if not email or not password:
            self.show_error("E-posta ve şifre zorunludur.")
            return
            
        if not self.is_login_mode and not name:
            self.show_error("Ad Soyad zorunludur.")
            return

        self.action_btn.setEnabled(False)
        self.action_btn.setText("Bekleniyor...")
        
        if self.is_login_mode:
            success, err_msg = login_user(email, password)
            if success:
                self.login_success.emit()
            else:
                self.show_error(err_msg)
        else:
            success, err_msg = register_user(name, email, password)
            if success:
                self.login_success.emit()
            else:
                self.show_error(err_msg)
                
        self.action_btn.setEnabled(True)
        self.action_btn.setText("Giriş Yap" if self.is_login_mode else "Kayıt Ol")

    def show_error(self, message):
        self.error_label.setText(message)
        self.error_label.show()
