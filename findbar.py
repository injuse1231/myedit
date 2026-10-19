from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QLabel,
    QToolButton, QCheckBox,
)


class FindBar(QWidget):
    """Панель поиска и замены, появляется под редактором."""

    findNext = pyqtSignal(str, bool, bool, bool)   # text, forward, case, regex
    replaceOne = pyqtSignal(str, str, bool, bool, bool)
    replaceAll = pyqtSignal(str, str, bool, bool, bool)
    closed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build()
        self.hide()

    def _build(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(6, 4, 6, 4)
        root.setSpacing(4)

        # --- Строка «Найти» ---
        row1 = QHBoxLayout()
        row1.setSpacing(4)

        row1.addWidget(QLabel("🔍"))

        self.edit_find = QLineEdit()
        self.edit_find.setPlaceholderText("Найти…")
        self.edit_find.returnPressed.connect(self._on_find_next)
        self.edit_find.textChanged.connect(self._on_text_changed)
        row1.addWidget(self.edit_find, 1)

        # Метка статуса («не найдено», «найдено N»)
        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #888; padding: 0 6px;")
        self.lbl_status.setMinimumWidth(120)
        row1.addWidget(self.lbl_status)

        self.chk_case = QCheckBox("Aa")
        self.chk_case.setToolTip("Учитывать регистр")
        row1.addWidget(self.chk_case)

        self.chk_regex = QCheckBox(".*")
        self.chk_regex.setToolTip("Регулярное выражение")
        row1.addWidget(self.chk_regex)

        btn_prev = QToolButton()
        btn_prev.setText("↑")
        btn_prev.setToolTip("Найти предыдущее (Shift+Enter)")
        btn_prev.clicked.connect(lambda: self._on_find(False))
        row1.addWidget(btn_prev)

        btn_next = QToolButton()
        btn_next.setText("↓")
        btn_next.setToolTip("Найти следующее (Enter)")
        btn_next.clicked.connect(lambda: self._on_find(True))
        row1.addWidget(btn_next)

        btn_close = QToolButton()
        btn_close.setText("✕")
        btn_close.setToolTip("Закрыть (Esc)")
        btn_close.clicked.connect(self.close_bar)
        row1.addWidget(btn_close)

        root.addLayout(row1)

        # --- Строка «Заменить» ---
        row2 = QHBoxLayout()
        row2.setSpacing(4)

        row2.addWidget(QLabel("↔"))

        self.edit_repl = QLineEdit()
        self.edit_repl.setPlaceholderText("Заменить на…")
        self.edit_repl.returnPressed.connect(self._on_replace_one)
        row2.addWidget(self.edit_repl, 1)

        btn_replace = QToolButton()
        btn_replace.setText("Заменить")
        btn_replace.clicked.connect(self._on_replace_one)
        row2.addWidget(btn_replace)

        btn_replace_all = QToolButton()
        btn_replace_all.setText("Всё")
        btn_replace_all.setToolTip("Заменить всё")
        btn_replace_all.clicked.connect(self._on_replace_all)
        row2.addWidget(btn_replace_all)

        root.addLayout(row2)

        # Показываем строку замены только по Ctrl+H
        self.row2_widgets = [
            self.edit_repl, btn_replace, btn_replace_all,
        ]
        self._replace_visible = False

        # Горячие клавиши внутри панели
        QShortcut(QKeySequence("Escape"), self, activated=self.close_bar)
        QShortcut(QKeySequence("Shift+Return"), self,
                  activated=lambda: self._on_find(False))

    def apply_theme(self, th):
        from theme_helper import qss_findbar
        self.setStyleSheet(qss_findbar(th))

    # ---------- API ----------

    def open_find(self):
        self._show_replace(False)
        self._activate()

    def open_replace(self):
        self._show_replace(True)
        self._activate()

    def close_bar(self):
        self.hide()
        self.closed.emit()

    def set_status(self, text, error=False):
        """Устанавливает текст статуса. error=True — красным."""
        self.lbl_status.setText(text)
        if error:
            self.lbl_status.setStyleSheet("color: #f48771; padding: 0 6px;")
        else:
            self.lbl_status.setStyleSheet("color: #888; padding: 0 6px;")

    def clear_status(self):
        self.lbl_status.setText("")

    # ---------- Внутреннее ----------

    def _on_text_changed(self, text):
        """При вводе — очищаем статус."""
        self.lbl_status.setText("")

    def _activate(self):
        self.show()
        self.edit_find.setFocus()
        self.edit_find.selectAll()

    def _show_replace(self, visible):
        self._replace_visible = visible
        for w in self.row2_widgets:
            w.setVisible(visible)

    def _flags(self):
        return self.chk_case.isChecked(), self.chk_regex.isChecked()

    def _on_find(self, forward):
        text = self.edit_find.text()
        if not text:
            return
        case, regex = self._flags()
        self.findNext.emit(text, forward, case, regex)

    def _on_find_next(self):
        self._on_find(True)

    def _on_replace_one(self):
        find = self.edit_find.text()
        repl = self.edit_repl.text()
        if not find:
            return
        case, regex = self._flags()
        self.replaceOne.emit(find, repl, case, regex, True)

    def _on_replace_all(self):
        find = self.edit_find.text()
        repl = self.edit_repl.text()
        if not find:
            return
        case, regex = self._flags()
        self.replaceAll.emit(find, repl, case, regex, True)
