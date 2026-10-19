"""
Панель поиска по проекту (Ctrl+Shift+F).
Ищет подстроку во всех файлах открытой папки.
"""

import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel,
    QPushButton, QTreeWidget, QTreeWidgetItem, QCheckBox,
)


SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules",
    ".venv", "venv", "env", ".idea", ".vscode", "build", "dist",
    ".mypy_cache", ".pytest_cache", ".cache",
}

TEXT_EXTS = {
    ".py", ".js", ".ts", ".html", ".htm", ".css", ".json",
    ".txt", ".md", ".rst", ".ini", ".cfg", ".conf", ".sh",
    ".bash", ".c", ".cpp", ".h", ".hpp", ".java", ".go",
    ".rs", ".rb", ".php", ".sql", ".xml", ".yml", ".yaml",
    ".toml", ".env", ".desktop",
}


class SearchProjectPanel(QWidget):
    fileRequested = pyqtSignal(str, int)   # путь, номер строки (1-based)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._root = None
        self._build_ui()
        self.hide()

    def _build_ui(self):
        pass  # QSS применяется методом apply_theme

        root = QVBoxLayout(self)
        root.setContentsMargins(6, 4, 6, 4)
        root.setSpacing(4)

        # Верхняя строка с полем и кнопкой
        row = QHBoxLayout()
        row.addWidget(QLabel("🔍"))

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Искать во всех файлах проекта…")
        self.edit.returnPressed.connect(self.do_search)
        row.addWidget(self.edit, 1)

        self.chk_case = QCheckBox("Aa")
        self.chk_case.setToolTip("Учитывать регистр")
        row.addWidget(self.chk_case)

        btn = QPushButton("Найти")
        btn.clicked.connect(self.do_search)
        row.addWidget(btn)

        btn_close = QPushButton("✕")
        btn_close.clicked.connect(self.hide)
        row.addWidget(btn_close)

        root.addLayout(row)

        self.lbl_status = QLabel("")
        root.addWidget(self.lbl_status)

        # Дерево результатов
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.itemActivated.connect(self._on_item)
        self.tree.itemClicked.connect(self._on_item)
        root.addWidget(self.tree, 1)

    def apply_theme(self, th):
        from theme_helper import qss_searchproject
        self.setStyleSheet(qss_searchproject(th))

    def set_root(self, path):
        self._root = path

    def open_panel(self):
        self.show()
        self.edit.setFocus()
        self.edit.selectAll()

    def do_search(self):
        query = self.edit.text()
        if not query or not self._root:
            return
        case = self.chk_case.isChecked()

        self.tree.clear()
        self.lbl_status.setText("Ищу…")
        from PyQt6.QtWidgets import QApplication
        QApplication.processEvents()

        hits_by_file = {}
        total = 0
        needle = query if case else query.lower()

        for dirpath, dirnames, filenames in os.walk(self._root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext and ext not in TEXT_EXTS:
                    continue
                full = os.path.join(dirpath, fname)
                try:
                    with open(full, "r", encoding="utf-8", errors="ignore") as f:
                        lines = f.readlines()
                except Exception:
                    continue

                for i, line in enumerate(lines):
                    hay = line if case else line.lower()
                    if needle in hay:
                        hits_by_file.setdefault(full, []).append((i + 1, line.rstrip()))
                        total += 1
                        if total >= 500:
                            break
                if total >= 500:
                    break
            if total >= 500:
                break

        self._populate(hits_by_file, query)
        self.lbl_status.setText(
            f"Найдено {total} совпадений в {len(hits_by_file)} файлах"
            + (" (лимит 500)" if total >= 500 else "")
        )

    def _populate(self, hits_by_file, query):
        for filepath, hits in hits_by_file.items():
            rel = os.path.relpath(filepath, self._root)
            parent = QTreeWidgetItem([f"📄 {rel}  ({len(hits)})"])
            parent.setExpanded(True)
            self.tree.addTopLevelItem(parent)
            for line_no, text in hits:
                child = QTreeWidgetItem([f"  {line_no}:  {text.strip()[:200]}"])
                child.setData(0, Qt.ItemDataRole.UserRole, (filepath, line_no))
                parent.addChild(child)

    def _on_item(self, item, column=0):
        data = item.data(0, Qt.ItemDataRole.UserRole)
        if data:
            path, line = data
            self.fileRequested.emit(path, line)
