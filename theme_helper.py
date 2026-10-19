"""
Генератор QSS для вспомогательных панелей на основе текущей темы.
Каждая панель при смене темы получает свой QSS из этого модуля.
"""


def _is_light(th):
    """Определяет, светлая ли тема — по яркости editor_bg."""
    try:
        bg = th["editor_bg"].lstrip("#")
        r = int(bg[0:2], 16)
        g = int(bg[2:4], 16)
        b = int(bg[4:6], 16)
        return (r + g + b) / 3 > 128
    except Exception:
        return False


def qss_outputpanel(th):
    """QSS для панели вывода."""
    bg      = th["editor_bg"]
    bg2     = th["margin_bg"]
    fg      = th["editor_fg"]
    accent  = th["selected_bg"]
    border  = th["edge_color"]
    light   = _is_light(th)
    btn_bg  = "#e8e8e8" if light else "#3c3c3c"
    btn_fg  = "#333333" if light else "#dddddd"
    code_bg = "#f8f8f8" if light else "#141414"

    return f"""
QWidget {{ background: {bg}; color: {fg}; }}
QTextEdit {{
    background: {code_bg}; color: {fg};
    border: 1px solid {border};
    font-family: 'Monospace';
    font-size: 12px;
}}
QPushButton {{
    background: {btn_bg}; color: {btn_fg};
    border: 1px solid {border}; padding: 4px 12px;
    border-radius: 3px;
}}
QPushButton:hover {{ background: {accent}; color: #ffffff; }}
QLabel {{ color: {fg}; }}
QComboBox {{
    background: {btn_bg}; color: {btn_fg};
    border: 1px solid {border}; padding: 3px;
}}
"""


def qss_findbar(th):
    """QSS для панели поиска/замены."""
    bg     = th["margin_bg"]
    fg     = th["editor_fg"]
    accent = th["selected_bg"]
    border = th["edge_color"]
    light  = _is_light(th)
    input_bg = "#ffffff" if light else "#3c3c3c"
    btn_bg   = "#e8e8e8" if light else "#3c3c3c"
    btn_fg   = "#333333" if light else "#dddddd"

    return f"""
QWidget {{ background: {bg}; color: {fg}; }}
QLineEdit {{
    background: {input_bg}; color: {fg};
    border: 1px solid {border}; padding: 4px;
    border-radius: 3px;
}}
QToolButton {{
    background: {btn_bg}; color: {btn_fg};
    border: 1px solid {border}; padding: 3px 8px;
    border-radius: 3px;
}}
QToolButton:hover {{ background: {accent}; color: #ffffff; }}
QCheckBox {{ color: {fg}; }}
"""


def qss_searchproject(th):
    """QSS для панели поиска по проекту."""
    bg     = th["margin_bg"]
    fg     = th["editor_fg"]
    accent = th["selected_bg"]
    border = th["edge_color"]
    light  = _is_light(th)
    input_bg = "#ffffff" if light else "#3c3c3c"
    btn_bg   = "#e8e8e8" if light else "#3c3c3c"
    btn_fg   = "#333333" if light else "#dddddd"

    return f"""
QWidget {{ background: {bg}; color: {fg}; }}
QLineEdit {{
    background: {input_bg}; color: {fg};
    border: 1px solid {border}; padding: 4px;
    border-radius: 3px;
}}
QPushButton {{
    background: {btn_bg}; color: {btn_fg};
    border: 1px solid {border}; padding: 4px 10px;
    border-radius: 3px;
}}
QPushButton:hover {{ background: {accent}; color: #ffffff; }}
QTreeWidget {{
    background: {bg}; color: {fg};
    border: none; outline: none;
    font-family: 'Monospace';
}}
QTreeWidget::item:selected {{ background: {accent}; color: #ffffff; }}
QCheckBox {{ color: {fg}; }}
QLabel {{ color: {fg}; }}
"""


def qss_dialog(th):
    """QSS для всплывающих диалогов (palette, quickopen)."""
    bg     = th["margin_bg"]
    fg     = th["editor_fg"]
    accent = th["selected_bg"]
    border = th["edge_color"]
    light  = _is_light(th)
    input_bg = "#ffffff" if light else "#3c3c3c"
    hover    = "#f0f0f0" if light else "#2a2d2e"

    return f"""
QDialog {{
    background: {bg}; color: {fg};
    border: 1px solid {border};
}}
QLineEdit {{
    background: {input_bg}; color: {fg};
    border: 1px solid {border};
    padding: 8px 10px;
    border-radius: 4px;
}}
QListWidget {{
    background: {bg}; color: {fg};
    border: none; outline: none;
}}
QListWidget::item {{ padding: 5px 10px; }}
QListWidget::item:selected {{ background: {accent}; color: #ffffff; }}
QListWidget::item:hover {{ background: {hover}; }}
"""


def qss_helpdialog(th):
    """QSS для окна справки."""
    bg     = th["editor_bg"]
    fg     = th["editor_fg"]
    accent = th["selected_bg"]
    border = th["edge_color"]
    light  = _is_light(th)
    key_bg = "rgba(0,120,212,0.15)" if light else "rgba(86,156,214,0.15)"
    key_border = "rgba(0,120,212,0.4)" if light else "rgba(86,156,214,0.4)"
    btn_bg = "#e8e8e8" if light else "#3c3c3c"
    btn_fg = "#333333" if light else "#dddddd"
    header_color = "#0078d4" if light else "#569cd6"

    return f"""
QDialog {{ background: {bg}; color: {fg}; }}
QLabel {{ color: {fg}; }}
QScrollArea {{ background: {bg}; border: none; }}
QWidget {{ background: {bg}; }}
QPushButton {{
    background: {btn_bg}; color: {btn_fg};
    border: 1px solid {border}; padding: 5px 14px;
    border-radius: 3px;
}}
QPushButton:hover {{ background: {accent}; color: #ffffff; }}
"""


# Для доступа к цвету групповых заголовков в help
def help_header_color(th):
    return "#0078d4" if _is_light(th) else "#569cd6"


def help_key_style(th):
    """Стиль для «клавиш» в справке."""
    light = _is_light(th)
    if light:
        return ("background: rgba(0,120,212,0.12);"
                "border: 1px solid rgba(0,120,212,0.4);"
                "border-radius: 4px; padding: 3px 8px;")
    return ("background: rgba(86,156,214,0.15);"
            "border: 1px solid rgba(86,156,214,0.4);"
            "border-radius: 4px; padding: 3px 8px;")
