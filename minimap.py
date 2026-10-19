"""
Minimap — маленькая карта файла справа от редактора.
Клик по карте — прыжок в это место.
Рамка показывает текущую видимую область.
"""

from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QPainter, QColor, QPen
from PyQt6.QtWidgets import QWidget
from PyQt6.Qsci import QsciScintilla


class Minimap(QWidget):
    """Уменьшенная копия текста редактора."""

    LINE_HEIGHT = 2
    PADDING = 4

    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self.setFixedWidth(90)
        self.setMinimumHeight(200)
        self.setMouseTracking(True)
        self._cached_lines = []
        self._cache_dirty = True
        self._theme = None

        self.editor.textChanged.connect(self._invalidate)
        self.editor.verticalScrollBar().valueChanged.connect(self.update)

    def set_theme(self, th):
        self._theme = th
        self.update()

    # ---------- Кэш ----------

    def _invalidate(self):
        self._cache_dirty = True
        self.update()

    def _rebuild_cache(self):
        self._cached_lines = self.editor.text().split("\n")
        self._cache_dirty = False

    # ---------- Отрисовка ----------

    def paintEvent(self, event):
        if self._theme is None:
            return

        if self._cache_dirty:
            self._rebuild_cache()

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing, False)

        bg = QColor(self._theme["editor_bg"])
        fg = QColor(self._theme["editor_fg"])

        p.fillRect(self.rect(), bg)

        total_lines = max(len(self._cached_lines), 1)
        h = self.height()

        visible_lines = max(h // self.LINE_HEIGHT, 1)
        if total_lines > visible_lines:
            step = max(self.LINE_HEIGHT, h / total_lines)
        else:
            step = self.LINE_HEIGHT

        max_line_len = max(
            (len(l) for l in self._cached_lines), default=1
        ) or 1
        cw = max(1.0, (self.width() - 2 * self.PADDING) / max_line_len)

        y = 0.0
        for line in self._cached_lines:
            if y > h:
                break
            if not line.strip():
                y += step
                continue

            line_len = min(len(line), max_line_len)
            w = line_len * cw
            leading = len(line) - len(line.lstrip())
            x = self.PADDING + leading * cw

            ratio = line_len / max_line_len
            color = QColor(fg)
            color.setAlphaF(0.35 + 0.5 * ratio)

            p.fillRect(QRectF(x, y, w, max(step - 1, 1)), color)
            y += step

        # Рамка видимой области
        if total_lines > 0:
            first_line = self.editor.firstVisibleLine()
            try:
                line_height = self.editor.SendScintilla(
                    QsciScintilla.SCI_TEXTHEIGHT, 0
                )
            except Exception:
                line_height = 16
            if line_height <= 0:
                line_height = 16
            editor_h = self.editor.height()
            lines_on_screen = max(editor_h // line_height, 1)

            top_y = (first_line / total_lines) * h
            height_y = max((lines_on_screen / total_lines) * h, 20)
            rect = QRectF(0, top_y, self.width(), height_y)
            pen = QPen(QColor(self._theme["selected_bg"]))
            pen.setWidth(2)
            p.setPen(pen)
            p.setBrush(QColor(0, 0, 0, 0))
            p.drawRect(rect)

        p.end()

    # ---------- Клик → прыжок ----------

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        total_lines = max(len(self._cached_lines), 1)
        h = self.height()
        y = event.position().y()
        ratio = max(0.0, min(1.0, y / h))
        target_line = int(ratio * total_lines)
        self.editor.setCursorPosition(target_line, 0)
        self.editor.ensureLineVisible(target_line)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton:
            self.mousePressEvent(event)
