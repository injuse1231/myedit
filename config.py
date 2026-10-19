"""
Работа с конфигом приложения.
Файл: ~/.config/myedit/config.json
"""

import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/myedit")
CONFIG_PATH = os.path.join(CONFIG_DIR, "config.json")

DEFAULTS = {
    "theme": "dark_soft",
    "window": {"x": 100, "y": 80, "w": 1200, "h": 750, "maximized": False},
    "open_files": [],
    "current_file": None,
    "font_ui": {"family": "Ubuntu", "size": 10},
    "font_editor": {"family": "JetBrains Mono", "size": 11},
    "tab_width": 4,
    "use_spaces": True,
    "show_edge": True,
    "edge_column": 100,
    "minimap_width": 90,
    "show_whitespace": False,
    "smart_home": True,
    "wrap_lines": False,
    "last_folder": None,
}


def _merge(base, override):
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = _merge(result[k], v)
        else:
            result[k] = v
    return result


def load():
    if not os.path.exists(CONFIG_PATH):
        return dict(DEFAULTS)
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return _merge(DEFAULTS, data)
    except Exception as e:
        print(f"[config] Не удалось прочитать {CONFIG_PATH}: {e}")
        return dict(DEFAULTS)


def save(cfg):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"[config] Не удалось сохранить {CONFIG_PATH}: {e}")
