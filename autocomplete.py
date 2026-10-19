"""
Умное автодополнение для QScintilla:
— слова из текущего документа
— ключевые слова Python
— встроенные функции Python
— часто используемые имена PyQt6
"""

import re
from PyQt6.QtCore import QTimer
from PyQt6.Qsci import QsciAPIs, QsciLexerPython


# --- Статические списки ---

PYTHON_KEYWORDS = [
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return",
    "try", "while", "with", "yield",
    "self", "cls",
]

PYTHON_BUILTINS = [
    "abs", "all", "any", "ascii", "bin", "bool", "bytearray", "bytes",
    "callable", "chr", "classmethod", "compile", "complex", "delattr",
    "dict", "dir", "divmod", "enumerate", "eval", "exec", "filter",
    "float", "format", "frozenset", "getattr", "globals", "hasattr",
    "hash", "help", "hex", "id", "input", "int", "isinstance",
    "issubclass", "iter", "len", "list", "locals", "map", "max",
    "memoryview", "min", "next", "object", "oct", "open", "ord",
    "pow", "print", "property", "range", "repr", "reversed", "round",
    "set", "setattr", "slice", "sorted", "staticmethod", "str", "sum",
    "super", "tuple", "type", "vars", "zip",
    "Exception", "ValueError", "TypeError", "KeyError", "IndexError",
    "AttributeError", "ImportError", "RuntimeError", "StopIteration",
    "__init__", "__main__", "__name__", "__file__",
]

PYQT_NAMES = [
    "QApplication", "QMainWindow", "QWidget", "QDialog", "QLabel",
    "QPushButton", "QLineEdit", "QTextEdit", "QPlainTextEdit",
    "QVBoxLayout", "QHBoxLayout", "QGridLayout", "QFormLayout",
    "QToolBar", "QMenuBar", "QMenu", "QStatusBar", "QTabWidget",
    "QSplitter", "QListWidget", "QTreeView", "QListView", "QComboBox",
    "QCheckBox", "QSpinBox", "QScrollArea", "QFileDialog",
    "QMessageBox", "QInputDialog", "QFont", "QColor", "QAction",
    "QKeySequence", "QShortcut", "QIcon", "QPixmap",
    "Qt", "pyqtSignal", "pyqtSlot",
]


def extract_words(text, min_len=3):
    words = set()
    for m in re.finditer(r"[A-Za-z_][A-Za-z0-9_]*", text):
        w = m.group(0)
        if len(w) >= min_len:
            words.add(w)
    return words


class AutoCompleter:
    """Хранит QsciAPIs и обновляет его с дебаунсом 300 мс."""

    def __init__(self, editor):
        self.editor = editor
        self.apis = None
        self._last_text_hash = None
        # Дебаунс-таймер — пересобираем API через 300 мс после последнего изменения
        self._timer = QTimer(editor)
        self._timer.setSingleShot(True)
        self._timer.setInterval(300)
        self._timer.timeout.connect(self._refresh)
        self._pending_text = None

    def attach(self):
        lexer = self.editor.lexer()
        if not isinstance(lexer, QsciLexerPython):
            return False

        self.apis = QsciAPIs(lexer)
        self._load_static()
        self.apis.prepare()

        self.editor.textChanged.connect(self._on_text_changed)
        # Первичное наполнение
        self._refresh()
        return True

    def _load_static(self):
        for kw in PYTHON_KEYWORDS:
            self.apis.add(kw)
        for bi in PYTHON_BUILTINS:
            self.apis.add(bi)
        for py in PYQT_NAMES:
            self.apis.add(py)

    def _on_text_changed(self):
        text = self.editor.text()
        h = hash(text)
        if h == self._last_text_hash:
            return
        self._last_text_hash = h
        self._pending_text = text
        # Перезапускаем таймер
        self._timer.start()

    def _refresh(self):
        """Пересобирает API. Вызывается таймером или вручную."""
        if self.apis is None:
            return
        lexer = self.editor.lexer()
        if not isinstance(lexer, QsciLexerPython):
            return

        # Пересоздаём API
        self.apis = QsciAPIs(lexer)
        self._load_static()

        # Слова из текста
        text = self._pending_text or self.editor.text()
        for w in extract_words(text, min_len=3):
            self.apis.add(w)

        self.apis.prepare()
        self._pending_text = None

    # Для совместимости с прошлым API
    def refresh_now(self):
        self._refresh()
