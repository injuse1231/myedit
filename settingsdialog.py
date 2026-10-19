"""
Окно настроек MyEdit.
Возвращает изменённый словарь config через сигнал applied(dict).
"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QComboBox, QSpinBox, QCheckBox, QPushButton, QGroupBox,
    QDialogButtonBox,
)


class SettingsDialog(QDialog):
    """
    settings_applied(new_cfg) — эмитится при нажатии «Применить»/«OK»
    с новым словарём (копия исходного с изменениями).
    """

    settings_applied = pyqtSignal(dict)

    def __init__(self, current_cfg, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Настройки — MyEdit")
        self.resize(500, 520)
        self.cfg = dict(current_cfg)
        self._build_ui()
        self._apply_qss()

    def _apply_qss(self):
        # Стиль наследуется от главного окна через parent. Здесь только
        # отступы и размеры — цвета уже придут.
        self.setStyleSheet(self.parent().styleSheet() if self.parent() else "")

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(14)

        # ============ ИНТЕРФЕЙС ============
        gb_ui = QGroupBox("Интерфейс")
        form_ui = QFormLayout(gb_ui)

        self.cb_ui_family = QComboBox()
        self.cb_ui_family.setEditable(True)
        # Популярные системные шрифты + текущий
        fonts = ["Ubuntu", "Cantarell", "Inter", "Noto Sans",
                 "DejaVu Sans", "Liberation Sans", "Arial", "Sans"]
        self.cb_ui_family.addItems(fonts)
        cur_ui = self.cfg.get("font_ui", {})
        self.cb_ui_family.setCurrentText(cur_ui.get("family", "Ubuntu"))
        form_ui.addRow("Шрифт интерфейса:", self.cb_ui_family)

        self.sp_ui_size = QSpinBox()
        self.sp_ui_size.setRange(8, 22)
        self.sp_ui_size.setValue(cur_ui.get("size", 12))
        form_ui.addRow("Размер интерфейса:", self.sp_ui_size)

        root.addWidget(gb_ui)

        # ============ РЕДАКТОР ============
        gb_ed = QGroupBox("Редактор")
        form_ed = QFormLayout(gb_ed)

        self.cb_ed_family = QComboBox()
        self.cb_ed_family.setEditable(True)
        mono_fonts = ["JetBrains Mono", "Fira Code", "Cascadia Code",
                      "Source Code Pro", "Hack", "Inconsolata",
                      "DejaVu Sans Mono", "Liberation Mono",
                      "Ubuntu Mono", "Monospace"]
        # Оставим только те, что реально установлены (плюс всегда «Monospace»)
        available = set(QFontDatabase.families())
        filtered = [f for f in mono_fonts if f in available]
        if "Monospace" not in filtered:
            filtered.append("Monospace")
        self.cb_ed_family.addItems(filtered)
        cur_ed = self.cfg.get("font_editor", {})
        self.cb_ed_family.setCurrentText(cur_ed.get("family", "Monospace"))
        form_ed.addRow("Шрифт редактора:", self.cb_ed_family)

        self.sp_ed_size = QSpinBox()
        self.sp_ed_size.setRange(8, 28)
        self.sp_ed_size.setValue(cur_ed.get("size", 11))
        form_ed.addRow("Размер редактора:", self.sp_ed_size)

        self.sp_tab = QSpinBox()
        self.sp_tab.setRange(1, 16)
        self.sp_tab.setValue(self.cfg.get("tab_width", 4))
        form_ed.addRow("Ширина таба:", self.sp_tab)

        self.cb_spaces = QCheckBox("Использовать пробелы вместо табов")
        self.cb_spaces.setChecked(self.cfg.get("use_spaces", True))
        form_ed.addRow("", self.cb_spaces)

        root.addWidget(gb_ed)

        # ============ ОТОБРАЖЕНИЕ ============
        gb_view = QGroupBox("Отображение")
        form_view = QFormLayout(gb_view)

        self.cb_edge = QCheckBox("Показывать линию-ограничитель")
        self.cb_edge.setChecked(self.cfg.get("show_edge", True))
        form_view.addRow("", self.cb_edge)

        self.sp_edge = QSpinBox()
        self.sp_edge.setRange(40, 300)
        self.sp_edge.setValue(self.cfg.get("edge_column", 100))
        form_view.addRow("Позиция линии:", self.sp_edge)

        self.cb_ws = QCheckBox("Показывать невидимые символы (· пробел, → таб)")
        self.cb_ws.setChecked(self.cfg.get("show_whitespace", False))
        form_view.addRow("", self.cb_ws)

        self.cb_smart_home = QCheckBox("Умный Home (к первому символу строки)")
        self.cb_smart_home.setChecked(self.cfg.get("smart_home", True))
        form_view.addRow("", self.cb_smart_home)

        self.cb_wrap = QCheckBox("Переносить длинные строки")
        self.cb_wrap.setChecked(self.cfg.get("wrap_lines", False))
        form_view.addRow("", self.cb_wrap)

        self.sp_minimap = QSpinBox()
        self.sp_minimap.setRange(40, 200)
        self.sp_minimap.setValue(int(self.cfg.get("minimap_width", 90) or 90))
        self.sp_minimap.setSuffix(" px")
        form_view.addRow("Ширина minimap:", self.sp_minimap)

        root.addWidget(gb_view)

        # ============ КНОПКИ ============
        buttons = QDialogButtonBox()
        btn_apply = buttons.addButton("Применить", QDialogButtonBox.ButtonRole.ApplyRole)
        btn_ok = buttons.addButton("OK", QDialogButtonBox.ButtonRole.AcceptRole)
        btn_cancel = buttons.addButton("Отмена", QDialogButtonBox.ButtonRole.RejectRole)
        btn_reset = buttons.addButton("Сбросить", QDialogButtonBox.ButtonRole.ResetRole)

        btn_apply.clicked.connect(self._on_apply)
        btn_ok.clicked.connect(self._on_ok)
        btn_cancel.clicked.connect(self.reject)
        btn_reset.clicked.connect(self._on_reset)

        root.addWidget(buttons)

    def _collect(self):
        """Собирает новые значения из виджетов в self.cfg."""
        self.cfg["font_ui"] = {
            "family": self.cb_ui_family.currentText().strip() or "Ubuntu",
            "size": self.sp_ui_size.value(),
        }
        self.cfg["font_editor"] = {
            "family": self.cb_ed_family.currentText().strip() or "Monospace",
            "size": self.sp_ed_size.value(),
        }
        self.cfg["tab_width"] = self.sp_tab.value()
        self.cfg["use_spaces"] = self.cb_spaces.isChecked()
        self.cfg["show_edge"] = self.cb_edge.isChecked()
        self.cfg["edge_column"] = self.sp_edge.value()
        self.cfg["show_whitespace"] = self.cb_ws.isChecked()
        self.cfg["smart_home"] = self.cb_smart_home.isChecked()
        self.cfg["wrap_lines"] = self.cb_wrap.isChecked()
        if hasattr(self, "sp_minimap"):
            self.cfg["minimap_width"] = self.sp_minimap.value()
        return self.cfg

    def _on_apply(self):
        self._collect()
        self.settings_applied.emit(self.cfg)

    def _on_ok(self):
        self._on_apply()
        self.accept()

    def _on_reset(self):
        # Возвращаем значения по умолчанию в виджетах
        import config as cfgmod
        d = cfgmod.DEFAULTS
        self.cb_ui_family.setCurrentText(d["font_ui"]["family"])
        self.sp_ui_size.setValue(d["font_ui"]["size"])
        self.cb_ed_family.setCurrentText(d["font_editor"]["family"])
        self.sp_ed_size.setValue(d["font_editor"]["size"])
        self.sp_tab.setValue(d["tab_width"])
        self.cb_spaces.setChecked(d["use_spaces"])
        self.cb_edge.setChecked(d["show_edge"])
        self.sp_edge.setValue(d["edge_column"])
        self.cb_ws.setChecked(d["show_whitespace"])
        self.cb_smart_home.setChecked(d["smart_home"])
        self.cb_wrap.setChecked(d["wrap_lines"])
        if hasattr(self, "sp_minimap"):
            self.sp_minimap.setValue(d.get("minimap_width", 90))
