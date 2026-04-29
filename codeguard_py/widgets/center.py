"""Orta panel — Skorlar / Kod görünüm toggle + içerikler."""
import os
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor, QFont, QTextCursor, QTextBlockFormat
from PyQt6.QtWidgets import (
    QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy,
    QScrollArea, QWidget, QStackedWidget, QGridLayout, QPlainTextEdit,
)

from theme import C, color_for_score, soft_color_for_score
from icons import make_icon
from data import FILE_SCORES, FILE_FINDINGS, FILE_SOURCES, FILE_ASIDE, PROJECT
from widgets.gauge import Gauge
from widgets.highlighter import PythonHighlighter


# ---------- Skor görünümü ----------

class _GaugeCard(QFrame):
    def __init__(self, key, metric, parent=None):
        super().__init__(parent)
        self.setObjectName("gaugeCard")
        lay = QHBoxLayout(self); lay.setContentsMargins(18, 16, 20, 16); lay.setSpacing(18)
        lbl = {"perf": "perf", "security": "secure", "cleanCode": "clean", "robust": "solid"}[key]
        self.gauge = Gauge(metric["value"], 108, lbl)
        lay.addWidget(self.gauge, 0, Qt.AlignmentFlag.AlignVCenter)

        right = QVBoxLayout(); right.setSpacing(4)
        title_row = QHBoxLayout(); title_row.setSpacing(8)
        ico_box = QFrame()
        ico_box.setFixedSize(22, 22)
        ico_box.setStyleSheet(f"background:{C.BG_3}; border:1px solid {C.BORDER}; border-radius:6px;")
        ic_lay = QHBoxLayout(ico_box); ic_lay.setContentsMargins(0, 0, 0, 0); ic_lay.setSpacing(0)
        ic_label = QLabel()
        ic_label.setPixmap(make_icon(
            {"security": "shield", "cleanCode": "sparkle", "perf": "zap", "robust": "check"}[key],
            C.TEXT_2, 12
        ).pixmap(12, 12))
        ic_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ic_lay.addWidget(ic_label)
        title_row.addWidget(ico_box)
        t = QLabel(metric["label"]); t.setObjectName("metricTitle")
        title_row.addWidget(t, 1)
        right.addLayout(title_row)

        d = QLabel(metric["desc"]); d.setObjectName("metricDesc"); d.setWordWrap(True)
        right.addWidget(d)

        stats_row = QHBoxLayout(); stats_row.setSpacing(14)
        for k, v in metric["stats"]:
            row = QHBoxLayout(); row.setSpacing(4)
            vlbl = QLabel(v); vlbl.setObjectName("metricStatVal")
            klbl = QLabel(k); klbl.setObjectName("metricStat")
            stats_row.addWidget(vlbl); stats_row.addWidget(klbl)
        stats_row.addStretch()
        right.addLayout(stats_row)
        right.addStretch()
        lay.addLayout(right, 1)


class ScoresView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{C.BG_0};")
        self._lay = QVBoxLayout(self)
        self._lay.setContentsMargins(28, 24, 28, 32)
        self._lay.setSpacing(18)
        self._gauges: list = []
        self._overall_gauge = None

    def populate(self, path: str, api_data: dict = None):
        # Temizle
        while self._lay.count():
            item = self._lay.takeAt(0)
            w = item.widget()
            if w:
                w.deleteLater()
        self._gauges = []
        self._overall_gauge = None

        if api_data:
            score = api_data.get("score", FILE_SCORES["default"])
            findings = api_data.get("findings", [])
        elif path and os.path.isabs(path):
            # Gerçek dosya ama henüz taranmamış
            score = {
                "overall": 0,
                "status": "Henüz taranmadı",
                "statusKind": "info",
                "metrics": {
                    "security": {"label": "Güvenlik", "value": 0, "desc": "Tarama bekleniyor", "stats": []},
                    "cleanCode": {"label": "Temiz Kod", "value": 0, "desc": "Tarama bekleniyor", "stats": []},
                    "perf": {"label": "Performans", "value": 0, "desc": "Tarama bekleniyor", "stats": []},
                    "robust": {"label": "Mimari", "value": 0, "desc": "Tarama bekleniyor", "stats": []},
                }
            }
            findings = []
        else:
            # Mock veriler (demo modu için)
            score = FILE_SCORES.get(path, FILE_SCORES["default"])
            findings = FILE_FINDINGS.get(path, FILE_FINDINGS["default"])

        # Başlık
        hdr = QHBoxLayout(); hdr.setSpacing(14)
        title_box = QVBoxLayout(); title_box.setSpacing(2)
        h1 = QLabel("Kod Sağlamlık Raporu"); h1.setObjectName("scoreH1")
        display_path = os.path.basename(path) if os.path.isabs(path) else path
        sub = QLabel(display_path); sub.setObjectName("scoreSub")
        title_box.addWidget(h1); title_box.addWidget(sub)
        hdr.addLayout(title_box, 1)

        # Gerçek dosyalar için "mock analiz" notu
        if os.path.isabs(path):
            note = QLabel("demo analiz · gerçek API bağlı değil")
            note.setObjectName("metaPill")
            hdr.addWidget(note)
        else:
            for txt in ("scan · 2.4s", PROJECT["branch"], f"@{PROJECT['commit']}"):
                p = QLabel(txt); p.setObjectName("metaPill")
                hdr.addWidget(p)

        wrap = QFrame(); wrap.setLayout(hdr)
        self._lay.addWidget(wrap)

        # Genel kart
        overall = QFrame(); overall.setObjectName("overallCard")
        ol = QHBoxLayout(overall); ol.setContentsMargins(26, 20, 26, 20); ol.setSpacing(28)

        og = Gauge(score["overall"], 140, "genel")
        ol.addWidget(og, 0, Qt.AlignmentFlag.AlignVCenter)
        self._overall_gauge = og

        mid = QVBoxLayout(); mid.setSpacing(4)
        ol_label = QLabel("GENEL SAĞLAMLIK SKORU"); ol_label.setObjectName("sectionLabel2")
        mid.addWidget(ol_label)
        big_row = QHBoxLayout(); big_row.setSpacing(6); big_row.setAlignment(Qt.AlignmentFlag.AlignBottom)
        big = QLabel(str(score["overall"])); big.setObjectName("bigNum")
        unit = QLabel("/ 100"); unit.setObjectName("unitLabel")
        big_row.addWidget(big); big_row.addWidget(unit); big_row.addStretch()
        mid.addLayout(big_row)
        sk = score.get("statusKind", "info")
        pill_bg = {"good": C.GOOD_SOFT, "warn": C.WARN_SOFT, "bad": C.BAD_SOFT, "info": C.ACCENT_SOFT}.get(sk, C.ACCENT_SOFT)
        pill_fg = {"good": C.GOOD, "warn": C.WARN, "bad": C.BAD, "info": C.ACCENT}.get(sk, C.ACCENT)
        pill = QLabel("  " + score["status"]); pill.setObjectName("statusPill")
        pill.setStyleSheet(
            f"background:{pill_bg}; color:{pill_fg}; border-radius:10px; "
            f"padding:4px 10px; font-family:'JetBrains Mono'; font-size:11px; font-weight:700;"
        )
        pill_row = QHBoxLayout(); pill_row.addWidget(pill); pill_row.addStretch()
        mid.addLayout(pill_row)
        ol.addLayout(mid, 1)

        trend = QVBoxLayout(); trend.setSpacing(2); trend.setAlignment(Qt.AlignmentFlag.AlignRight)
        t1 = QLabel("son 7 gün"); t1.setObjectName("metricStat"); t1.setAlignment(Qt.AlignmentFlag.AlignRight)
        t2 = QLabel("▲ +6")
        t2.setStyleSheet(f"color:{C.GOOD}; font-family:'JetBrains Mono'; font-size:14px; font-weight:700;")
        t2.setAlignment(Qt.AlignmentFlag.AlignRight)
        t3 = QLabel(f"{len(findings)} bulgu"); t3.setObjectName("metricStat"); t3.setAlignment(Qt.AlignmentFlag.AlignRight)
        trend.addWidget(t1); trend.addWidget(t2); trend.addWidget(t3)
        ol.addLayout(trend)
        self._lay.addWidget(overall)

        # 2x2 gauge ızgarası
        grid = QGridLayout(); grid.setSpacing(14)
        for i, k in enumerate(["security", "cleanCode", "perf", "robust"]):
            card = _GaugeCard(k, score["metrics"][k])
            grid.addWidget(card, i // 2, i % 2)
            self._gauges.append(card.gauge)
        gw = QFrame(); gw.setLayout(grid)
        self._lay.addWidget(gw)

        # Bulgular
        fcard = QFrame(); fcard.setObjectName("findingsCard")
        fl = QVBoxLayout(fcard); fl.setContentsMargins(0, 0, 0, 0); fl.setSpacing(0)
        fh = QFrame(); fh.setObjectName("findingsHead")
        fhl = QHBoxLayout(fh); fhl.setContentsMargins(18, 12, 18, 12)
        ftitle = QLabel("Bulgular")
        ftitle.setStyleSheet(f"font-size:13px; font-weight:600; color:{C.TEXT_1};")
        fcount = QLabel(f"{len(findings)} aktif · {sum(1 for x in findings if x['sev'] == 'h')} yüksek")
        fcount.setObjectName("findingsCount")
        fhl.addWidget(ftitle); fhl.addStretch(); fhl.addWidget(fcount)
        fl.addWidget(fh)

        for fi in findings:
            row = QFrame()
            row.setStyleSheet(f"QFrame {{ border-top: 1px solid {C.BORDER}; }}")
            rl = QHBoxLayout(row); rl.setContentsMargins(18, 12, 18, 12); rl.setSpacing(12)
            sev = fi["sev"]
            sev_bg = {"h": C.BAD_SOFT, "m": C.WARN_SOFT, "l": C.ACCENT_SOFT}.get(sev, C.ACCENT_SOFT)
            sev_fg = {"h": C.BAD, "m": C.WARN, "l": C.ACCENT_STRONG}.get(sev, C.ACCENT_STRONG)
            spill = QLabel(sev.upper()); spill.setObjectName("sevPill"); spill.setFixedWidth(30)
            spill.setAlignment(Qt.AlignmentFlag.AlignCenter)
            spill.setStyleSheet(
                f"background:{sev_bg}; color:{sev_fg}; border-radius:4px; "
                f"font-family:'JetBrains Mono'; font-size:10px; font-weight:700; padding:3px 0;"
            )
            rl.addWidget(spill, 0, Qt.AlignmentFlag.AlignTop)
            mid2 = QVBoxLayout(); mid2.setSpacing(2)
            t = QLabel(fi["title"]); t.setObjectName("findingTitle")
            l = QLabel(fi["loc"]); l.setObjectName("findingLoc")
            mid2.addWidget(t); mid2.addWidget(l)
            rl.addLayout(mid2, 1)
            tag = QLabel(fi["tag"]); tag.setObjectName("fmetaTag")
            rl.addWidget(tag, 0, Qt.AlignmentFlag.AlignTop)
            fl.addWidget(row)

        self._lay.addWidget(fcard)
        self._lay.addStretch()

    def replay(self):
        if self._overall_gauge:
            self._overall_gauge.replay()
        for g in self._gauges:
            g.replay()


# ---------- Kod görünümü ----------

class CodeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{C.BG_0};")
        root = QHBoxLayout(self); root.setContentsMargins(0, 0, 0, 0); root.setSpacing(0)

        # Kod paneli
        left = QFrame(); ll = QVBoxLayout(left); ll.setContentsMargins(0, 0, 0, 0); ll.setSpacing(0)

        # Araç çubuğu
        tb = QFrame(); tb.setObjectName("codeToolbar"); tb.setFixedHeight(34)
        tbl = QHBoxLayout(tb); tbl.setContentsMargins(14, 4, 14, 4); tbl.setSpacing(10)
        self.ftab = QLabel()
        self.ftab.setObjectName("codeFtab")
        tbl.addWidget(self.ftab)
        tbl.addStretch()
        for txt in ("UTF-8", "LF", "Python", "spaces: 4"):
            l = QLabel(txt); l.setObjectName("codeInfo")
            tbl.addWidget(l)
        ll.addWidget(tb)

        # Editör
        self.edit = QPlainTextEdit()
        self.edit.setObjectName("codeEdit")
        self.edit.setReadOnly(True)
        self.edit.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.edit.setFont(QFont("JetBrains Mono", 10))
        self.edit.setStyleSheet(
            f"QPlainTextEdit {{ background:{C.BG_0}; color:{C.TEXT_1}; border:none; padding:8px 12px; }}"
        )
        self.highlighter = PythonHighlighter(self.edit.document())
        ll.addWidget(self.edit, 1)
        root.addWidget(left, 1)

        # Aside
        aside = QFrame(); aside.setObjectName("codeAside"); aside.setFixedWidth(240)
        al = QVBoxLayout(aside); al.setContentsMargins(16, 14, 16, 14); al.setSpacing(8)
        atitle = QLabel("BU DOSYADA"); atitle.setObjectName("asideTitle")
        al.addWidget(atitle)
        self._aside_layout = al
        root.addWidget(aside)

    def populate(self, path: str, api_data: dict = None):
        fname = os.path.basename(path) if path else ""
        self.ftab.setText(f"  {fname}" if fname else "")

        # Gerçek dosya
        if not api_data and path and os.path.isabs(path) and os.path.isfile(path):
            try:
                with open(path, encoding="utf-8", errors="replace") as f:
                    text = f.read()
            except Exception as exc:
                text = f"# Dosya okunamadı: {exc}"
            self.edit.setPlainText(text)
            self._clear_aside()
            self._aside_layout.addStretch()
            return

        if api_data:
            src = api_data.get("sources", [])
            aside_list = api_data.get("aside", [])
        else:
            src = FILE_SOURCES.get(path, FILE_SOURCES["default"])
            aside_list = FILE_ASIDE.get(path, FILE_ASIDE["default"])

        text = "\n".join(line for _, line, _ in src)
        self.edit.setPlainText(text)

        # Renkli satır arka planları
        for ln, _, issue in src:
            if not issue:
                continue
            block = self.edit.document().findBlockByLineNumber(ln - 1)
            if not block.isValid():
                continue
            cur = QTextCursor(block)
            bf = QTextBlockFormat()
            color = {"warn": C.WARN_SOFT, "bad": C.BAD_SOFT, "info": C.ACCENT_SOFT}[issue]
            bf.setBackground(QColor(color))
            cur.setBlockFormat(bf)

        # Aside
        self._clear_aside()
        for a in aside_list:
            box = QFrame(); box.setObjectName("asideIssue")
            bl = QVBoxLayout(box); bl.setContentsMargins(10, 8, 10, 10); bl.setSpacing(4)
            color = {"warn": C.WARN, "bad": C.BAD, "info": C.ACCENT}[a["sev"]]
            box.setStyleSheet(
                f"QFrame#asideIssue {{ background:{C.BG_2}; border:1px solid {C.BORDER}; "
                f"border-left:3px solid {color}; border-radius:6px; }}"
            )
            head = QHBoxLayout()
            t = QLabel(a["title"]); t.setObjectName("asideIssueT")
            l = QLabel(f"L{a['line']}"); l.setObjectName("asideIssueL")
            head.addWidget(t, 1); head.addWidget(l)
            bl.addLayout(head)
            d = QLabel(a["desc"]); d.setObjectName("asideIssueD"); d.setWordWrap(True)
            bl.addWidget(d)
            if a.get("fix"):
                btn = QPushButton(a["fix"]); btn.setObjectName("asideFix")
                btn.setIcon(make_icon("sparkle", C.TEXT_2, 10))
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                bl.addWidget(btn, 0, Qt.AlignmentFlag.AlignLeft)
            self._aside_layout.addWidget(box)
        self._aside_layout.addStretch()

    def _clear_aside(self):
        while self._aside_layout.count() > 1:
            item = self._aside_layout.takeAt(1)
            if item.widget():
                item.widget().deleteLater()


# ---------- Orta panel ----------

class CenterPane(QFrame):
    scan_requested = pyqtSignal()
    view_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"background:{C.BG_0};")
        lay = QVBoxLayout(self); lay.setContentsMargins(0, 0, 0, 0); lay.setSpacing(0)

        # Tab çubuğu
        tabs = QFrame(); tabs.setObjectName("centerTabs"); tabs.setFixedHeight(46)
        tl = QHBoxLayout(tabs); tl.setContentsMargins(14, 6, 14, 6); tl.setSpacing(10)

        toggle = QFrame(); toggle.setObjectName("viewToggle")
        tg = QHBoxLayout(toggle); tg.setContentsMargins(2, 2, 2, 2); tg.setSpacing(0)
        self.btn_scores = QPushButton("  Skorlar"); self.btn_scores.setObjectName("vtBtnOn")
        self.btn_scores.setIcon(make_icon("gauge", C.TEXT_1, 12))
        self.btn_code = QPushButton("  Kod"); self.btn_code.setObjectName("vtBtn")
        self.btn_code.setIcon(make_icon("code", C.TEXT_2, 12))
        for b in (self.btn_scores, self.btn_code):
            b.setCursor(Qt.CursorShape.PointingHandCursor)
            b.setFixedHeight(28)
        tg.addWidget(self.btn_scores); tg.addWidget(self.btn_code)
        tl.addWidget(toggle)
        tl.addStretch()

        self._scan_lbl = QLabel("● son tarama 2 dk önce")
        self._scan_lbl.setObjectName("scanState")
        self._scan_lbl.setStyleSheet(f"color:{C.GOOD}; font-family:'JetBrains Mono'; font-size:11px;")
        tl.addWidget(self._scan_lbl)

        self.scan_btn = QPushButton("  Tara")
        self.scan_btn.setObjectName("scanBtn")
        self.scan_btn.setIcon(make_icon("play", C.BG_0, 11, fill=True))
        self.scan_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.scan_btn.clicked.connect(self.scan_requested.emit)
        tl.addWidget(self.scan_btn)
        lay.addWidget(tabs)

        # Yığın: skorlar / kod
        self.stack = QStackedWidget()
        self.scores_scroll = QScrollArea(); self.scores_scroll.setWidgetResizable(True)
        self.scores_view = ScoresView()
        self.scores_scroll.setWidget(self.scores_view)
        self.code_view = CodeView()
        self.stack.addWidget(self.scores_scroll)
        self.stack.addWidget(self.code_view)
        lay.addWidget(self.stack, 1)

        self.btn_scores.clicked.connect(lambda: self.set_view("scores"))
        self.btn_code.clicked.connect(lambda: self.set_view("code"))

    def set_active(self, path: str, api_data: dict = None):
        if not path:
            return
        self.scores_view.populate(path, api_data)
        self.code_view.populate(path, api_data)

    def set_view(self, mode: str):
        if mode == "scores":
            self.btn_scores.setObjectName("vtBtnOn"); self.btn_scores.setIcon(make_icon("gauge", C.TEXT_1, 12))
            self.btn_code.setObjectName("vtBtn"); self.btn_code.setIcon(make_icon("code", C.TEXT_2, 12))
            self.stack.setCurrentIndex(0)
        else:
            self.btn_scores.setObjectName("vtBtn"); self.btn_scores.setIcon(make_icon("gauge", C.TEXT_2, 12))
            self.btn_code.setObjectName("vtBtnOn"); self.btn_code.setIcon(make_icon("code", C.TEXT_1, 12))
            self.stack.setCurrentIndex(1)
        for b in (self.btn_scores, self.btn_code):
            b.style().unpolish(b); b.style().polish(b)
        self.view_changed.emit(mode)

    def set_scanning(self, on: bool):
        if on:
            self._scan_lbl.setText("● taranıyor…")
            self._scan_lbl.setStyleSheet(f"color:{C.WARN}; font-family:'JetBrains Mono'; font-size:11px;")
            self.scan_btn.setText("  Taranıyor")
            self.scan_btn.setIcon(make_icon("refresh", C.BG_0, 11, fill=True))
            self.scan_btn.setEnabled(False)
        else:
            self._scan_lbl.setText("● son tarama az önce")
            self._scan_lbl.setStyleSheet(f"color:{C.GOOD}; font-family:'JetBrains Mono'; font-size:11px;")
            self.scan_btn.setText("  Tara")
            self.scan_btn.setIcon(make_icon("play", C.BG_0, 11, fill=True))
            self.scan_btn.setEnabled(True)

    def replay_animations(self):
        self.scores_view.replay()
