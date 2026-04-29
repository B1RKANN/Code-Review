"""Sağ panel — AI chat (sahte cevap üretici, animasyonlu yazıyor göstergesi)."""
import random
from PyQt6.QtCore import Qt, pyqtSignal, QTimer, QSize, QThread
from PyQt6.QtGui import QFont, QTextOption
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTextEdit,
    QScrollArea, QSizePolicy, QPlainTextEdit, QWidget
)

from theme import C
from icons import make_icon
from api_client import chat_about_file


SUGGESTIONS = [
    "/scan tüm projeyi",
    "Kodun karmaşıklığı nasıl?",
    "Async refactor öner",
    "Güvenlik açığı var mı?",
]

class ChatWorker(QThread):
    finished = pyqtSignal(dict)
    
    def __init__(self, message: str, active_path: str):
        super().__init__()
        self.message = message
        self.active_path = active_path
        
    def run(self):
        # Gerçek backend çağrısı yap (yapay zeka entegrasyonu)
        reply_html = chat_about_file(self.active_path, self.message)
        payload = {"text": reply_html}
        self.finished.emit(payload)

class _MessageBubble(QFrame):
    action_clicked = pyqtSignal(str, bool)  # label, primary

    def __init__(self, role: str, payload: dict, parent=None):
        super().__init__(parent)
        self.setObjectName("msgBubUser" if role == "user" else "msgBub")
        bg = C.ACCENT_SOFT if role == "user" else C.BG_2
        border = C.ACCENT if role == "user" else C.BORDER
        self.setStyleSheet(
            f"QFrame {{ background:{bg}; border:1px solid {border}; border-radius:8px; }}"
        )
        lay = QVBoxLayout(self); lay.setContentsMargins(12, 9, 12, 9); lay.setSpacing(6)

        if "text" in payload:
            t = QLabel(payload["text"])
            t.setWordWrap(True)
            t.setTextFormat(Qt.TextFormat.RichText)
            t.setStyleSheet(f"color:{C.TEXT_1}; font-size:12px; background:transparent; border:none;")
            lay.addWidget(t)
        if "code" in payload:
            code = QPlainTextEdit(payload["code"])
            code.setReadOnly(True)
            code.setFont(QFont("JetBrains Mono", 9))
            code.setStyleSheet(
                f"QPlainTextEdit {{ background:{C.BG_0}; border:1px solid {C.BORDER}; "
                f"border-radius:6px; color:{C.TEXT_1}; padding:8px; }}"
            )
            lines = payload["code"].count("\n") + 1
            code.setFixedHeight(min(220, 18 * lines + 16))
            lay.addWidget(code)
        if "after" in payload:
            t2 = QLabel(payload["after"])
            t2.setWordWrap(True); t2.setTextFormat(Qt.TextFormat.RichText)
            t2.setStyleSheet(f"color:{C.TEXT_1}; font-size:12px; background:transparent; border:none;")
            lay.addWidget(t2)


class _TypingDots(QLabel):
    def __init__(self, parent=None):
        super().__init__("● ● ●", parent)
        self.setStyleSheet(f"color:{C.TEXT_3}; font-size:12px;")
        self._step = 0
        self._timer = QTimer(self); self._timer.timeout.connect(self._tick); self._timer.start(350)

    def _tick(self):
        self._step = (self._step + 1) % 4
        dots = "● ● ●"
        opa = ["○ ○ ○", "● ○ ○", "● ● ○", "● ● ●"][self._step]
        self.setText(opa)


class ChatPanel(QFrame):
    open_file_requested = pyqtSignal(str)
    toast_requested = pyqtSignal(str, str, str)  # title, desc, kind

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("chat")
        self.setStyleSheet(f"QFrame#chat {{ background:{C.BG_1}; border-left:1px solid {C.BORDER}; }}")
        self._active_path = "app/api/webhooks.py"
        self._messages = []

        lay = QVBoxLayout(self); lay.setContentsMargins(0,0,0,0); lay.setSpacing(0)

        # Head
        head = QFrame(); head.setObjectName("chatHead"); head.setFixedHeight(50)
        hl = QHBoxLayout(head); hl.setContentsMargins(14, 8, 12, 8); hl.setSpacing(10)
        av = QLabel("CG"); av.setObjectName("chatAv")
        av.setFixedSize(28, 28); av.setAlignment(Qt.AlignmentFlag.AlignCenter)
        av.setStyleSheet(f"background:{C.ACCENT}; color:{C.BG_0}; border-radius:7px; font-weight:700; font-family:'JetBrains Mono'; font-size:11px;")
        hl.addWidget(av)
        info = QVBoxLayout(); info.setSpacing(0)
        ti = QLabel("CodeGuard AI"); ti.setObjectName("chatTi")
        sub = QLabel("python kalite uzmanı"); sub.setObjectName("chatSub")
        info.addWidget(ti); info.addWidget(sub)
        hl.addLayout(info, 1)
        for ic in ("history", "plus"):
            b = QPushButton(); b.setObjectName("chatHeadBtn")
            b.setIcon(make_icon(ic, C.TEXT_3, 12)); b.setFixedSize(24, 24)
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            hl.addWidget(b)
        lay.addWidget(head)

        # Body
        self.scroll = QScrollArea(); self.scroll.setObjectName("chatBody"); self.scroll.setWidgetResizable(True)
        self.body = QWidget()
        self.body_layout = QVBoxLayout(self.body)
        self.body_layout.setContentsMargins(14, 14, 14, 8); self.body_layout.setSpacing(12)
        self.body_layout.addStretch()
        self.scroll.setWidget(self.body)
        lay.addWidget(self.scroll, 1)

        # Foot
        foot = QFrame(); foot.setObjectName("chatFoot")
        fl = QVBoxLayout(foot); fl.setContentsMargins(12, 10, 12, 12); fl.setSpacing(8)

        sugg_row = QHBoxLayout(); sugg_row.setSpacing(6)
        for s in SUGGESTIONS:
            b = QPushButton(s); b.setObjectName("suggBtn")
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.clicked.connect(lambda _, t=s: self._send(t))
            sugg_row.addWidget(b)
        sugg_row.addStretch()
        fl.addLayout(sugg_row)

        # Input
        ibox = QFrame(); ibox.setObjectName("chatInputBox")
        ibox.setStyleSheet(f"QFrame#chatInputBox {{ background:{C.BG_2}; border:1px solid {C.BORDER}; border-radius:8px; }}")
        il = QHBoxLayout(ibox); il.setContentsMargins(8, 4, 6, 4); il.setSpacing(6)
        attach = QPushButton(); attach.setObjectName("attachBtn")
        attach.setIcon(make_icon("paperclip", C.TEXT_3, 13)); attach.setFixedSize(26, 26)
        il.addWidget(attach)
        self.input = QTextEdit(); self.input.setObjectName("chatInput")
        self.input.setPlaceholderText("webhooks.py hakkında soru sor…")
        self.input.setFixedHeight(36)
        self.input.setStyleSheet(f"QTextEdit {{ background:transparent; border:none; color:{C.TEXT_1}; font-size:12px; }}")
        self.input.installEventFilter(self)
        il.addWidget(self.input, 1)
        send = QPushButton(); send.setObjectName("sendBtn")
        send.setIcon(make_icon("send", C.BG_0, 12, stroke_w=2.0, fill=True)); send.setFixedSize(28, 28)
        send.setCursor(Qt.CursorShape.PointingHandCursor)
        send.clicked.connect(self._on_send_btn)
        il.addWidget(send)
        fl.addWidget(ibox)
        lay.addWidget(foot)

        # Initial greeting
        self._add_message("assistant", {
            "text": (
                "<p>Merhaba — ben <b>CodeGuard AI</b>. Seçtiğiniz dosyalar veya kod blokları hakkında "
                "bana sorular sorabilir, iyileştirme önerileri veya güvenlik analizi isteyebilirsiniz.</p>"
            ),
        })

    def set_active(self, path: str):
        self._active_path = path
        self.input.setPlaceholderText(f"{path.split('/')[-1]} hakkında soru sor…")

    def eventFilter(self, obj, event):
        from PyQt6.QtCore import QEvent
        if obj is self.input and event.type() == QEvent.Type.KeyPress:
            if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier):
                self._on_send_btn()
                return True
        return super().eventFilter(obj, event)

    def _on_send_btn(self):
        text = self.input.toPlainText().strip()
        if not text:
            return
        self.input.clear()
        self._send(text)

    def _send(self, text: str):
        self._add_message("user", {"text": f"<p>{text}</p>"})
        # typing indicator
        typing_row = self._add_typing()
        
        # Gerçek AI isteğini QThread ile başlat (UI donmasını önlemek için)
        self._chat_worker = ChatWorker(text, self._active_path)
        self._chat_worker.finished.connect(lambda payload: self._reply(payload, typing_row))
        self._chat_worker.start()

    def _reply(self, payload: dict, typing_row: QFrame):
        # remove typing row
        typing_row.setParent(None); typing_row.deleteLater()
        self._add_message("assistant", payload)

    def _add_typing(self):
        row = QFrame()
        rl = QVBoxLayout(row); rl.setContentsMargins(0,0,0,0); rl.setSpacing(4)
        meta = QLabel("CodeGuard AI · yazıyor…"); meta.setObjectName("msgMeta")
        meta.setStyleSheet(f"color:{C.TEXT_3}; font-family:'JetBrains Mono'; font-size:10px;")
        rl.addWidget(meta)
        bub = QFrame()
        bub.setStyleSheet(f"background:{C.BG_2}; border:1px solid {C.BORDER}; border-radius:8px;")
        bl = QHBoxLayout(bub); bl.setContentsMargins(12, 8, 12, 8)
        bl.addWidget(_TypingDots())
        rl.addWidget(bub)
        # Insert before stretch
        self.body_layout.insertWidget(self.body_layout.count() - 1, row)
        QTimer.singleShot(50, self._scroll_bottom)
        return row

    def _add_message(self, role: str, payload: dict, target_file: str = None):
        row = QFrame()
        rl = QVBoxLayout(row); rl.setContentsMargins(0,0,0,0); rl.setSpacing(4)

        meta = QLabel(("Sen" if role == "user" else "CodeGuard AI") + " · şimdi")
        meta.setObjectName("msgMeta")
        meta.setStyleSheet(f"color:{C.TEXT_3}; font-family:'JetBrains Mono'; font-size:10px;")
        rl.addWidget(meta)

        bub = _MessageBubble(role, payload)
        rl.addWidget(bub)

        # Action buttons
        actions = payload.get("actions") or []
        if actions:
            ar = QHBoxLayout(); ar.setSpacing(6); ar.setContentsMargins(0, 4, 0, 0)
            for label, primary in actions:
                b = QPushButton(label)
                b.setObjectName("actionBtnPrimary" if primary else "actionBtn")
                b.setCursor(Qt.CursorShape.PointingHandCursor)
                b.clicked.connect(lambda _, l=label, t=target_file, p=primary: self._on_action(l, t, p))
                ar.addWidget(b)
            ar.addStretch()
            rl.addLayout(ar)

        self.body_layout.insertWidget(self.body_layout.count() - 1, row)
        self._messages.append(row)
        QTimer.singleShot(50, self._scroll_bottom)

    def _on_action(self, label: str, target_file: str, primary: bool):
        if target_file and "aç" in label.lower():
            self.open_file_requested.emit(target_file)
            self.toast_requested.emit("Dosya açıldı", target_file, "good")
            return
        if "uygula" in label.lower() or "patch" in label.lower() or "refactor" in label.lower():
            self.toast_requested.emit("Patch uygulandı", "Skorlar yeniden hesaplanıyor…", "good")
            return
        # Otherwise treat as new query
        self._send(label)

    def _scroll_bottom(self):
        sb = self.scroll.verticalScrollBar()
        sb.setValue(sb.maximum())
