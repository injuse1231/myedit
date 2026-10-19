from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem,
)


class CommandPalette(QDialog):
    """
    Всплывающее окно с командами и поиском.
    Эмитит signal `commandTriggered` с id команды, когда пользователь выбрал.
    """

    commandTriggered = pyqtSignal(str)

    def __init__(self, commands, parent=None):
        """
        commands: список кортежей (id, label, shortcut_str)
          id         — внутренний ключ команды (передаётся в сигнал)
          label      — что показать пользователю
          shortcut   — строка с хоткеем для отображения (может быть '')
        """
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.Popup)
        self.setModal(True)
        self.setFixedWidth(600)
        self.resize(600, 360)

        self._all = commands      # все команды
        self._filtered = list(commands)

        self._build_ui()
        self._populate()

    def apply_theme(self, th):
        from theme_helper import qss_dialog
        self.setStyleSheet(qss_dialog(th))

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.edit = QLineEdit()
        self.edit.setPlaceholderText("Введите команду…")
        self.edit.textChanged.connect(self._filter)
        self.edit.returnPressed.connect(self._execute_current)
        layout.addWidget(self.edit)

        self.list = QListWidget()
        self.list.itemActivated.connect(self._execute_item)
        self.list.itemClicked.connect(self._execute_item)
        layout.addWidget(self.list, 1)

    def _populate(self):
        self.list.clear()
        for cmd_id, label, shortcut in self._filtered:
            text = f"{label}"
            if shortcut:
                text = f"{label}    {shortcut}"
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, cmd_id)
            self.list.addItem(item)
        if self.list.count() > 0:
            self.list.setCurrentRow(0)

    def _filter(self, query):
        q = query.strip().lower()
        if not q:
            self._filtered = list(self._all)
        else:
            # простое подстрочное совпадение
            self._filtered = [
                c for c in self._all
                if q in c[1].lower() or q in c[0].lower()
            ]
        self._populate()

    def _execute_current(self):
        item = self.list.currentItem()
        if item:
            self._execute_item(item)

    def _execute_item(self, item):
        cmd_id = item.data(Qt.ItemDataRole.UserRole)
        self.commandTriggered.emit(cmd_id)
        self.accept()

    # ---- Обработка клавиш ----

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_Escape:
            self.reject()
            return
        if key == Qt.Key.Key_Down:
            row = self.list.currentRow()
            if row < self.list.count() - 1:
                self.list.setCurrentRow(row + 1)
            return
        if key == Qt.Key.Key_Up:
            row = self.list.currentRow()
            if row > 0:
                self.list.setCurrentRow(row - 1)
            return
        # Всё остальное — в поле ввода
        super().keyPressEvent(event)
        self.edit.setFocus()
