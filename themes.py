"""
Темы оформления MyEdit в стиле VS Code.
"""

# ============ 1. VS CODE DARK+ (стандартная тёмная VS Code) ============
DARK_CONTRAST = {
    "name": "VS Code Dark+",
    "editor_bg":    "#1e1e1e",
    "editor_fg":    "#d4d4d4",
    "caret_line":   "#2a2d2e",
    "margin_bg":    "#1e1e1e",
    "margin_fg":    "#858585",
    "selected_bg":  "#264f78",
    "selected_fg":  "#ffffff",
    "edge_color":   "#4a4a50",
    "qss": """
* { outline: none; }
QMainWindow, QWidget {
    background: #1e1e1e;
    color: #d4d4d4;
    font-family: "Ubuntu";
    font-size: 10pt;
}

/* === Вкладки === */
QTabWidget::pane { border: 0; background: #1e1e1e; }
QTabBar {
    background: #252526;
    qproperty-drawBase: 0;
}
QTabBar::tab {
    background: #2d2d2d;
    color: #969696;
    padding: 6px 16px;
    border: none;
    border-right: 1px solid #1e1e1e;
    margin: 0;
    min-width: 80px;
}
QTabBar::tab:hover { background: #2d2d2d; color: #ccc; }
QTabBar::tab:selected {
    background: #1e1e1e;
    color: #ffffff;
    border-bottom: 2px solid #0078d4;
}

/* === Дерево (sidebar) === */
QTreeView {
    background: #252526;
    color: #cccccc;
    border: none;
    outline: none;
    padding: 2px 0;
    font-size: 10pt;
}
QTreeView::item {
    padding: 3px 4px;
    border: none;
}
QTreeView::item:hover { background: #2a2d2e; }
QTreeView::item:selected {
    background: #04395e;
    color: #ffffff;
}

/* === Меню === */
QMenuBar {
    background: #3c3c3c;
    color: #cccccc;
    padding: 1px 0;
    font-size: 10pt;
}
QMenuBar::item {
    padding: 4px 8px;
    background: transparent;
}
QMenuBar::item:selected { background: #505050; }
QMenuBar::item:pressed { background: #0078d4; }

QMenu {
    background: #252526;
    border: 1px solid #454545;
    color: #cccccc;
    padding: 4px 0;
}
QMenu::item {
    padding: 5px 30px 5px 24px;
    border: none;
}
QMenu::item:selected { background: #04395e; }
QMenu::separator {
    height: 1px;
    background: #454545;
    margin: 4px 8px;
}

/* === Статус-бар (синий как в VS Code) === */
QStatusBar {
    background: #181818;
    color: #cccccc;
    padding: 2px 8px;
    font-size: 9pt;
}
QStatusBar QLabel { color: #cccccc; padding: 0 6px; }
QStatusBar::item { border: none; }

/* === Поля ввода === */
QLineEdit {
    background: #3c3c3c;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    padding: 4px 8px;
    selection-background-color: #264f78;
    selection-color: #ffffff;
}
QLineEdit:focus { border: 1px solid #007fd4; }

/* === Сплиттеры === */
QSplitter::handle { background: #3e3e42; }
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }
QSplitter::handle:hover { background: #007fd4; }

/* === Тулбар === */
QToolBar {
    background: #323233;
    border: none;
    spacing: 0;
    padding: 3px 4px;
    min-height: 32px;
}
QToolBar::separator {
    background: #454545;
    width: 1px;
    margin: 6px 4px;
}
QToolButton {
    color: #cccccc;
    padding: 4px 10px;
    border: none;
    border-radius: 2px;
    min-height: 22px;
    font-size: 10pt;
}
QToolButton:hover { background: #505050; }
QToolButton:pressed { background: #0078d4; }
QToolButton:checked { background: #0078d4; }

/* === Чекбоксы === */
QCheckBox { color: #cccccc; spacing: 6px; font-size: 10pt; }
QCheckBox::indicator {
    width: 14px; height: 14px;
    border: 1px solid #6b6b6b;
    background: #3c3c3c;
    border-radius: 2px;
}
QCheckBox::indicator:hover { border: 1px solid #007fd4; }
QCheckBox::indicator:checked {
    background: #0078d4;
    border: 1px solid #0078d4;
    image: none;
}

QLabel { color: #cccccc; font-size: 10pt; }

/* === Кнопки === */
QPushButton {
    background: #0e639c;
    color: #ffffff;
    border: none;
    padding: 5px 14px;
    border-radius: 2px;
    min-height: 20px;
    font-size: 10pt;
}
QPushButton:hover { background: #1177bb; }
QPushButton:pressed { background: #0d5a91; }
QPushButton:disabled { background: #3c3c3c; color: #6b6b6b; }

/* === Диалоги === */
QDialog { background: #252526; color: #cccccc; }

QListWidget {
    background: #1e1e1e;
    color: #cccccc;
    border: 1px solid #3e3e42;
    outline: none;
    padding: 2px;
}
QListWidget::item { padding: 4px 8px; }
QListWidget::item:hover { background: #2a2d2e; }
QListWidget::item:selected { background: #04395e; color: #ffffff; }

QComboBox {
    background: #3c3c3c;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    padding: 4px 8px;
    min-height: 18px;
}
QComboBox:hover { border: 1px solid #007fd4; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: #252526;
    color: #cccccc;
    border: 1px solid #454545;
    selection-background-color: #04395e;
    selection-color: #ffffff;
}

QSpinBox {
    background: #3c3c3c;
    color: #cccccc;
    border: 1px solid #3c3c3c;
    padding: 3px 6px;
}
QSpinBox:focus { border: 1px solid #007fd4; }

/* === Группы в настройках === */
QGroupBox {
    border: 1px solid #3e3e42;
    margin-top: 10px;
    padding: 10px 8px 8px 8px;
    color: #cccccc;
    font-weight: normal;
    font-size: 10pt;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 6px;
    left: 10px;
    color: #569cd6;
    background: #1e1e1e;
}

/* === Скроллбары (как в VS Code — тонкие) === */
QScrollBar:vertical {
    background: transparent;
    width: 14px;
    margin: 0;
}
QScrollBar::handle:vertical {
    background: #424242;
    min-height: 30px;
    border: 3px solid transparent;
    border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:vertical:hover { background: #4f4f4f; background-clip: content-box; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; background: transparent; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal {
    background: transparent;
    height: 14px;
    margin: 0;
}
QScrollBar::handle:horizontal {
    background: #424242;
    min-width: 30px;
    border: 3px solid transparent;
    border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:horizontal:hover { background: #4f4f4f; background-clip: content-box; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; background: transparent; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
""",
    "lexer_colors": {
        "default":   "#d4d4d4",
        "comment":   "#6a9955",
        "keyword":   "#569cd6",
        "string":    "#ce9178",
        "number":    "#b5cea8",
        "class_":    "#4ec9b0",
        "function":  "#dcdcaa",
        "decorator": "#dcdcaa",
        "operator":  "#d4d4d4",
    },
}

# ============ 2. VS CODE DARK MODERN (чуть мягче) ============
DARK_SOFT = {
    "name": "VS Code Dark Modern",
    "editor_bg":    "#1f1f1f",
    "editor_fg":    "#cccccc",
    "caret_line":   "#282828",
    "margin_bg":    "#1f1f1f",
    "margin_fg":    "#858585",
    "selected_bg":  "#264f78",
    "selected_fg":  "#ffffff",
    "edge_color":   "#3e3e42",
    "qss": """
* { outline: none; }
QMainWindow, QWidget {
    background: #1f1f1f;
    color: #cccccc;
    font-family: "Ubuntu";
    font-size: 10pt;
}

QTabWidget::pane { border: 0; background: #1f1f1f; }
QTabBar { background: #181818; qproperty-drawBase: 0; }
QTabBar::tab {
    background: #181818;
    color: #9d9d9d;
    padding: 6px 16px;
    border: none;
    border-right: 1px solid #1f1f1f;
    min-width: 80px;
}
QTabBar::tab:hover { color: #cccccc; background: #1f1f1f; }
QTabBar::tab:selected {
    background: #1f1f1f;
    color: #ffffff;
    border-bottom: 2px solid #0078d4;
}

QTreeView {
    background: #181818;
    color: #cccccc;
    border: none;
    outline: none;
    padding: 2px 0;
    font-size: 10pt;
}
QTreeView::item { padding: 3px 4px; }
QTreeView::item:hover { background: #2a2d2e; }
QTreeView::item:selected { background: #04395e; color: #fff; }

QMenuBar { background: #181818; color: #cccccc; padding: 1px 0; font-size: 10pt; }
QMenuBar::item { padding: 4px 8px; background: transparent; }
QMenuBar::item:selected { background: #2a2d2e; }

QMenu { background: #1f1f1f; border: 1px solid #2b2b2b; color: #cccccc; padding: 4px 0; }
QMenu::item { padding: 5px 30px 5px 24px; }
QMenu::item:selected { background: #04395e; }
QMenu::separator { height: 1px; background: #2b2b2b; margin: 4px 8px; }

QStatusBar { background: #181818; color: #cccccc; padding: 2px 8px; font-size: 9pt; }
QStatusBar::item { border: none; }

QLineEdit {
    background: #313131; color: #cccccc;
    border: 1px solid #313131; padding: 4px 8px;
    selection-background-color: #264f78;
}
QLineEdit:focus { border: 1px solid #007fd4; }

QSplitter::handle { background: #2b2b2b; }
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }
QSplitter::handle:hover { background: #007fd4; }

QToolBar { background: #181818; border: none; spacing: 0; padding: 3px 4px; min-height: 32px; }
QToolBar::separator { background: #2b2b2b; width: 1px; margin: 6px 4px; }
QToolButton {
    color: #cccccc; padding: 4px 10px;
    border: none; border-radius: 2px; min-height: 22px; font-size: 10pt;
}
QToolButton:hover { background: #2a2d2e; }
QToolButton:pressed, QToolButton:checked { background: #0078d4; }

QCheckBox { color: #cccccc; spacing: 6px; font-size: 10pt; }
QCheckBox::indicator {
    width: 14px; height: 14px;
    border: 1px solid #6b6b6b; background: #313131;
    border-radius: 2px;
}
QCheckBox::indicator:checked { background: #0078d4; border: 1px solid #0078d4; image: none; }

QLabel { color: #cccccc; font-size: 10pt; }

QPushButton {
    background: #0078d4; color: #ffffff; border: none;
    padding: 5px 14px; border-radius: 2px; min-height: 20px; font-size: 10pt;
}
QPushButton:hover { background: #026ec1; }
QPushButton:pressed { background: #005a9e; }
QPushButton:disabled { background: #2b2b2b; color: #6b6b6b; }

QDialog { background: #1f1f1f; color: #cccccc; }
QListWidget { background: #181818; color: #cccccc; border: 1px solid #2b2b2b; padding: 2px; }
QListWidget::item { padding: 4px 8px; }
QListWidget::item:hover { background: #2a2d2e; }
QListWidget::item:selected { background: #04395e; color: #fff; }

QComboBox {
    background: #313131; color: #cccccc; border: 1px solid #313131;
    padding: 4px 8px; min-height: 18px;
}
QComboBox:hover { border: 1px solid #007fd4; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: #1f1f1f; color: #cccccc; border: 1px solid #2b2b2b;
    selection-background-color: #04395e;
}

QSpinBox { background: #313131; color: #cccccc; border: 1px solid #313131; padding: 3px 6px; }
QSpinBox:focus { border: 1px solid #007fd4; }

QGroupBox {
    border: 1px solid #2b2b2b; margin-top: 10px;
    padding: 10px 8px 8px 8px; color: #cccccc; font-size: 10pt;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    padding: 0 6px; left: 10px; color: #4fc3f7; background: #1f1f1f;
}

QScrollBar:vertical { background: transparent; width: 14px; margin: 0; }
QScrollBar::handle:vertical {
    background: #424242; min-height: 30px;
    border: 3px solid transparent; border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:vertical:hover { background: #4f4f4f; background-clip: content-box; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal { background: transparent; height: 14px; margin: 0; }
QScrollBar::handle:horizontal {
    background: #424242; min-width: 30px;
    border: 3px solid transparent; border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:horizontal:hover { background: #4f4f4f; background-clip: content-box; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
""",
    "lexer_colors": {
        "default":   "#cccccc",
        "comment":   "#6a9955",
        "keyword":   "#569cd6",
        "string":    "#ce9178",
        "number":    "#b5cea8",
        "class_":    "#4ec9b0",
        "function":  "#dcdcaa",
        "decorator": "#dcdcaa",
        "operator":  "#cccccc",
    },
}

# ============ 3. VS CODE LIGHT+ ============
LIGHT_CONTRAST = {
    "name": "VS Code Light+",
    "editor_bg":    "#ffffff",
    "editor_fg":    "#000000",
    "caret_line":   "#f0f0f0",
    "margin_bg":    "#ffffff",
    "margin_fg":    "#237893",
    "selected_bg":  "#add6ff",
    "selected_fg":  "#000000",
    "edge_color":   "#c8c8c8",
    "qss": """
* { outline: none; }
QMainWindow, QWidget {
    background: #ffffff; color: #333333;
    font-family: "Ubuntu"; font-size: 10pt;
}

QTabWidget::pane { border: 0; background: #ffffff; }
QTabBar { background: #f3f3f3; qproperty-drawBase: 0; }
QTabBar::tab {
    background: #ececec; color: #6f6f6f;
    padding: 6px 16px; border: none;
    border-right: 1px solid #ffffff;
    min-width: 80px;
}
QTabBar::tab:hover { color: #333333; background: #e0e0e0; }
QTabBar::tab:selected {
    background: #ffffff;
    color: #333333;
    border-bottom: 2px solid #0078d4;
}

QTreeView {
    background: #f3f3f3; color: #333333;
    border: none; outline: none; padding: 2px 0; font-size: 10pt;
}
QTreeView::item { padding: 3px 4px; }
QTreeView::item:hover { background: #e8e8e8; }
QTreeView::item:selected { background: #cce4f7; color: #000; }

QMenuBar { background: #f3f3f3; color: #333333; padding: 1px 0; font-size: 10pt; }
QMenuBar::item { padding: 4px 8px; background: transparent; }
QMenuBar::item:selected { background: #e8e8e8; }

QMenu { background: #ffffff; border: 1px solid #d4d4d4; color: #333333; padding: 4px 0; }
QMenu::item { padding: 5px 30px 5px 24px; }
QMenu::item:selected { background: #cce4f7; }
QMenu::separator { height: 1px; background: #e5e5e5; margin: 4px 8px; }

QStatusBar { background: #f3f3f3; color: #333333; padding: 2px 8px; font-size: 9pt; }
QStatusBar QLabel { color: #333333; padding: 0 6px; }
QStatusBar::item { border: none; }

QLineEdit {
    background: #ffffff; color: #333333;
    border: 1px solid #cecece; padding: 4px 8px;
    selection-background-color: #add6ff;
}
QLineEdit:focus { border: 1px solid #007fd4; }

QSplitter::handle { background: #e5e5e5; }
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }
QSplitter::handle:hover { background: #007fd4; }

QToolBar { background: #f3f3f3; border: none; spacing: 0; padding: 3px 4px; min-height: 32px; }
QToolBar::separator { background: #e5e5e5; width: 1px; margin: 6px 4px; }
QToolButton {
    color: #333333; padding: 4px 10px;
    border: none; border-radius: 2px; min-height: 22px; font-size: 10pt;
}
QToolButton:hover { background: #e8e8e8; }
QToolButton:pressed, QToolButton:checked { background: #0078d4; color: #fff; }

QCheckBox { color: #333333; spacing: 6px; font-size: 10pt; }
QCheckBox::indicator {
    width: 14px; height: 14px;
    border: 1px solid #cecece; background: #ffffff; border-radius: 2px;
}
QCheckBox::indicator:checked { background: #0078d4; border: 1px solid #0078d4; image: none; }

QLabel { color: #333333; font-size: 10pt; }

QPushButton {
    background: #0078d4; color: #ffffff; border: none;
    padding: 5px 14px; border-radius: 2px; min-height: 20px; font-size: 10pt;
}
QPushButton:hover { background: #026ec1; }
QPushButton:pressed { background: #005a9e; }
QPushButton:disabled { background: #e5e5e5; color: #a0a0a0; }

QDialog { background: #ffffff; color: #333333; }
QListWidget { background: #ffffff; color: #333333; border: 1px solid #cecece; padding: 2px; }
QListWidget::item { padding: 4px 8px; }
QListWidget::item:hover { background: #f3f3f3; }
QListWidget::item:selected { background: #cce4f7; color: #000; }

QComboBox {
    background: #ffffff; color: #333333; border: 1px solid #cecece;
    padding: 4px 8px; min-height: 18px;
}
QComboBox:hover { border: 1px solid #007fd4; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: #ffffff; color: #333333; border: 1px solid #cecece;
    selection-background-color: #cce4f7;
}

QSpinBox { background: #ffffff; color: #333333; border: 1px solid #cecece; padding: 3px 6px; }
QSpinBox:focus { border: 1px solid #007fd4; }

QGroupBox {
    border: 1px solid #e5e5e5; margin-top: 10px;
    padding: 10px 8px 8px 8px; color: #333333; font-size: 10pt;
}
QGroupBox::title {
    subcontrol-origin: margin; subcontrol-position: top left;
    padding: 0 6px; left: 10px; color: #0078d4; background: #ffffff;
}

QScrollBar:vertical { background: transparent; width: 14px; margin: 0; }
QScrollBar::handle:vertical {
    background: #c1c1c1; min-height: 30px;
    border: 3px solid transparent; border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:vertical:hover { background: #a8a8a8; background-clip: content-box; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal { background: transparent; height: 14px; margin: 0; }
QScrollBar::handle:horizontal {
    background: #c1c1c1; min-width: 30px;
    border: 3px solid transparent; border-radius: 8px;
    background-clip: content-box;
}
QScrollBar::handle:horizontal:hover { background: #a8a8a8; background-clip: content-box; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
""",
    "lexer_colors": {
        "default":   "#000000",
        "comment":   "#008000",
        "keyword":   "#0000ff",
        "string":    "#a31515",
        "number":    "#098658",
        "class_":    "#267f99",
        "function":  "#795e26",
        "decorator": "#795e26",
        "operator":  "#000000",
    },
}

# ============ 4. VS CODE LIGHT MODERN ============
WHITE_SOFT = {
    "name": "VS Code Light Modern",
    "editor_bg":    "#ffffff",
    "editor_fg":    "#3b3b3b",
    "caret_line":   "#f5f5f5",
    "margin_bg":    "#ffffff",
    "margin_fg":    "#237893",
    "selected_bg":  "#add6ff",
    "selected_fg":  "#000000",
    "edge_color":   "#c8c8c8",
    "qss": """
* { outline: none; }
QMainWindow, QWidget {
    background: #ffffff; color: #3b3b3b;
    font-family: "Ubuntu"; font-size: 10pt;
}

QTabWidget::pane { border: 0; background: #ffffff; }
QTabBar { background: #f8f8f8; qproperty-drawBase: 0; }
QTabBar::tab {
    background: #f8f8f8; color: #8a8a8a;
    padding: 6px 16px; border: none;
    border-right: 1px solid #ffffff;
    min-width: 80px;
}
QTabBar::tab:hover { color: #3b3b3b; background: #ececec; }
QTabBar::tab:selected {
    background: #ffffff;
    color: #3b3b3b;
    border-bottom: 2px solid #0078d4;
}

QTreeView { background: #f8f8f8; color: #3b3b3b; border: none; outline: none; padding: 2px 0; font-size: 10pt; }
QTreeView::item { padding: 3px 4px; }
QTreeView::item:hover { background: #ececec; }
QTreeView::item:selected { background: #e4e6f1; color: #000; }

QMenuBar { background: #f8f8f8; color: #3b3b3b; padding: 1px 0; font-size: 10pt; }
QMenuBar::item { padding: 4px 8px; background: transparent; }
QMenuBar::item:selected { background: #ececec; }

QMenu { background: #ffffff; border: 1px solid #d4d4d4; color: #3b3b3b; padding: 4px 0; }
QMenu::item { padding: 5px 30px 5px 24px; }
QMenu::item:selected { background: #e4e6f1; }
QMenu::separator { height: 1px; background: #e5e5e5; margin: 4px 8px; }

QStatusBar { background: #f8f8f8; color: #3b3b3b; padding: 2px 8px; font-size: 9pt; }
QStatusBar::item { border: none; }

QLineEdit { background: #ffffff; color: #3b3b3b; border: 1px solid #cecece; padding: 4px 8px; selection-background-color: #add6ff; }
QLineEdit:focus { border: 1px solid #007fd4; }

QSplitter::handle { background: #e5e5e5; }
QSplitter::handle:horizontal { width: 1px; }
QSplitter::handle:vertical { height: 1px; }
QSplitter::handle:hover { background: #007fd4; }

QToolBar { background: #f8f8f8; border: none; spacing: 0; padding: 3px 4px; min-height: 32px; }
QToolBar::separator { background: #e5e5e5; width: 1px; margin: 6px 4px; }
QToolButton { color: #3b3b3b; padding: 4px 10px; border: none; border-radius: 2px; min-height: 22px; font-size: 10pt; }
QToolButton:hover { background: #ececec; }
QToolButton:pressed, QToolButton:checked { background: #0078d4; color: #fff; }

QCheckBox { color: #3b3b3b; spacing: 6px; font-size: 10pt; }
QCheckBox::indicator { width: 14px; height: 14px; border: 1px solid #cecece; background: #ffffff; border-radius: 2px; }
QCheckBox::indicator:checked { background: #0078d4; border: 1px solid #0078d4; image: none; }

QLabel { color: #3b3b3b; font-size: 10pt; }

QPushButton { background: #0078d4; color: #ffffff; border: none; padding: 5px 14px; border-radius: 2px; min-height: 20px; font-size: 10pt; }
QPushButton:hover { background: #026ec1; }
QPushButton:pressed { background: #005a9e; }
QPushButton:disabled { background: #e5e5e5; color: #a0a0a0; }

QDialog { background: #ffffff; color: #3b3b3b; }
QListWidget { background: #ffffff; color: #3b3b3b; border: 1px solid #cecece; padding: 2px; }
QListWidget::item { padding: 4px 8px; }
QListWidget::item:hover { background: #f8f8f8; }
QListWidget::item:selected { background: #e4e6f1; color: #000; }

QComboBox { background: #ffffff; color: #3b3b3b; border: 1px solid #cecece; padding: 4px 8px; min-height: 18px; }
QComboBox:hover { border: 1px solid #007fd4; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView { background: #ffffff; color: #3b3b3b; border: 1px solid #cecece; selection-background-color: #e4e6f1; }

QSpinBox { background: #ffffff; color: #3b3b3b; border: 1px solid #cecece; padding: 3px 6px; }
QSpinBox:focus { border: 1px solid #007fd4; }

QGroupBox { border: 1px solid #e5e5e5; margin-top: 10px; padding: 10px 8px 8px 8px; color: #3b3b3b; font-size: 10pt; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 6px; left: 10px; color: #0078d4; background: #ffffff; }

QScrollBar:vertical { background: transparent; width: 14px; margin: 0; }
QScrollBar::handle:vertical { background: #c1c1c1; min-height: 30px; border: 3px solid transparent; border-radius: 8px; background-clip: content-box; }
QScrollBar::handle:vertical:hover { background: #a8a8a8; background-clip: content-box; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: transparent; }

QScrollBar:horizontal { background: transparent; height: 14px; margin: 0; }
QScrollBar::handle:horizontal { background: #c1c1c1; min-width: 30px; border: 3px solid transparent; border-radius: 8px; background-clip: content-box; }
QScrollBar::handle:horizontal:hover { background: #a8a8a8; background-clip: content-box; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: transparent; }
""",
    "lexer_colors": {
        "default":   "#3b3b3b",
        "comment":   "#008000",
        "keyword":   "#0000ff",
        "string":    "#a31515",
        "number":    "#098658",
        "class_":    "#267f99",
        "function":  "#795e26",
        "decorator": "#795e26",
        "operator":  "#3b3b3b",
    },
}

THEMES = {
    "dark_contrast":  DARK_CONTRAST,
    "dark_soft":      DARK_SOFT,
    "light_contrast": LIGHT_CONTRAST,
    "white_soft":     WHITE_SOFT,
}

DEFAULT_THEME = "dark_soft"
