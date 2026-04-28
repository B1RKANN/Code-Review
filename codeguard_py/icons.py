"""SVG benzeri vector path ikonları. QPainter ile çizilir."""
from PyQt6.QtCore import Qt, QSize, QRectF, QPointF
from PyQt6.QtGui import QPainter, QPainterPath, QPen, QColor, QIcon, QPixmap


# Path verileri (18x18 viewbox)
ICONS = {
    "folder":     [("M", 3, 6), ("C", 3, 5, 3.7, 4.5, 4.5, 4.5), ("L", 7.5, 4.5), ("L", 9, 6), ("L", 15, 6), ("C", 15.8, 6, 16.5, 6.7, 16.5, 7.5), ("L", 16.5, 13.5), ("C", 16.5, 14.3, 15.8, 15, 15, 15), ("L", 4.5, 15), ("C", 3.7, 15, 3, 14.3, 3, 13.5), ("Z",)],
    "folderOpen": [("M", 3, 7.5), ("L", 16, 7.5), ("L", 14.8, 13), ("C", 14.65, 13.7, 14, 14, 13.5, 14), ("L", 4.5, 14), ("C", 3.8, 14, 3.2, 13.5, 3, 12.8), ("Z",)],
    "file":       [("M", 5, 2.5), ("L", 10, 2.5), ("L", 13, 5.5), ("L", 13, 14), ("C", 13, 14.6, 12.6, 15, 12, 15), ("L", 5, 15), ("C", 4.4, 15, 4, 14.6, 4, 14), ("L", 4, 3.5), ("C", 4, 2.9, 4.4, 2.5, 5, 2.5), ("Z",)],
    "py":         [("CIRCLE", 9, 9, 6.5), ("M", 5, 9), ("L", 13, 9), ("M", 9, 5), ("L", 9, 13)],
    "chevR":      [("M", 7, 5), ("L", 10, 9), ("L", 7, 13)],
    "chevD":      [("M", 5, 7), ("L", 9, 11), ("L", 13, 7)],
    "search":     [("CIRCLE", 8, 8, 4.5), ("M", 11.5, 11.5), ("L", 14.5, 14.5)],
    "code":       [("M", 5.5, 5.5), ("L", 2, 9), ("L", 5.5, 12.5), ("M", 12.5, 5.5), ("L", 16, 9), ("L", 12.5, 12.5), ("M", 10.5, 4), ("L", 7.5, 14)],
    "gauge":      [("M", 3, 12), ("C", 3, 8.7, 5.7, 6, 9, 6), ("C", 12.3, 6, 15, 8.7, 15, 12), ("M", 9, 12), ("L", 12, 9)],
    "play":       [("M", 6, 4), ("L", 14, 9), ("L", 6, 14), ("Z",)],
    "settings":   [("CIRCLE", 9, 9, 2), ("M", 9, 2), ("L", 9, 4), ("M", 9, 14), ("L", 9, 16), ("M", 2, 9), ("L", 4, 9), ("M", 14, 9), ("L", 16, 9)],
    "bell":       [("M", 5, 12), ("L", 5, 8), ("C", 5, 5.8, 6.8, 4, 9, 4), ("C", 11.2, 4, 13, 5.8, 13, 8), ("L", 13, 12), ("L", 14, 13.5), ("L", 4, 13.5), ("Z",), ("M", 7.5, 14.5), ("C", 7.5, 15.5, 10.5, 15.5, 10.5, 14.5)],
    "shield":     [("M", 9, 2), ("L", 14.5, 4), ("L", 14.5, 9), ("C", 14.5, 12, 12.2, 14.5, 9, 16), ("C", 5.8, 14.5, 3.5, 12, 3.5, 9), ("L", 3.5, 4), ("Z",)],
    "sparkle":    [("M", 9, 2.5), ("L", 10.4, 7.1), ("L", 15, 8.5), ("L", 10.4, 9.9), ("L", 9, 14.5), ("L", 7.6, 9.9), ("L", 3, 8.5), ("L", 7.6, 7.1), ("Z",)],
    "bug":        [("M", 9, 5), ("C", 7.5, 5, 6.5, 6, 6.5, 7.5), ("L", 6.5, 11), ("C", 6.5, 12.5, 7.5, 13.5, 9, 13.5), ("C", 10.5, 13.5, 11.5, 12.5, 11.5, 11), ("L", 11.5, 7.5), ("C", 11.5, 6, 10.5, 5, 9, 5), ("Z",), ("M", 3, 8), ("L", 6.5, 8), ("M", 11.5, 8), ("L", 15, 8)],
    "plus":       [("M", 9, 4), ("L", 9, 14), ("M", 4, 9), ("L", 14, 9)],
    "refresh":    [("M", 14, 5), ("L", 14, 8), ("L", 11, 8), ("M", 14, 8), ("C", 13, 5.5, 10.5, 4, 8, 4), ("C", 5, 4, 3, 6, 3, 9), ("C", 3, 12, 5, 14, 8, 14), ("C", 10, 14, 12, 13, 13, 11.5)],
    "send":       [("M", 3, 9), ("L", 15, 4), ("L", 12, 16), ("L", 9, 11), ("Z",)],
    "paperclip":  [("M", 13, 7), ("L", 8, 12), ("C", 6.5, 13.5, 4.5, 13.5, 3.5, 12.5), ("C", 2.5, 11.5, 2.5, 9.5, 4, 8), ("L", 9.5, 2.5), ("C", 11, 1, 13, 1, 14, 2), ("C", 15, 3, 15, 5, 13.5, 6.5), ("L", 8, 12)],
    "close":      [("M", 5, 5), ("L", 13, 13), ("M", 13, 5), ("L", 5, 13)],
    "check":      [("M", 4, 9.5), ("L", 7, 12.5), ("L", 14, 5.5)],
    "arrowUp":    [("M", 9, 14), ("L", 9, 4), ("M", 5, 8), ("L", 9, 4), ("L", 13, 8)],
    "arrowDown":  [("M", 9, 4), ("L", 9, 14), ("M", 5, 10), ("L", 9, 14), ("L", 13, 10)],
    "branch":     [("CIRCLE", 5, 4, 1.5), ("CIRCLE", 5, 14, 1.5), ("CIRCLE", 13, 6, 1.5), ("M", 5, 5.5), ("L", 5, 12.5), ("M", 5, 9), ("C", 5, 7, 6, 6, 8, 6), ("L", 11.5, 6)],
    "history":    [("CIRCLE", 9, 9, 6), ("M", 9, 5), ("L", 9, 9), ("L", 11.5, 11)],
    "zap":        [("M", 10, 2), ("L", 4, 10), ("L", 8, 10), ("L", 7, 16), ("L", 13, 8), ("L", 9, 8), ("Z",)],
    "list":       [("M", 3, 5), ("L", 15, 5), ("M", 3, 9), ("L", 15, 9), ("M", 3, 13), ("L", 15, 13)],
    "terminal":   [("M", 2, 3), ("L", 16, 3), ("L", 16, 15), ("L", 2, 15), ("Z",), ("M", 5, 7), ("L", 7.5, 9), ("L", 5, 11), ("M", 9, 11), ("L", 13, 11)],
    "eye":        [("M", 2, 9), ("C", 4, 5, 6.5, 4.5, 9, 4.5), ("C", 11.5, 4.5, 14, 5, 16, 9), ("C", 14, 13, 11.5, 13.5, 9, 13.5), ("C", 6.5, 13.5, 4, 13, 2, 9), ("Z",), ("CIRCLE", 9, 9, 2)],
    "sidebarL":   [("M", 2, 2), ("L", 16, 2), ("L", 16, 16), ("L", 2, 16), ("Z",), ("M", 7, 2), ("L", 7, 16)],
    "sidebarR":   [("M", 2, 2), ("L", 16, 2), ("L", 16, 16), ("L", 2, 16), ("Z",), ("M", 11, 2), ("L", 11, 16)],
    "folderUp":   [("M", 3, 7), ("C", 3, 6, 3.7, 5, 4.5, 5), ("L", 7.5, 5), ("L", 9, 7), ("L", 15, 7), ("C", 15.8, 7, 16.5, 7.7, 16.5, 8.5), ("L", 16.5, 14), ("C", 16.5, 14.8, 15.8, 15.5, 15, 15.5), ("L", 4.5, 15.5), ("C", 3.7, 15.5, 3, 14.8, 3, 14), ("Z",), ("M", 9, 9.5), ("L", 9, 13.5), ("M", 7, 11.5), ("L", 9, 9.5), ("L", 11, 11.5)],
}


def _draw_path(painter: QPainter, name: str, color: QColor, size: int, stroke_w: float = 1.6, fill: bool = False):
    if name not in ICONS:
        return
    scale = size / 18.0
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    pen = QPen(color, stroke_w)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    painter.setPen(pen)
    if fill:
        painter.setBrush(color)
    else:
        painter.setBrush(Qt.GlobalColor.transparent)

    path = QPainterPath()
    started = False
    for cmd in ICONS[name]:
        op = cmd[0]
        if op == "M":
            path.moveTo(cmd[1] * scale, cmd[2] * scale); started = True
        elif op == "L":
            path.lineTo(cmd[1] * scale, cmd[2] * scale)
        elif op == "C":
            # 3 control points (cubic)
            path.cubicTo(cmd[1] * scale, cmd[2] * scale,
                         cmd[3] * scale, cmd[4] * scale,
                         cmd[5] * scale, cmd[6] * scale)
        elif op == "Z":
            path.closeSubpath()
        elif op == "CIRCLE":
            cx, cy, r = cmd[1] * scale, cmd[2] * scale, cmd[3] * scale
            path.addEllipse(QPointF(cx, cy), r, r)
    painter.drawPath(path)


def make_icon(name: str, color: str = "#ececf2", size: int = 16, stroke_w: float = 1.6, fill: bool = False) -> QIcon:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    _draw_path(p, name, QColor(color), size, stroke_w, fill)
    p.end()
    return QIcon(pix)


def make_pixmap(name: str, color: str = "#ececf2", size: int = 16, stroke_w: float = 1.6, fill: bool = False) -> QPixmap:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    p = QPainter(pix)
    _draw_path(p, name, QColor(color), size, stroke_w, fill)
    p.end()
    return pix
