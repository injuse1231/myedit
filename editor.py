import os
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont, QColor
from PyQt6.Qsci import QsciScintilla, QsciLexerPython
from highlighter import get_lexer, apply_lexer_colors
from autocomplete import AutoCompleter


class CodeEditor(QsciScintilla):
    """Редактор кода на базе QScintilla."""

    cursorMoved = pyqtSignal(int, int)

    def __init__(self, path=None, parent=None):
        super().__init__(parent)
        self.path = None
        self._settings = {}
        self._autocompleter = None
        self._minimap = None
        self._gutter = None
        self._theme_dict = None
        self._setup()
        if path:
            self.load_file(path)

    # ============================================================
    # ИНИЦИАЛИЗАЦИЯ
    # ============================================================

    def _setup(self):
        # Шрифт
        font = QFont("JetBrains Mono", 11)
        if not font.exactMatch():
            font = QFont("Monospace", 11)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 и 1 отключены — номера рисует Gutter (gutter.py)
        self.setMarginWidth(0, 0)
        self.setMarginWidth(1, 0)

        # Margin 2 — folding (невидимый, только для логики сворачивания)
        self.setMarginType(2, QsciScintilla.MarginType.SymbolMargin)
        self.setMarginWidth(2, 0)
        self.setMarginLineNumbers(2, False)
        self.setMarginSensitivity(2, False)
        self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle, 2)

        # Автодополнение
        self.setAutoCompletionSource(QsciScintilla.AutoCompletionSource.AcsAPIs)
        self.setAutoCompletionThreshold(2)
        self.setAutoCompletionCaseSensitivity(False)
        self.setAutoCompletionReplaceWord(False)
        self.setAutoCompletionUseSingle(
            QsciScintilla.AutoCompletionUseSingle.AcusNever
        )
        self.setAutoCompletionShowSingle(False)

        # Отступы
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)  # guides ВКЛЮЧЕНЫ — покрасим серым
        self.setBackspaceUnindents(True)

        # Прочее
        self.setCaretLineVisible(True)
        self.setBraceMatching(QsciScintilla.BraceMatch.SloppyBraceMatch)
        self.setEdgeMode(QsciScintilla.EdgeMode.EdgeLine)
        self.setEdgeColumn(100)
        self.setScrollWidth(1)
        self.setScrollWidthTracking(True)

        # Межстрочный интервал — через константы
        try:
            from PyQt6.Qsci import QsciScintilla as _Q
            self.SendScintilla(_Q.SCI_SETEXTRAASCENT, 4)
            self.SendScintilla(_Q.SCI_SETEXTRADESCENT, 4)
        except Exception:
            pass
        # Fallback — числовые
        try:
            self.SendScintilla(2526, 4)
            self.SendScintilla(2528, 4)
        except Exception:
            pass

        # Убираем внешние margins viewport
        try:
            self.SendScintilla(2155, 0)  # SCI_SETMARGINLEFT
            self.SendScintilla(2157, 0)  # SCI_SETMARGINRIGHT
        except Exception:
            pass



        # Умный Home
        try:
            self.SendScintilla(QsciScintilla.SCI_ASSIGNCMDKEY,
                               QsciScintilla.SCK_HOME,
                               QsciScintilla.SCI_VCHOME)
        except Exception:
            pass

        self.cursorPositionChanged.connect(self._emit_cursor)

        # Нейтральные цвета
        self.setCaretLineBackgroundColor(QColor("#2a2d2e"))
        self.setMarginsBackgroundColor(QColor("#1e1e1e"))
        self.setMarginsForegroundColor(QColor("#6a6a6a"))

    # ============================================================
    # ЦВЕТА GUTTER
    # ============================================================

    def _apply_gutter_colors(self, bg_hex, fg_hex, edge_hex=None):
        """Красит margins и fold-margin. Guides отключены."""
        bg = QColor(bg_hex)
        fg = QColor(fg_hex)

        # Margin 0 — фон и цвет номеров (обычно не используется — Gutter свой)
        self.setMarginsBackgroundColor(bg)
        self.setMarginsForegroundColor(fg)

        # Все margins — фон = фон редактора (убирает белые полосы)
        for m in (0, 1, 2):
            try:
                self.SendScintilla(
                    QsciScintilla.SCI_SETMARGINBACKN, m, bg.rgb()
                )
            except Exception:
                pass

        # Fold margin — фон = фон редактора
        try:
            self.setFoldMarginColors(bg, bg)
        except Exception:
            pass
        try:
            self.SendScintilla(2295, bg.rgb())  # SCI_SETFOLDMARGINCOLOUR
            self.SendScintilla(2296, bg.rgb())  # SCI_SETFOLDMARGINHICOLOUR
        except Exception:
            pass

        # === INDENTATION GUIDES — СЕРЫЕ ===
        # Определяем цвет в зависимости от яркости фона
        try:
            bright = (bg.red() + bg.green() + bg.blue()) // 3
        except Exception:
            bright = 128

        if bright < 128:
            guide = QColor("#4a4a4a")  # тёмная тема — серый
        else:
            guide = QColor("#c0c0c0")  # светлая тема — светло-серый

        # Способ 1: официальный API QsciScintilla
        try:
            self.setIndentationGuidesForegroundColor(guide)
            self.setIndentationGuidesBackgroundColor(bg)
        except Exception:
            pass

        # Способ 2: через Scintilla STYLE 37 (STYLE_INDENTGUIDE)
        try:
            self.SendScintilla(QsciScintilla.SCI_STYLESETFORE, 37, guide.rgb())
            self.SendScintilla(QsciScintilla.SCI_STYLESETBACK, 37, bg.rgb())
        except Exception:
            pass

        # Включаем показ guides (1 = показывать на всех уровнях)
        try:
            self.SendScintilla(QsciScintilla.SCI_SETINDENTATIONGUIDES, 1)
        except Exception:
            pass
        try:
            self.setIndentationGuides(True)
        except Exception:
            pass

    # ============================================================
    # НАСТРОЙКИ
    # ============================================================

    def apply_settings(self, cfg):
        self._settings = dict(cfg)

        # Шрифт
        fcfg = cfg.get("font_editor", {})
        family = fcfg.get("family", "Monospace")
        size = fcfg.get("size", 11)
        font = QFont(family, size)
        if not font.exactMatch():
            font = QFont("Monospace", size)
        self.setFont(font)
        self.setMarginsFont(font)
        if self._gutter:
            self._gutter.apply_font(font)

        # Табы
        use_spaces = cfg.get("use_spaces", True)
        self.setIndentationsUseTabs(not use_spaces)
        self.setTabWidth(cfg.get("tab_width", 4))

        # Линия-ограничитель
        if cfg.get("show_edge", True):
            self.setEdgeMode(QsciScintilla.EdgeMode.EdgeLine)
            self.setEdgeColumn(cfg.get("edge_column", 100))
        else:
            self.setEdgeMode(QsciScintilla.EdgeMode.EdgeNone)

        # Невидимые символы
        ws = 1 if cfg.get("show_whitespace", False) else 0
        try:
            self.SendScintilla(QsciScintilla.SCI_SETVIEWWS, ws)
        except Exception:
            pass

        # Умный Home
        try:
            if cfg.get("smart_home", True):
                self.SendScintilla(QsciScintilla.SCI_ASSIGNCMDKEY,
                                   QsciScintilla.SCK_HOME,
                                   QsciScintilla.SCI_VCHOME)
            else:
                self.SendScintilla(QsciScintilla.SCI_ASSIGNCMDKEY,
                                   QsciScintilla.SCK_HOME,
                                   QsciScintilla.SCI_HOME)
        except Exception:
            pass

        # Перенос строк
        if cfg.get("wrap_lines", False):
            self.setWrapMode(QsciScintilla.WrapMode.WrapWord)
        else:
            self.setWrapMode(QsciScintilla.WrapMode.WrapNone)

        # Переприменяем тему
        if self._theme_dict:
            self.apply_theme(self._theme_dict)

    # ============================================================
    # ТЕМА
    # ============================================================

    def apply_theme(self, th):
        self._theme_dict = th
        bg = QColor(th["editor_bg"])
        fg = QColor(th["editor_fg"])

        self.setPaper(bg)
        self.setColor(fg)
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor(th["caret_line"]))
        self.setSelectionBackgroundColor(QColor(th["selected_bg"]))
        self.setSelectionForegroundColor(QColor(th["selected_fg"]))
        self.setEdgeColor(QColor(th["edge_color"]))

        self._apply_gutter_colors(th["margin_bg"], th["margin_fg"],
                                  th["edge_color"])

        try:
            self.setWhitespaceForegroundColor(QColor(th["margin_fg"]))
            self.setWhitespaceBackgroundColor(bg)
        except Exception:
            pass

        if self._minimap:
            self._minimap.set_theme(th)
        if self._gutter:
            self._gutter.apply_theme(th)

        # Лексер
        if self.path:
            ext = os.path.splitext(self.path)[1]
            lexer = get_lexer(ext, self)
            if lexer is not None:
                apply_lexer_colors(lexer, th["lexer_colors"], th["editor_bg"])
            self.setLexer(lexer)
            self._reapply_folding()
            self._apply_gutter_colors(th["margin_bg"], th["margin_fg"],
                                      th["edge_color"])
            # ПОВТОРНО применяем guides через лексер (он мог сбросить цвета)
            try:
                bright = (bg.red() + bg.green() + bg.blue()) // 3
                guide = QColor("#4a4a4a") if bright < 128 else QColor("#c0c0c0")
                if lexer is not None:
                    lexer.setColor(guide, 37)
                    lexer.setPaper(bg, 37)
            except Exception:
                pass
            self._attach_autocompleter()
        else:
            self.setLexer(None)

    def _reapply_folding(self):
        """Переустанавливает folding после смены лексера."""
        try:
            self.setFolding(QsciScintilla.FoldStyle.BoxedTreeFoldStyle, 2)
        except Exception:
            pass

    def _emit_cursor(self):
        line, col = self.getCursorPosition()
        self.cursorMoved.emit(line + 1, col + 1)

    # ============================================================
    # AUTOCOMPLETE
    # ============================================================

    def _attach_autocompleter(self):
        if not isinstance(self.lexer(), QsciLexerPython):
            self._autocompleter = None
            return
        self._autocompleter = AutoCompleter(self)
        self._autocompleter.attach()

    # ============================================================
    # GUTTER / MINIMAP
    # ============================================================

    def attach_gutter(self, gutter):
        self._gutter = gutter
        if self._theme_dict:
            gutter.apply_theme(self._theme_dict)
        gutter.apply_font(self.font())

    def attach_minimap(self, minimap):
        self._minimap = minimap
        if self._theme_dict:
            minimap.set_theme(self._theme_dict)

    def find_with_status(self, text, forward=True, case=False, regex=False):
        """Ищет text. Возвращает True, если найдено."""
        if not text:
            return False
        found = self.findFirst(text, regex, case, False, True, forward)
        if not found:
            # Попробуем с начала файла (если искали вперёд)
            if forward:
                self.setCursorPosition(0, 0)
                found = self.findFirst(text, regex, case, False, True, True)
            else:
                last = self.lines() - 1
                self.setCursorPosition(last, 0)
                found = self.findFirst(text, regex, case, False, True, False)
        return found

    # ============================================================
    # FOLDING API (для gutter)
    # ============================================================

    def is_foldable(self, line):
        """Можно ли свернуть блок на этой строке."""
        try:
            state = self.SendScintilla(QsciScintilla.SCI_GETLINESTATE, line)
            return bool(state & QsciScintilla.SC_FOLDLEVELHEADERFLAG)
        except Exception:
            return False

    def is_folded(self, line):
        """Свёрнут ли блок на этой строке."""
        try:
            expanded = self.SendScintilla(
                QsciScintilla.SCI_GETFOLDEXPANDED, line
            )
            return not expanded
        except Exception:
            return False

    def toggle_fold(self, line):
        """Свернуть/развернуть блок."""
        try:
            self.SendScintilla(QsciScintilla.SCI_TOGGLEFOLD, line)
        except Exception:
            pass

    # ============================================================
    # ФАЙЛ
    # ============================================================

    def apply_lexer(self):
        if not self.path:
            self.setLexer(None)
            return
        ext = os.path.splitext(self.path)[1]
        lexer = get_lexer(ext, self)
        self.setLexer(lexer)
        self._reapply_folding()
        self._attach_autocompleter()
        if self._theme_dict:
            self._apply_gutter_colors(
                self._theme_dict["margin_bg"],
                self._theme_dict["margin_fg"],
                self._theme_dict["edge_color"],
            )
            # Guides через лексер — после setLexer
            try:
                th = self._theme_dict
                bg = QColor(th["editor_bg"])
                bright = (bg.red() + bg.green() + bg.blue()) // 3
                guide = QColor("#4a4a4a") if bright < 128 else QColor("#c0c0c0")
                if lexer is not None:
                    lexer.setColor(guide, 37)
                    lexer.setPaper(bg, 37)
            except Exception:
                pass

    def load_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(path, "r", encoding="latin-1") as f:
                content = f.read()
        self.path = path
        self.setText(content)
        self.apply_lexer()

    def save_file(self, path=None):
        if path:
            self.path = path
            self.apply_lexer()
        if not self.path:
            return False
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(self.text())
        return True

    def name(self):
        return os.path.basename(self.path) if self.path else "Без имени"
