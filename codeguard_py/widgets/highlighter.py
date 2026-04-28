"""Python syntax highlighter — QSyntaxHighlighter."""
import re
from PyQt6.QtCore import Qt, QRegularExpression
from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from theme import C


class PythonHighlighter(QSyntaxHighlighter):
    KEYWORDS = (
        "from import async await def class return if elif else try except "
        "pass with as for in not and or is None True False raise yield "
        "lambda self finally global nonlocal break continue"
    ).split()

    def __init__(self, doc):
        super().__init__(doc)

        def fmt(color, bold=False, italic=False):
            f = QTextCharFormat()
            f.setForeground(QColor(color))
            if bold:
                f.setFontWeight(QFont.Weight.Bold)
            if italic:
                f.setFontItalic(True)
            return f

        self.f_kw = fmt(C.SYN_KW)
        self.f_fn = fmt(C.SYN_FN)
        self.f_str = fmt(C.SYN_STR)
        self.f_num = fmt(C.SYN_NUM)
        self.f_cm = fmt(C.SYN_CM, italic=True)
        self.f_ann = fmt(C.SYN_ANN)
        self.f_cls = fmt(C.SYN_CLS)

        self.rules = []
        # Keywords
        for kw in self.KEYWORDS:
            self.rules.append((QRegularExpression(rf"\b{kw}\b"), self.f_kw))
        # Function calls
        self.rules.append((QRegularExpression(r"\b([A-Za-z_][\w]*)(?=\()"), self.f_fn))
        # Numbers
        self.rules.append((QRegularExpression(r"\b\d+(\.\d+)?\b"), self.f_num))
        # Decorators
        self.rules.append((QRegularExpression(r"@[\w.]+"), self.f_ann))
        # Strings (simple, single line)
        self.rules.append((QRegularExpression(r"\".*?\""), self.f_str))
        self.rules.append((QRegularExpression(r"'.*?'"), self.f_str))
        # Comments
        self.rules.append((QRegularExpression(r"#.*$"), self.f_cm))

    def highlightBlock(self, text: str):
        for regex, fmt in self.rules:
            it = regex.globalMatch(text)
            while it.hasNext():
                m = it.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)
