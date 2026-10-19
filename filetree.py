import os
import shutil
import subprocess

from PyQt6.QtCore import QDir, pyqtSignal, Qt
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import (
    QTreeView, QWidget, QVBoxLayout,
    QMenu, QInputDialog, QMessageBox, QFileDialog,
)


class FileTree(QWidget):
    fileOpened = pyqtSignal(str)
    fileOperationDone = pyqtSignal(str)   # текст для статус-бара

    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.model.setFilter(
            QDir.Filter.AllDirs | QDir.Filter.Files | QDir.Filter.NoDotAndDotDot
        )
        self.root_path = None

        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setHeaderHidden(True)
        for col in range(1, 4):
            self.tree.hideColumn(col)
        self.tree.setAnimated(True)
        self.tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self._show_context_menu)
        self.tree.doubleClicked.connect(self._on_double_click)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tree)

    def set_root(self, path):
        self.root_path = path
        self.tree.setRootIndex(self.model.index(path))

    # ---------- Открытие файла ----------

    def _on_double_click(self, index):
        path = self.model.filePath(index)
        if os.path.isfile(path):
            self.fileOpened.emit(path)

    # ---------- Контекстное меню ----------

    def _current_path(self, pos):
        """Возвращает путь к элементу под курсором или None."""
        index = self.tree.indexAt(pos)
        if not index.isValid():
            # Клик по пустому месту — работаем в корне
            return self.root_path if self.root_path else None
        return self.model.filePath(index)

    def _is_dir(self, path):
        return path and os.path.isdir(path)

    def _show_context_menu(self, pos):
        path = self._current_path(pos)
        if not path:
            return

        menu = QMenu(self)

        if self._is_dir(path):
            act_new_file = QAction("📄 Новый файл…", self)
            act_new_file.triggered.connect(lambda: self._new_file(path))
            menu.addAction(act_new_file)

            act_new_dir = QAction("📁 Новая папка…", self)
            act_new_dir.triggered.connect(lambda: self._new_folder(path))
            menu.addAction(act_new_dir)

            menu.addSeparator()

            act_refresh = QAction("🔄 Обновить", self)
            act_refresh.triggered.connect(self._refresh)
            menu.addAction(act_refresh)

            menu.addSeparator()
        else:
            act_open = QAction("📂 Открыть", self)
            act_open.triggered.connect(lambda: self.fileOpened.emit(path))
            menu.addAction(act_open)
            menu.addSeparator()

        # Общие пункты для файла и папки
        act_rename = QAction("✏  Переименовать…", self)
        act_rename.triggered.connect(lambda: self._rename(path))
        menu.addAction(act_rename)

        act_delete = QAction("🗑  Удалить", self)
        act_delete.triggered.connect(lambda: self._delete(path))
        menu.addAction(act_delete)

        menu.addSeparator()

        act_copy = QAction("📋 Копировать путь", self)
        act_copy.triggered.connect(lambda: self._copy_path(path))
        menu.addAction(act_copy)

        act_show = QAction("🗂  Открыть в файловом менеджере", self)
        act_show.triggered.connect(lambda: self._open_in_filemanager(path))
        menu.addAction(act_show)

        menu.exec(self.tree.viewport().mapToGlobal(pos))

    # ---------- Операции ----------

    def _new_file(self, folder):
        name, ok = QInputDialog.getText(self, "Новый файл", "Имя файла:")
        if not ok or not name.strip():
            return
        name = name.strip()
        full = os.path.join(folder, name)
        if os.path.exists(full):
            QMessageBox.warning(self, "Ошибка", f"Файл уже существует:\n{full}")
            return
        try:
            open(full, "w", encoding="utf-8").close()
            self.fileOperationDone.emit(f"Создан файл: {name}")
            self.fileOpened.emit(full)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать:\n{e}")

    def _new_folder(self, folder):
        name, ok = QInputDialog.getText(self, "Новая папка", "Имя папки:")
        if not ok or not name.strip():
            return
        name = name.strip()
        full = os.path.join(folder, name)
        if os.path.exists(full):
            QMessageBox.warning(self, "Ошибка", f"Уже существует:\n{full}")
            return
        try:
            os.makedirs(full, exist_ok=True)
            self.fileOperationDone.emit(f"Создана папка: {name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось создать:\n{e}")

    def _rename(self, path):
        old_name = os.path.basename(path)
        new_name, ok = QInputDialog.getText(
            self, "Переименовать", "Новое имя:", text=old_name
        )
        if not ok or not new_name.strip():
            return
        new_name = new_name.strip()
        if new_name == old_name:
            return
        parent = os.path.dirname(path)
        new_path = os.path.join(parent, new_name)
        if os.path.exists(new_path):
            QMessageBox.warning(self, "Ошибка", f"Уже существует:\n{new_path}")
            return
        try:
            os.rename(path, new_path)
            self.fileOperationDone.emit(f"Переименовано: {old_name} → {new_name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось переименовать:\n{e}")

    def _delete(self, path):
        name = os.path.basename(path)
        is_dir = os.path.isdir(path)
        what = "папку" if is_dir else "файл"
        answer = QMessageBox.question(
            self,
            "Удалить?",
            f"Удалить {what} «{name}»?\n\n{path}",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        try:
            if is_dir:
                shutil.rmtree(path)
            else:
                os.remove(path)
            self.fileOperationDone.emit(f"Удалено: {name}")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось удалить:\n{e}")

    def _copy_path(self, path):
        from PyQt6.QtWidgets import QApplication
        QApplication.clipboard().setText(path)
        self.fileOperationDone.emit("Путь скопирован в буфер")

    def _open_in_filemanager(self, path):
        """Открывает папку в системном файловом менеджере (Nautilus)."""
        folder = path if os.path.isdir(path) else os.path.dirname(path)
        try:
            subprocess.Popen(["xdg-open", folder])
            self.fileOperationDone.emit("Открыто в файловом менеджере")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось открыть:\n{e}")

    def _refresh(self):
        """Обновляет модель дерева."""
        if self.root_path:
            self.model.setRootPath("")
            self.model.setRootPath(QDir.rootPath())
            self.tree.setRootIndex(self.model.index(self.root_path))
            self.fileOperationDone.emit("Дерево обновлено")
