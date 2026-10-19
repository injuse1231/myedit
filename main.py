#!/usr/bin/env python3
import os
import sys

os.environ["QT_QPA_PLATFORM"] = "xcb"
os.environ["QT_QPA_PLATFORMTHEME"] = ""
os.environ["QT_QPA_PLATFORMTHEME_DISABLE_PORTAL"] = "1"

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QKeySequence, QFont, QShortcut
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QSplitter, QFileDialog,
    QToolBar, QStatusBar, QLabel, QWidget, QVBoxLayout, QHBoxLayout,
    QMessageBox,
)

from editor import CodeEditor
from filetree import FileTree
from findbar import FindBar
from palette import CommandPalette
from commands import COMMANDS
from themes import THEMES, DEFAULT_THEME
from helpdialog import HelpDialog
from quickopen import QuickOpenDialog
from settingsdialog import SettingsDialog
from outputpanel import OutputPanel
from minimap import Minimap
from gutter import Gutter
from searchproject import SearchProjectPanel
import config as cfg


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyEdit")

        self.cfg = cfg.load()
        self.current_theme = self.cfg.get("theme", DEFAULT_THEME)
        if self.current_theme not in THEMES:
            self.current_theme = DEFAULT_THEME

        w = self.cfg["window"]
        self.resize(w.get("w", 1200), w.get("h", 750))
        self.move(w.get("x", 100), w.get("y", 80))

        # --- Вкладки ---
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # --- Дерево ---
        self.tree = FileTree()
        self.tree.fileOpened.connect(self.open_path)
        self.tree.fileOperationDone.connect(self._on_file_op)

        # --- Сплиттер ---
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.tree)
        self.splitter.addWidget(self.tabs)
        self.splitter.setSizes([180, 1020])

        # --- Контейнер ---
        container = QWidget()
        vbox = QVBoxLayout(container)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(0)
        vbox.addWidget(self.splitter, 1)

        self.findbar = FindBar()
        vbox.addWidget(self.findbar)

        self.outputpanel = OutputPanel()
        vbox.addWidget(self.outputpanel)

        self.searchproject = SearchProjectPanel()
        vbox.addWidget(self.searchproject)
        self.searchproject.fileRequested.connect(self._jump_to)

        self.setCentralWidget(container)

        self.findbar.findNext.connect(self._find_next)
        self.findbar.replaceOne.connect(self._replace_one)
        self.findbar.replaceAll.connect(self._replace_all)

        # --- UI ---
        self._build_menu()
        self._build_toolbar()
        self._build_statusbar()

        # --- Хоткеи ---
        QShortcut(QKeySequence("F1"), self, activated=self.show_help)
        QShortcut(QKeySequence("Ctrl+Shift+P"), self, activated=self.show_palette)
        QShortcut(QKeySequence("Ctrl+P"), self, activated=self.show_quick_open)
        QShortcut(QKeySequence("Ctrl+,"), self, activated=self.show_settings)
        QShortcut(QKeySequence("F5"), self, activated=self.run_current_file)
        QShortcut(QKeySequence("Ctrl+Shift+F"), self,
                  activated=self.show_search_project)

        # --- Сессия ---
        self._restore_session()
        self.apply_theme(self.current_theme)

        if self.tabs.count() == 0:
            self.new_file()

        # --- Таймер автосохранения ---
        self.auto_save_timer = QTimer(self)
        self.auto_save_timer.setInterval(3000)
        self.auto_save_timer.timeout.connect(self._auto_save)
        self.auto_save_timer.start()

    # ==================== МЕНЮ ====================

    def _build_menu(self):
        mb = self.menuBar()

        file_menu = mb.addMenu("Файл")
        self._act(file_menu, "Новый", QKeySequence.StandardKey.New, self.new_file)
        self._act(file_menu, "Открыть файл…", QKeySequence.StandardKey.Open, self.open_file)
        self._act(file_menu, "Открыть папку…", "Ctrl+K", self.open_folder)
        file_menu.addSeparator()
        self._act(file_menu, "Быстрое открытие файла…", "Ctrl+P", self.show_quick_open)
        file_menu.addSeparator()
        self._act(file_menu, "Сохранить", QKeySequence.StandardKey.Save, self.save)
        self._act(file_menu, "Сохранить как…", QKeySequence.StandardKey.SaveAs, self.save_as)
        file_menu.addSeparator()
        self._act(file_menu, "▶  Запустить", "F5", self.run_current_file)
        file_menu.addSeparator()
        self._act(file_menu, "Выход", "Ctrl+Q", self.close)

        edit_menu = mb.addMenu("Правка")
        self._act(edit_menu, "Отменить", QKeySequence.StandardKey.Undo,
                  lambda: self._cur() and self._cur().undo())
        self._act(edit_menu, "Вернуть", QKeySequence.StandardKey.Redo,
                  lambda: self._cur() and self._cur().redo())
        edit_menu.addSeparator()
        self._act(edit_menu, "Вырезать", QKeySequence.StandardKey.Cut,
                  lambda: self._cur() and self._cur().cut())
        self._act(edit_menu, "Копировать", QKeySequence.StandardKey.Copy,
                  lambda: self._cur() and self._cur().copy())
        self._act(edit_menu, "Вставить", QKeySequence.StandardKey.Paste,
                  lambda: self._cur() and self._cur().paste())
        edit_menu.addSeparator()
        self._act(edit_menu, "Найти…", QKeySequence.StandardKey.Find, self.show_find)
        self._act(edit_menu, "Найти и заменить…", QKeySequence.StandardKey.Replace,
                  self.show_replace)
        edit_menu.addSeparator()
        self._act(edit_menu, "Найти в проекте…", "Ctrl+Shift+F",
                  self.show_search_project)
        edit_menu.addSeparator()
        self._act(edit_menu, "Настройки…", "Ctrl+,", self.show_settings)

        view_menu = mb.addMenu("Вид")
        self._act(view_menu, "Показать дерево", "Ctrl+B", self.toggle_tree,
                  checkable=True, checked=True)
        view_menu.addSeparator()
        self._act(view_menu, "Командная палитра…", "Ctrl+Shift+P", self.show_palette)

        theme_menu = mb.addMenu("Темы")
        for key, th in THEMES.items():
            self._act(theme_menu, th["name"], None,
                      lambda checked=False, k=key: self.apply_theme(k))

        help_menu = mb.addMenu("Справка")
        self._act(help_menu, "Горячие клавиши", "F1", self.show_help)
        self._act(help_menu, "О программе", None, self.show_about)

    def _act(self, menu, text, shortcut, slot, checkable=False, checked=False):
        a = QAction(text, self)
        if shortcut:
            a.setShortcut(shortcut)
        a.setCheckable(checkable)
        a.setChecked(checked)
        a.triggered.connect(slot)
        menu.addAction(a)
        return a

    def _build_toolbar(self):
        tb = QToolBar("Панель")
        tb.setMovable(False)
        tb.setIconSize(tb.iconSize())
        self.addToolBar(tb)

        # Группа «Файл»
        self._act(tb, "Новый", None, self.new_file)
        self._act(tb, "Открыть", None, self.open_file)
        self._act(tb, "Быстро", None, self.show_quick_open)
        self._act(tb, "Сохранить", None, self.save)
        tb.addSeparator()
        # Группа «Запуск»
        self._act(tb, "Запустить", None, self.run_current_file)
        tb.addSeparator()
        # Группа «Поиск»
        self._act(tb, "Найти", None, self.show_find)
        self._act(tb, "В проекте", None, self.show_search_project)
        tb.addSeparator()
        # Группа «Прочее»
        self._act(tb, "Палитра", None, self.show_palette)
        self._act(tb, "Настройки", None, self.show_settings)
        self._act(tb, "Справка", None, self.show_help)

    def _build_statusbar(self):
        sb = QStatusBar()
        self.setStatusBar(sb)
        self.lbl_pos = QLabel("Стр 1, Кол 1")
        self.lbl_info = QLabel("Готово")
        sb.addWidget(self.lbl_info, 1)
        sb.addPermanentWidget(self.lbl_pos)

    # ==================== ТЕМА ====================

    def apply_theme(self, key):
        if key not in THEMES:
            return
        th = THEMES[key]
        self.current_theme = key
        self.cfg["theme"] = key
        # Дополнительный QSS для handle сплиттера — видимая ручка
        extra_qss = """
        QSplitter::handle {
            background: %s;
        }
        QSplitter::handle:hover {
            background: %s;
        }
        """ % (th.get("edge_color", "#3a3a3a"), th.get("selected_bg", "#264f78"))
        self.setStyleSheet(th["qss"] + extra_qss)

        ui_font = self.cfg.get("font_ui", {})
        f = QFont(ui_font.get("family", "Ubuntu"), ui_font.get("size", 10))
        self.setFont(f)
        self.menuBar().setFont(f)
        if hasattr(self, "tabs"):
            self.tabs.setFont(f)
        if hasattr(self, "tree"):
            self.tree.setFont(f)

        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
            if isinstance(ed, CodeEditor):
                ed.apply_theme(th)

        # Применяем тему ко всем панелям
        if hasattr(self, "findbar"):
            self.findbar.apply_theme(th)
        if hasattr(self, "outputpanel"):
            self.outputpanel.apply_theme(th)
        if hasattr(self, "searchproject"):
            self.searchproject.apply_theme(th)

        self.lbl_info.setText(f"Тема: {th['name']}")

    def _apply_all_settings(self):
        """Применяет текущий self.cfg ко всем редакторам."""
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
            if isinstance(ed, CodeEditor):
                ed.apply_settings(self.cfg)

    # ==================== ФАЙЛЫ ====================

    def _cur(self):
        w = self.tabs.currentWidget()
        if isinstance(w, CodeEditor):
            return w
        if hasattr(w, "_editor") and isinstance(w._editor, CodeEditor):
            return w._editor
        return None

    def new_file(self):
        ed = CodeEditor()
        ed.cursorMoved.connect(self._update_pos)
        ed.apply_settings(self.cfg)
        ed.apply_theme(THEMES[self.current_theme])
        idx = self.tabs.addTab(self._wrap_editor(ed), "Без имени")
        self.tabs.setCurrentIndex(idx)


    def _wrap_editor(self, ed):
        """Оборачивает редактор: gutter | редактор | minimap."""

        # 1. Gutter — авто-ширина (см. gutter.py)
        gutter = Gutter(ed)
        ed.attach_gutter(gutter)
        if hasattr(self, "current_theme"):
            gutter.apply_theme(THEMES[self.current_theme])

        # 2. Minimap справа — фиксированная ширина
        mm = Minimap(ed)
        try:
            mw = int(self.cfg.get("minimap_width", 90))
        except Exception:
            mw = 90
        mm.setFixedWidth(mw)
        ed.attach_minimap(mm)
        if hasattr(self, "current_theme"):
            mm.set_theme(THEMES[self.current_theme])

        # 3. QHBoxLayout: gutter | editor | minimap
        #    с отступами между деревом и gutter, gutter и кодом
        wrapper = QWidget()
        hbox = QHBoxLayout(wrapper)
        hbox.setContentsMargins(6, 0, 0, 0)   # ← 6px слева от gutter
        hbox.setSpacing(4)                     # ← 4px между элементами
        hbox.addWidget(gutter)
        hbox.addWidget(ed, 1)
        hbox.addWidget(mm)

        # Ссылки
        wrapper._editor = ed
        wrapper._gutter = gutter
        wrapper._minimap = mm
        return wrapper


    def open_path(self, path):
        path = os.path.abspath(path)
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
            if isinstance(ed, CodeEditor) and ed.path == path:
                self.tabs.setCurrentIndex(i)
                return
        ed = CodeEditor(path)
        ed.cursorMoved.connect(self._update_pos)
        ed.apply_settings(self.cfg)
        ed.apply_theme(THEMES[self.current_theme])
        idx = self.tabs.addTab(self._wrap_editor(ed), ed.name())
        self.tabs.setCurrentIndex(idx)

    def open_file(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Открыть файлы")
        for p in paths:
            self.open_path(p)

    def open_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Открыть папку")
        if path:
            self.tree.set_root(path)
            self.searchproject.set_root(path)
            self.cfg["last_folder"] = path
            cfg.save(self.cfg)
            self.lbl_info.setText(f"Папка: {path}")

    def save(self):
        ed = self._cur()
        if not ed:
            return
        if not ed.path:
            return self.save_as()
        ed.save_file()
        self.lbl_info.setText(f"Сохранено: {ed.path}")

    def save_as(self):
        ed = self._cur()
        if not ed:
            return
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить как")
        if path:
            ed.save_file(path)
            self.tabs.setTabText(self.tabs.currentIndex(), ed.name())
            self.lbl_info.setText(f"Сохранено: {path}")

    def close_tab(self, idx):
        """Закрывает вкладку. Спрашивает про несохранённые изменения."""
        w = self.tabs.widget(idx)
        ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)

        if isinstance(ed, CodeEditor) and ed.isModified():
            box = QMessageBox(self)
            box.setWindowTitle("Сохранить изменения?")
            box.setIcon(QMessageBox.Icon.Warning)
            box.setText(f"Файл «{ed.name()}» изменён.")
            box.setInformativeText("Сохранить перед закрытием?")
            btn_save = box.addButton("Сохранить", QMessageBox.ButtonRole.AcceptRole)
            btn_discard = box.addButton("Не сохранять", QMessageBox.ButtonRole.DestructiveRole)
            btn_cancel = box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
            box.setDefaultButton(btn_save)
            box.exec()
            clicked = box.clickedButton()

            if clicked == btn_cancel:
                return
            if clicked == btn_save:
                if not ed.path:
                    self.tabs.setCurrentIndex(idx)
                    self.save_as()
                    if not ed.path:
                        return
                else:
                    ed.save_file()

        self.tabs.removeTab(idx)
        if self.tabs.count() == 0:
            self.new_file()

    def _on_tab_changed(self, idx):
        ed = self._cur()
        if ed and ed.path:
            self.lbl_info.setText(ed.path)

    def _on_file_op(self, msg):
        self.lbl_info.setText(msg)

    def _update_pos(self, line, col):
        self.lbl_pos.setText(f"Стр {line}, Кол {col}")

    def toggle_tree(self, checked):
        self.tree.setVisible(checked)

    # ==================== ПОИСК ====================

    def show_find(self):
        self.findbar.open_find()

    def show_replace(self):
        self.findbar.open_replace()

    def _find_next(self, text, forward, case, regex):
        ed = self._cur()
        if not ed:
            return
        found = ed.find_with_status(text, forward, case, regex)
        if found:
            self.findbar.set_status(f"Найдено: {text!r}", error=False)
        else:
            self.findbar.set_status(f"Не найдено: {text!r}", error=True)

    def _replace_one(self, find, repl, case, regex, forward):
        ed = self._cur()
        if not ed:
            return
        sel = ed.selectedText()
        if sel and ((regex and sel) or (sel == find)):
            ed.replaceSelectedText(repl)
        ed.findFirst(find, regex, case, False, True, forward)

    def _replace_all(self, find, repl, case, regex, forward):
        ed = self._cur()
        if not ed:
            return
        text = ed.text()
        if regex:
            import re
            flags = 0 if case else re.IGNORECASE
            try:
                new_text, count = re.subn(find, repl, text, flags=flags)
            except re.error:
                return
        else:
            if case:
                count = text.count(find)
                new_text = text.replace(find, repl)
            else:
                import re
                new_text, count = re.subn(re.escape(find), repl, text,
                                          flags=re.IGNORECASE)
        if count:
            ed.setText(new_text)
        self.lbl_info.setText(f"Заменено: {count}")

    # ==================== ПАЛИТРА ====================

    def show_palette(self):
        dlg = CommandPalette(COMMANDS, self)
        dlg.commandTriggered.connect(self._run_command)
        parent_geo = self.geometry()
        x = parent_geo.x() + (parent_geo.width() - dlg.width()) // 2
        y = parent_geo.y() + 80
        dlg.move(x, y)
        dlg.exec()

    def show_quick_open(self):
        root = self.cfg.get("last_folder")
        if not root or not os.path.isdir(root):
            root = QFileDialog.getExistingDirectory(self, "Открыть папку для поиска")
            if not root:
                return
            self.tree.set_root(root)
            self.cfg["last_folder"] = root
            cfg.save(self.cfg)

        dlg = QuickOpenDialog(root, self)
        dlg.fileChosen.connect(self.open_path)
        parent_geo = self.geometry()
        x = parent_geo.x() + (parent_geo.width() - dlg.width()) // 2
        y = parent_geo.y() + 80
        dlg.move(x, y)
        dlg.exec()

    def _run_command(self, cmd_id):
        if cmd_id == "file.new":         return self.new_file()
        if cmd_id == "file.open":        return self.open_file()
        if cmd_id == "file.open_folder": return self.open_folder()
        if cmd_id == "file.quick_open":  return self.show_quick_open()
        if cmd_id == "file.save":        return self.save()
        if cmd_id == "file.save_as":     return self.save_as()
        if cmd_id == "file.close_tab":
            return self.close_tab(self.tabs.currentIndex())
        if cmd_id == "file.quit":        return self.close()

        ed = self._cur()
        if cmd_id == "edit.undo":       return ed and ed.undo()
        if cmd_id == "edit.redo":       return ed and ed.redo()
        if cmd_id == "edit.cut":        return ed and ed.cut()
        if cmd_id == "edit.copy":       return ed and ed.copy()
        if cmd_id == "edit.paste":      return ed and ed.paste()
        if cmd_id == "edit.select_all": return ed and ed.selectAll()

        if cmd_id == "search.find":     return self.show_find()
        if cmd_id == "search.replace":  return self.show_replace()
        if cmd_id == "search.project":  return self.show_search_project()

        if cmd_id == "view.toggle_tree":
            self.tree.setVisible(not self.tree.isVisible())
            return

        if cmd_id == "run.current":     return self.run_current_file()
        if cmd_id == "settings.open":   return self.show_settings()

        if cmd_id.startswith("theme."):
            key = cmd_id.split(".", 1)[1]
            return self.apply_theme(key)

        if cmd_id == "help.shortcuts":  return self.show_help()
        if cmd_id == "help.about":      return self.show_about()

    # ==================== ЗАПУСК PYTHON ====================

    def run_current_file(self):
        ed = self._cur()
        if not ed:
            return
        if not ed.path:
            # Несохранённый файл — предложим сохранить
            answer = QMessageBox.question(
                self, "Сохранить?",
                "Файл не сохранён. Сохранить перед запуском?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return
            self.save()
            if not ed.path:
                return

        if not ed.path.endswith(".py"):
            answer = QMessageBox.question(
                self, "Не Python-файл",
                "Текущий файл не .py. Запустить всё равно?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if answer != QMessageBox.StandardButton.Yes:
                return

        # Если есть несохранённые изменения — сохраним
        if ed.isModified():
            ed.save_file()

        self.outputpanel.run(ed.path, working_dir=os.path.dirname(ed.path))

    # ==================== ПОИСК ПО ПРОЕКТУ ====================

    def show_search_project(self):
        self.searchproject.open_panel()

    def _jump_to(self, path, line):
        self.open_path(path)
        ed = self._cur()
        if ed and ed.path == os.path.abspath(path):
            ed.setCursorPosition(line - 1, 0)
            ed.ensureLineVisible(line - 1)
            ed.setFocus()

    # ==================== НАСТРОЙКИ ====================

    def show_settings(self):
        dlg = SettingsDialog(self.cfg, self)
        dlg.settings_applied.connect(self._on_settings_applied)
        dlg.exec()

    def _on_settings_applied(self, new_cfg):
        self.cfg.update(new_cfg)
        cfg.save(self.cfg)

        # Переприменяем тему (обновляет шрифт UI)
        self.apply_theme(self.current_theme)
        # Применяем настройки ко всем редакторам
        self._apply_all_settings()
        self.lbl_info.setText("Настройки применены")

    # ==================== СПРАВКА ====================

    def show_help(self):
        dlg = HelpDialog(self)
        dlg.exec()

    def show_about(self):
        QMessageBox.about(
            self,
            "О программе MyEdit",
            "<h3>MyEdit</h3>"
            "<p>Текстовый редактор для Ubuntu на Python + PyQt6 + QScintilla.</p>"
        )

    # ==================== СЕССИЯ ====================

    def _restore_session(self):
        last_folder = self.cfg.get("last_folder")
        if last_folder and os.path.isdir(last_folder):
            self.tree.set_root(last_folder)
            self.searchproject.set_root(last_folder)

        for path in self.cfg.get("open_files", []):
            if path and os.path.isfile(path):
                self.open_path(path)

    def _collect_modified(self):
        """Возвращает список (index, editor) для изменённых вкладок."""
        result = []
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
            if isinstance(ed, CodeEditor) and ed.isModified():
                result.append((i, ed))
        return result

    def _save_session(self):
        open_files = []
        current = None
        for i in range(self.tabs.count()):
            w = self.tabs.widget(i)
            ed = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
            if isinstance(ed, CodeEditor) and ed.path:
                open_files.append(ed.path)
                if i == self.tabs.currentIndex():
                    current = ed.path
        self.cfg["open_files"] = open_files
        self.cfg["current_file"] = current

        geo = self.geometry()
        self.cfg["window"] = {
            "x": geo.x(), "y": geo.y(),
            "w": geo.width(), "h": geo.height(),
            "maximized": self.isMaximized(),
        }
        cfg.save(self.cfg)

    def _auto_save(self):
        """Тихо сохраняет размер окна и открытые файлы."""
        try:
            geo = self.geometry()
            self.cfg["window"] = {
                "x": geo.x(), "y": geo.y(),
                "w": geo.width(), "h": geo.height(),
                "maximized": self.isMaximized(),
            }
            cfg.save(self.cfg)
        except Exception as e:
            pass

    def closeEvent(self, event):
        """При закрытии — спрашиваем про несохранённые вкладки."""
        modified = self._collect_modified()

        if not modified:
            self._save_session()
            super().closeEvent(event)
            return

        # Собираем имена файлов
        names = []
        for _, ed in modified:
            names.append(ed.name())
        files_str = "\n".join(f"  • {n}" for n in names[:10])
        if len(names) > 10:
            files_str += f"\n  … и ещё {len(names) - 10}"

        box = QMessageBox(self)
        box.setWindowTitle("Сохранить изменения?")
        box.setIcon(QMessageBox.Icon.Warning)
        box.setText(
            f"В {len(modified)} файлах есть несохранённые изменения."
        )
        box.setInformativeText(files_str)
        btn_save = box.addButton("Сохранить", QMessageBox.ButtonRole.AcceptRole)
        btn_discard = box.addButton("Не сохранять", QMessageBox.ButtonRole.DestructiveRole)
        btn_cancel = box.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)
        box.setDefaultButton(btn_save)

        box.exec()
        clicked = box.clickedButton()

        if clicked == btn_cancel:
            event.ignore()
            return

        if clicked == btn_save:
            # Пытаемся сохранить все модифицированные
            for _, ed in modified:
                if not ed.path:
                    # Нет пути — предложим Save As
                    self.tabs.setCurrentWidget(
                        self.tabs.widget(self.tabs.indexOf(ed.parent()))
                        if hasattr(ed, "parent") else ed
                    )
                    # Проще — активируем вкладку с этим редактором
                    for i in range(self.tabs.count()):
                        w = self.tabs.widget(i)
                        cur = w if isinstance(w, CodeEditor) else getattr(w, "_editor", None)
                        if cur is ed:
                            self.tabs.setCurrentIndex(i)
                            break
                    self.save_as()
                    # Если после Save As всё ещё без пути — отменяем закрытие
                    if not ed.path:
                        event.ignore()
                        return
                else:
                    ed.save_file()

        # Сохраняем сессию и закрываем
        self._save_session()
        super().closeEvent(event)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("MyEdit")
    app.setApplicationDisplayName("MyEdit")
    app.setDesktopFileName("myedit")

    cfg_data = cfg.load()
    ui_font = cfg_data.get("font_ui", {})
    app.setFont(QFont(ui_font.get("family", "Ubuntu"), ui_font.get("size", 10)))

    win = MainWindow()
    win.show()

    if cfg_data["window"].get("maximized"):
        win.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
