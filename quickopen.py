"""
Быстрое открытие файла по имени (Ctrl+P).
Собирает все файлы в открытой папке, фильтрует по подстроке.
"""

import os
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
)


# Файлы, которые игнорируем при обходе
SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", "node_modules",
    ".venv", "venv", "env", ".idea", ".vscode", "build", "dist",
}


class QuickOpenDialog(QDialog):
    fileChosen = pyqtSignal(str)

    def __init__(self, root_folder, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setModal(True)
        self.setFixedWidth(650)
        self.resize(650, 420)

        self.root = root_folder
        self._all_files = []           # список кортежей (display, fullpath)
        self._filtered = []

        self._build_ui()
        self._scan_files()
        self._populate()

    def apply_theme(self, th):
        from theme_helper import qss_dialog
        self.setStyleSheet(qss_dialog(th))

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Найти файл…")
        self.edit.textChanged.connect(self._filter)
        self.edit.returnPressed.connect(self._choose_current)
        layout.addWidget(self.edit)

        self.list = QListWidget()
        self.list.itemActivated.connect(self._choose_item)
        self.list.itemClicked.connect(self._choose_item)
        layout.addWidget(self.list, 1)

    def _scan_files(self):
        if not self.root or not os.path.isdir(self.root):
            return
        for dirpath, dirnames, filenames in os.walk(self.root):
            # Отсеиваем системные папки
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for fname in filenames:
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, self.root)
                self._all_files.append((rel, full))
        # Сортируем: сначала файлы в корне, потом в подпапках
        self._all_files.sort(key=lambda x: (x[0].count(os.sep), x[0].lower()))

    def _filter(self, query):
        q = query.strip().lower()
        if not q:
            self._filtered = list(self._all_files[:500])
        else:
            # Приоритет: совпадение в имени файла > в пути
            hits_name = []
            hits_path = []
            for rel, full in self._all_files:
                base = os.path.basename(rel).lower()
                if q in base:
                    hits_name.append((rel, full))
                elif q in rel.lower():
                    hits_path.append((rel, full))
            self._filtered = (hits_name + hits_path)[:500]
        self._populate()

    def _populate(self):
        self.list.clear()
        for rel, full in self._filtered:
            item = QListWidgetItem(rel)
            item.setData(Qt.ItemDataRole.UserRole, full)
            self.list.addItem(item)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _choose_current(self):
        item = self.list.currentItem()
        if item:
            self._choose_item(item)

    def _choose_item(self, item):
        path = item.data(Qt.ItemDataRole.UserRole)
        if path:
            self.fileChosen.emit(path)
        self.accept()

    def keyPressEvent(self, event):
        k = event.key()
        if k == Qt.Key.Key_Escape:
            self.reject()
            return
        if k == Qt.Key.Key_Down:
            row = self.list.currentRow()
            if row < self.list.count() - 1:
                self.list.setCurrentRow(row + 1)
            return
        if k == Qt.Key.Key_Up:
            row = self.list.currentRow()
            if row > 0:
                self.list.setCurrentRow(row - 1)
            return
        super().keyPressEvent(event)
        self.edit.setFocus()
