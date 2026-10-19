"""
Gutter — колонка с номерами строк слева от редактора.
Рисуется вручную через paintEvent, синхронизируется с редактором.
Стиль — как в VS Code: без стрелочек, с тонкой разделительной линией.
"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QColor, QFont, QPen
from PyQt6.QtWidgets import QWidget


class Gutter(QWidget):
    """Левый виджет с номерами строк."""

    PADDING_LEFT = 6       # от левого края до цифр
    PADDING_RIGHT = 4      # от цифр до разделительной линии
    LINE_OFFSET = 2         # смещение линии от правого края

    def __init__(self, editor, parent=None):
        super().__init__(parent)
        self.editor = editor
        self._theme = None
        self._font = QFont("JetBrains Mono", 11)

        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, True)

        # Реакция на изменения
        self.editor.verticalScrollBar().valueChanged.connect(self.update)
        self.editor.textChanged.connect(self._on_text_changed)
        self.editor.cursorPositionChanged.connect(self.update)

        # Периодическая проверка скролла (на случай если сигнал не сработал)
        self._timer = QTimer(self)
        self._timer.setInterval(120)
        self._timer.timeout.connect(self._tick)
        self._timer.start()
        self._last_first = -1
        
        # Сразу подгоняем ширину под шрифт
        self._auto_width()

    def _on_text_changed(self):
        self._auto_width()
        self.update()

    def _tick(self):
        try:
            first = self.editor.firstVisibleLine()
        except Exception:
            return
        if first != self._last_first:
            self._last_first = first
            self.update()

    # ---------- Тема и шрифт ----------

    def apply_theme(self, th):
        self._theme = th
        self.update()

    def apply_font(self, font):
        self._font = QFont(font)
        self._auto_width()
        self.update()

    def _auto_width(self):
        """Авто-ширина под количество цифр в максимальном номере."""
        try:
            total = self.editor.lines()
        except Exception:
            total = 9999
        digits = max(len(str(total)), 2)
        fm = self.fontMetrics()
        text_w = fm.horizontalAdvance("0" * digits)
        w = self.PADDING_LEFT + text_w + self.PADDING_RIGHT + self.LINE_OFFSET
        self.setFixedWidth(w)

    # ---------- Отрисовка ----------

    def paintEvent(self, event):
        if self._theme is None:
            return

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.TextAntialiasing, True)

        # Фон gutter = фон редактора (как в VS Code)
        bg = QColor(self._theme["editor_bg"])
        p.fillRect(self.rect(), bg)

        # Разделительная линия справа
        edge = QColor(self._theme["edge_color"])
        pen = QPen(edge)
        pen.setWidth(1)
        p.setPen(pen)
        x_line = self.width() - self.LINE_OFFSET - 1
        p.drawLine(x_line, 0, x_line, self.height())

        try:
            first = self.editor.firstVisibleLine()
            total = self.editor.lines()
            line_h = self.editor.SendScintilla(
                self.editor.SCI_TEXTHEIGHT, first
            )
        except Exception:
            return

        if line_h <= 0:
            line_h = 16

        h = self.height()
        fm = p.fontMetrics()
        count = h // line_h + 1

        # Номера строк — серые
        fg = QColor(self._theme["margin_fg"])
        p.setPen(fg)
        p.setFont(self._font)

        # Стрелочки — светло-серые, чётко видны
        arrow_color = QColor("#c0c0c0")

        x_line = self.width() - self.LINE_OFFSET - 1
        arrow_x = 6  # отступ стрелочки от левого края

        y = 0
        for i in range(first, min(first + count, total)):
            # === Номер строки ===
            text = str(i + 1)
            text_w = fm.horizontalAdvance(text)
            x = x_line - self.PADDING_RIGHT - text_w
            p.drawText(x, y + line_h - fm.descent() - 2, text)

            # === Стрелочка сворачивания ===
            try:
                foldable = self.editor.is_foldable(i)
            except Exception:
                foldable = False

            if foldable:
                folded = self.editor.is_folded(i)
                p.setPen(arrow_color)
                # Центр стрелочки по вертикали
                cy = y + line_h // 2
                # Рисуем треугольник
                if folded:
                    # ▶ — свёрнуто (стрелка вправо)
                    pts = [
                        (arrow_x, cy - 4),
                        (arrow_x + 6, cy),
                        (arrow_x, cy + 4),
                    ]
                else:
                    # ▼ — развёрнуто (стрелка вниз)
                    pts = [
                        (arrow_x, cy - 3),
                        (arrow_x + 7, cy - 3),
                        (arrow_x + 3, cy + 2),
                    ]
                # Заливаем треугольник
                from PyQt6.QtGui import QPolygon
                from PyQt6.QtCore import QPoint
                poly = QPolygon([QPoint(x, yy) for x, yy in pts])
                p.setBrush(arrow_color)
                p.drawPolygon(poly)
                # Возвращаем серый для номеров
                p.setPen(fg)

            y += line_h

        p.end()

    # ---------- Клик — выбор строки ----------

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        try:
            first = self.editor.firstVisibleLine()
            line_h = self.editor.SendScintilla(
                self.editor.SCI_TEXTHEIGHT, first
            )
        except Exception:
            return
        if line_h <= 0:
            return
        y = event.position().y()
        x = event.position().x()
        offset = int(y // line_h)
        target = first + offset
        total = self.editor.lines()
        if not (0 <= target < total):
            return

        # Клик по зоне стрелочки (первые ~18 пикселей)?
        if x < 18:
            try:
                if self.editor.is_foldable(target):
                    self.editor.toggle_fold(target)
            except Exception:
                pass
        else:
            # Клик по номеру — выбор строки
            self.editor.setCursorPosition(target, 0)
            self.editor.ensureLineVisible(target)
            self.editor.setFocus()
