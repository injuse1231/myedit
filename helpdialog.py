from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget,
)


# Список всех горячих клавиш: (группа, [(клавиши, описание), ...])
SHORTCUTS = [
    ("Файл", [
        ("Ctrl+N",         "Новый файл"),
        ("Ctrl+O",         "Открыть файл"),
        ("Ctrl+K",         "Открыть папку"),
        ("Ctrl+S",         "Сохранить"),
        ("Ctrl+Shift+S",   "Сохранить как"),
        ("Ctrl+W",         "Закрыть вкладку"),
        ("Ctrl+Q",         "Выход"),
    ]),
    ("Правка", [
        ("Ctrl+Z",         "Отменить"),
        ("Ctrl+Y",         "Вернуть"),
        ("Ctrl+X",         "Вырезать"),
        ("Ctrl+C",         "Копировать"),
        ("Ctrl+V",         "Вставить"),
        ("Ctrl+A",         "Выделить всё"),
    ]),
    ("Поиск", [
        ("Ctrl+F",         "Найти"),
        ("Ctrl+H",         "Найти и заменить"),
        ("Enter",          "Следующее совпадение"),
        ("Shift+Enter",    "Предыдущее совпадение"),
        ("Esc",            "Закрыть панель поиска"),
    ]),
    ("Вид", [
        ("Ctrl+B",         "Показать/скрыть дерево файлов"),
        ("Ctrl+Shift+P",   "Командная палитра"),
        ("F1",             "Эта справка"),
    ]),
    ("В редакторе", [
        ("Tab",            "Отступ вправо"),
        ("Shift+Tab",      "Отступ влево"),
        ("Ctrl+/",         "Комментарий (в некоторых языках)"),
        ("Ctrl+D",         "Дублировать строку (если поддерживается)"),
        ("Ctrl+Home",      "В начало файла"),
        ("Ctrl+End",       "В конец файла"),
    ]),
]


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Горячие клавиши — MyEdit")
        self.resize(640, 620)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # Заголовок
        title = QLabel("⌨  Горячие клавиши MyEdit")
        f = QFont()
        f.setPointSize(14)
        f.setBold(True)
        title.setFont(f)
        layout.addWidget(title)

        # Область с прокруткой
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.Shape.NoFrame)

        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(0, 0, 0, 0)
        cl.setSpacing(14)

        for group_name, items in SHORTCUTS:
            # Название группы
            g = QLabel(group_name)
            gf = QFont()
            gf.setPointSize(11)
            gf.setBold(True)
            g.setFont(gf)
            g.setProperty("is_group_header", True)
            cl.addWidget(g)

            for keys, desc in items:
                row = QHBoxLayout()
                row.setSpacing(12)

                k = QLabel(keys)
                k.setFixedWidth(140)
                k.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                kf = QFont("Monospace", 10)
                kf.setBold(True)
                k.setFont(kf)
                k.setProperty("is_key", True)
                row.addWidget(k)

                d = QLabel(desc)
                row.addWidget(d, 1)

                wrapper = QWidget()
                wrapper.setLayout(row)
                cl.addWidget(wrapper)

        cl.addStretch(1)
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        # Кнопка закрытия
        btn_row = QHBoxLayout()
        btn_row.addStretch(1)
        btn_close = QPushButton("Закрыть")
        btn_close.clicked.connect(self.accept)
        btn_close.setMinimumWidth(100)
        btn_row.addWidget(btn_close)
        layout.addLayout(btn_row)

        # Применяем тему из родителя, если есть
        if parent is not None:
            try:
                th_name = getattr(parent, "current_theme", None)
                if th_name:
                    from themes import THEMES
                    if th_name in THEMES:
                        self.apply_theme(THEMES[th_name])
            except Exception:
                pass

    def apply_theme(self, th):
        from theme_helper import qss_helpdialog, help_key_style, help_header_color
        self.setStyleSheet(qss_helpdialog(th))
        # Перекрашиваем ключи и заголовки групп
        for label in self.findChildren(QLabel):
            try:
                text = label.text()
                if not text:
                    continue
                # Группа — заголовок с цветом
                if label.property("is_group_header"):
                    label.setStyleSheet(
                        f"color: {help_header_color(th)}; padding-top: 6px;"
                    )
                elif label.property("is_key"):
                    label.setStyleSheet(help_key_style(th))
            except Exception:
                continue

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.accept()
            return
        super().keyPressEvent(event)
