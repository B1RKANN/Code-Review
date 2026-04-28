"""Tema, renkler, fontlar ve global stylesheet.

HTML mockup'ındaki CSS değişkenlerinin Python karşılığı.
"""
from PyQt6.QtGui import QColor, QFont, QFontDatabase
from PyQt6.QtWidgets import QApplication


# ---------- Renkler ----------
class C:
    BG_0 = "#0a0a0d"
    BG_1 = "#101016"
    BG_2 = "#15151c"
    BG_3 = "#1c1c25"
    BG_4 = "#23232e"
    BORDER = "#2a2a36"
    BORDER_STRONG = "#3a3a48"

    TEXT_1 = "#ececf2"
    TEXT_2 = "#a0a0b0"
    TEXT_3 = "#6a6a78"
    TEXT_4 = "#4a4a56"

    # oklch yaklaşıkları (Qt oklch desteklemediği için hex)
    ACCENT = "#5a8dee"          # oklch(0.7 0.18 250)
    ACCENT_SOFT = "#5a8dee24"
    ACCENT_STRONG = "#7aa3f5"

    GOOD = "#5cc890"            # oklch(0.74 0.16 150)
    GOOD_SOFT = "#5cc89020"
    WARN = "#e0b756"            # oklch(0.8 0.15 85)
    WARN_SOFT = "#e0b75620"
    BAD = "#e26d5a"             # oklch(0.68 0.2 25)
    BAD_SOFT = "#e26d5a20"

    # Syntax
    SYN_KW = "#c08bd6"
    SYN_FN = "#d9c373"
    SYN_STR = "#7ec896"
    SYN_NUM = "#d9a36b"
    SYN_CM = "#4a4a56"
    SYN_OP = TEXT_2
    SYN_CLS = "#7ac4d4"
    SYN_ANN = "#d99a6a"


FONT_UI = "Inter"
FONT_MONO = "JetBrains Mono"


def color_for_score(v: int) -> str:
    if v >= 80:
        return C.GOOD
    if v >= 65:
        return C.WARN
    return C.BAD


def soft_color_for_score(v: int) -> str:
    if v >= 80:
        return C.GOOD_SOFT
    if v >= 65:
        return C.WARN_SOFT
    return C.BAD_SOFT


# ---------- Stylesheet ----------
STYLESHEET = f"""
* {{
    color: {C.TEXT_1};
    font-family: "Inter", "Segoe UI", "Helvetica Neue", sans-serif;
    font-size: 13px;
}}

QMainWindow, QWidget#root, QWidget#body {{
    background: {C.BG_0};
}}

/* ---------- TitleBar ---------- */
QFrame#titlebar {{
    background: {C.BG_1};
    border: none;
    border-bottom: 1px solid {C.BORDER};
}}

QLabel#brandLabel {{ color: {C.TEXT_1}; font-weight: 700; font-size: 13px; }}

QLabel#bcSeg {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", "Consolas", monospace; font-size: 11px; padding: 2px 6px; }}
QLabel#bcSegActive {{ color: {C.TEXT_1}; background: {C.BG_3}; border-radius: 4px; padding: 2px 6px; font-family: "JetBrains Mono", "Consolas", monospace; font-size: 11px; }}
QLabel#bcSep {{ color: {C.TEXT_4}; font-family: "JetBrains Mono", "Consolas", monospace; font-size: 11px; }}

QPushButton#cmdkBtn {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 6px;
    padding: 4px 10px;
    color: {C.TEXT_3};
    font-size: 11px;
    text-align: left;
}}
QPushButton#cmdkBtn:hover {{
    border: 1px solid {C.BORDER_STRONG};
    color: {C.TEXT_2};
}}

QPushButton#tbIconBtn {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 4px;
    color: {C.TEXT_3};
}}
QPushButton#tbIconBtn:hover {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    color: {C.TEXT_1};
}}

/* ---------- Sidebar ---------- */
QFrame#sidebar {{
    background: {C.BG_1};
    border: none;
    border-right: 1px solid {C.BORDER};
}}

QLabel#sectionLabel {{
    color: {C.TEXT_3};
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
}}

QFrame#projectCard {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 6px;
}}

QLabel#projectName {{ color: {C.TEXT_1}; font-weight: 600; font-size: 12px; }}
QLabel#projectMeta {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 10px; }}

QTreeWidget {{
    background: transparent;
    border: none;
    outline: 0;
    color: {C.TEXT_2};
    font-size: 12px;
}}
QTreeWidget::item {{
    padding: 3px 4px;
    border-radius: 4px;
    height: 22px;
}}
QTreeWidget::item:hover {{
    background: {C.BG_2};
    color: {C.TEXT_1};
}}
QTreeWidget::item:selected {{
    background: {C.ACCENT_SOFT};
    color: {C.TEXT_1};
}}
QTreeWidget::branch {{
    background: transparent;
}}

QFrame#venvCard {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 6px;
}}
QLabel#venvLbl {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#venvVal {{ color: {C.TEXT_1}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}

/* ---------- Center / Tabs ---------- */
QFrame#centerTabs {{
    background: {C.BG_1};
    border: none;
    border-bottom: 1px solid {C.BORDER};
}}

QFrame#viewToggle {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 7px;
}}

QPushButton#vtBtn {{
    background: transparent;
    border: none;
    color: {C.TEXT_2};
    font-size: 12px;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 5px;
}}
QPushButton#vtBtn:hover {{ color: {C.TEXT_1}; }}
QPushButton#vtBtnOn {{
    background: {C.BG_4};
    border: none;
    color: {C.TEXT_1};
    font-size: 12px;
    font-weight: 600;
    padding: 5px 12px;
    border-radius: 5px;
}}

QPushButton#scanBtn {{
    background: {C.ACCENT};
    color: {C.BG_0};
    border: 1px solid {C.ACCENT_STRONG};
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 700;
    font-size: 12px;
}}
QPushButton#scanBtn:hover {{ background: {C.ACCENT_STRONG}; }}
QPushButton#scanBtn:disabled {{ background: {C.BG_3}; color: {C.TEXT_3}; border-color: {C.BORDER}; }}

QLabel#scanState {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}

QScrollArea {{ background: {C.BG_0}; border: none; }}
QScrollArea > QWidget > QWidget {{ background: {C.BG_0}; }}
QScrollBar:vertical {{ background: {C.BG_0}; width: 10px; margin: 0; }}
QScrollBar::handle:vertical {{ background: #25252f; min-height: 24px; border-radius: 5px; }}
QScrollBar::handle:vertical:hover {{ background: #2f2f3a; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
QScrollBar:horizontal {{ background: {C.BG_0}; height: 10px; }}
QScrollBar::handle:horizontal {{ background: #25252f; min-width: 24px; border-radius: 5px; }}
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ height: 0; width: 0; }}

/* ---------- Score cards ---------- */
QFrame#overallCard {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 12px;
}}
QFrame#gaugeCard {{
    background: {C.BG_1};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
}}
QLabel#scoreH1 {{ font-size: 22px; font-weight: 700; color: {C.TEXT_1}; }}
QLabel#scoreSub {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 12px; }}
QLabel#metaPill {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
    padding: 3px 10px;
    color: {C.TEXT_3};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QLabel#sectionLabel2 {{
    color: {C.TEXT_3};
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
}}
QLabel#bigNum {{ font-size: 44px; font-weight: 700; color: {C.TEXT_1}; }}
QLabel#unitLabel {{ font-size: 18px; color: {C.TEXT_3}; }}
QLabel#statusPill {{
    border-radius: 10px;
    padding: 4px 10px;
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    font-weight: 700;
}}
QLabel#metricTitle {{ font-size: 13px; font-weight: 600; color: {C.TEXT_1}; }}
QLabel#metricDesc {{ color: {C.TEXT_3}; font-size: 11px; }}
QLabel#metricStat {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#metricStatVal {{ color: {C.TEXT_1}; font-family: "JetBrains Mono", monospace; font-size: 11px; font-weight: 500; }}

QFrame#findingsCard {{
    background: {C.BG_1};
    border: 1px solid {C.BORDER};
    border-radius: 10px;
}}
QFrame#findingsHead {{
    background: {C.BG_2};
    border: none;
    border-bottom: 1px solid {C.BORDER};
}}
QLabel#findingsCount {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#findingTitle {{ color: {C.TEXT_1}; font-size: 12px; font-weight: 500; }}
QLabel#findingLoc {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#sevPill {{ border-radius: 4px; font-family: "JetBrains Mono", monospace; font-size: 10px; font-weight: 700; padding: 3px 6px; }}
QLabel#fmetaTag {{ background: {C.BG_3}; color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 10px; padding: 2px 8px; border-radius: 4px; }}

/* ---------- Code view ---------- */
QFrame#codeToolbar {{ background: {C.BG_1}; border: none; border-bottom: 1px solid {C.BORDER}; }}
QLabel#codeFtab {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-radius: 5px;
    padding: 4px 10px;
    color: {C.TEXT_1};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QLabel#codeInfo {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QPlainTextEdit#codeEdit, QTextEdit#codeEdit {{
    background: {C.BG_0};
    color: {C.TEXT_1};
    border: none;
    font-family: "JetBrains Mono", "Consolas", monospace;
    font-size: 12px;
    selection-background-color: {C.ACCENT_SOFT};
}}

QFrame#codeAside {{ background: {C.BG_1}; border: none; border-left: 1px solid {C.BORDER}; }}
QFrame#asideIssue {{ background: {C.BG_2}; border: 1px solid {C.BORDER}; border-radius: 6px; }}
QLabel#asideTitle {{ font-size: 11px; font-weight: 700; color: {C.TEXT_3}; letter-spacing: 1.5px; }}
QLabel#asideIssueT {{ font-size: 11px; font-weight: 600; color: {C.TEXT_1}; }}
QLabel#asideIssueL {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 10px; }}
QLabel#asideIssueD {{ color: {C.TEXT_2}; font-size: 11px; }}
QPushButton#asideFix {{
    background: {C.BG_3};
    border: 1px solid {C.BORDER};
    color: {C.TEXT_2};
    border-radius: 4px;
    padding: 4px 10px;
    font-family: "JetBrains Mono", monospace;
    font-size: 10px;
    text-align: left;
}}
QPushButton#asideFix:hover {{ color: {C.ACCENT_STRONG}; border: 1px solid {C.ACCENT}; }}

/* ---------- Chat ---------- */
QFrame#chat {{
    background: {C.BG_1};
    border: none;
    border-left: 1px solid {C.BORDER};
}}
QFrame#chatHead {{ background: {C.BG_1}; border: none; border-bottom: 1px solid {C.BORDER}; }}
QLabel#chatAv {{
    background: {C.ACCENT};
    color: {C.BG_0};
    border-radius: 7px;
    font-weight: 700;
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QLabel#chatTi {{ font-size: 13px; font-weight: 600; color: {C.TEXT_1}; }}
QLabel#chatSub {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QPushButton#chatHeadBtn {{ background: transparent; border: none; border-radius: 4px; color: {C.TEXT_3}; padding: 4px; }}
QPushButton#chatHeadBtn:hover {{ background: {C.BG_3}; color: {C.TEXT_1}; }}

QScrollArea#chatBody {{ background: {C.BG_1}; border: none; }}
QScrollArea#chatBody > QWidget > QWidget {{ background: {C.BG_1}; }}

QFrame#msgBub {{ background: {C.BG_2}; border: 1px solid {C.BORDER}; border-radius: 8px; }}
QFrame#msgBubUser {{ background: {C.ACCENT_SOFT}; border: 1px solid {C.ACCENT}; border-radius: 8px; }}
QLabel#msgMeta {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 10px; }}
QLabel#msgText {{ color: {C.TEXT_1}; font-size: 12px; }}
QPlainTextEdit#msgCode {{
    background: {C.BG_0};
    border: 1px solid {C.BORDER};
    border-radius: 6px;
    color: {C.TEXT_1};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}

QPushButton#actionBtn {{
    background: {C.BG_3};
    border: 1px solid {C.BORDER};
    color: {C.TEXT_2};
    border-radius: 5px;
    padding: 4px 10px;
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QPushButton#actionBtn:hover {{ background: {C.BG_4}; color: {C.TEXT_1}; border: 1px solid {C.BORDER_STRONG}; }}
QPushButton#actionBtnPrimary {{
    background: {C.ACCENT_SOFT};
    border: 1px solid {C.ACCENT};
    color: {C.ACCENT_STRONG};
    border-radius: 5px;
    padding: 4px 10px;
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    font-weight: 600;
}}
QPushButton#actionBtnPrimary:hover {{ background: {C.ACCENT}; color: {C.BG_0}; }}

QFrame#chatFoot {{ background: {C.BG_1}; border: none; border-top: 1px solid {C.BORDER}; }}
QPushButton#suggBtn {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    color: {C.TEXT_2};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    border-radius: 12px;
    padding: 4px 10px;
}}
QPushButton#suggBtn:hover {{ color: {C.TEXT_1}; border: 1px solid {C.ACCENT}; }}

QFrame#chatInputBox {{ background: {C.BG_2}; border: 1px solid {C.BORDER}; border-radius: 8px; }}
QFrame#chatInputBoxFocus {{ background: {C.BG_2}; border: 1px solid {C.ACCENT}; border-radius: 8px; }}
QTextEdit#chatInput {{
    background: transparent;
    border: none;
    color: {C.TEXT_1};
    font-size: 12px;
}}
QPushButton#sendBtn {{
    background: {C.ACCENT};
    border: none;
    border-radius: 6px;
    color: {C.BG_0};
    padding: 4px;
}}
QPushButton#sendBtn:disabled {{ background: {C.BG_3}; color: {C.TEXT_3}; }}
QPushButton#attachBtn {{ background: transparent; border: none; color: {C.TEXT_3}; border-radius: 5px; padding: 4px; }}
QPushButton#attachBtn:hover {{ background: {C.BG_3}; color: {C.TEXT_1}; }}

/* ---------- StatusBar ---------- */
QFrame#statusbar {{
    background: {C.BG_1};
    border: none;
    border-top: 1px solid {C.BORDER};
}}
QLabel#sbItem {{ color: {C.TEXT_3}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#sbItemGood {{ color: {C.GOOD}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}
QLabel#sbItemHot {{ color: {C.ACCENT_STRONG}; font-family: "JetBrains Mono", monospace; font-size: 11px; }}

/* ---------- Command Palette ---------- */
QDialog#cmdkDialog {{ background: transparent; }}
QFrame#cmdkBox {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER_STRONG};
    border-radius: 12px;
}}
QFrame#cmdkInput {{ border: none; border-bottom: 1px solid {C.BORDER}; background: transparent; }}
QLineEdit#cmdkLine {{
    background: transparent;
    border: none;
    color: {C.TEXT_1};
    font-size: 14px;
    padding: 6px 0;
}}
QListWidget#cmdkList {{
    background: transparent;
    border: none;
    color: {C.TEXT_1};
    outline: 0;
}}
QListWidget#cmdkList::item {{ padding: 8px 10px; border-radius: 6px; }}
QListWidget#cmdkList::item:selected, QListWidget#cmdkList::item:hover {{ background: {C.ACCENT_SOFT}; }}

/* ---------- Splitter ---------- */
QSplitter#bodySplitter {{
    background: {C.BG_0};
}}
QSplitter#bodySplitter::handle {{
    background: {C.BORDER};
    width: 1px;
}}
QSplitter#bodySplitter::handle:hover,
QSplitter#bodySplitter::handle:pressed {{
    background: {C.ACCENT};
    width: 2px;
}}

/* ---------- Aktif panel butonu ---------- */
QPushButton#tbIconBtnActive {{
    background: {C.ACCENT_SOFT};
    border: 1px solid {C.ACCENT};
    border-radius: 6px;
    padding: 4px;
    color: {C.ACCENT_STRONG};
}}
QPushButton#tbIconBtnActive:hover {{
    background: {C.ACCENT};
    color: {C.BG_0};
}}

/* ---------- Toast ---------- */
QFrame#toast {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-left: 3px solid {C.ACCENT};
    border-radius: 8px;
}}
QFrame#toastGood {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-left: 3px solid {C.GOOD};
    border-radius: 8px;
}}
QFrame#toastWarn {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER};
    border-left: 3px solid {C.WARN};
    border-radius: 8px;
}}
QLabel#toastTitle {{ color: {C.TEXT_1}; font-size: 12px; font-weight: 600; }}
QLabel#toastDesc {{ color: {C.TEXT_3}; font-size: 11px; }}

/* ---------- Welcome Screen ---------- */
QFrame#welcomeScreen {{
    background: {C.BG_0};
}}
QLabel#welcomeTitle {{
    color: {C.TEXT_1};
    font-size: 30px;
    font-weight: 700;
    letter-spacing: -0.5px;
}}
QLabel#welcomeSub {{
    color: {C.TEXT_3};
    font-size: 14px;
}}
QLabel#welcomeSepLbl {{
    color: {C.TEXT_4};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QLabel#welcomeVer {{
    color: {C.TEXT_4};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
}}
QPushButton#welcomeBtn {{
    background: {C.BG_2};
    border: 1px solid {C.BORDER_STRONG};
    border-radius: 8px;
    color: {C.TEXT_1};
    font-size: 13px;
    font-weight: 500;
    padding: 8px 16px;
    text-align: left;
}}
QPushButton#welcomeBtn:hover {{
    background: {C.BG_3};
    border: 1px solid {C.ACCENT};
    color: {C.TEXT_1};
}}
QPushButton#welcomeBtnPrimary {{
    background: {C.ACCENT};
    border: 1px solid {C.ACCENT_STRONG};
    border-radius: 8px;
    color: {C.BG_0};
    font-size: 13px;
    font-weight: 700;
    padding: 8px 16px;
    text-align: left;
}}
QPushButton#welcomeBtnPrimary:hover {{
    background: {C.ACCENT_STRONG};
}}
QPushButton#welcomeMockBtn {{
    background: transparent;
    border: 1px solid {C.BORDER};
    border-radius: 6px;
    color: {C.TEXT_3};
    font-family: "JetBrains Mono", monospace;
    font-size: 11px;
    padding: 6px 14px;
}}
QPushButton#welcomeMockBtn:hover {{
    border: 1px solid {C.BORDER_STRONG};
    color: {C.TEXT_2};
    background: {C.BG_2};
}}
"""


def apply_theme(app: QApplication) -> None:
    # Fontu kayıtlı değilse fallback OK
    app.setStyleSheet(STYLESHEET)
    # Default ui font
    f = QFont("Inter", 9)
    app.setFont(f)
