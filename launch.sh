#!/bin/bash
# Запуск MyEdit из системного меню
cd "$(dirname "$0")"

# Настройки окружения для корректной работы Qt
export QT_QPA_PLATFORM=xcb
export QT_QPA_PLATFORMTHEME=""
export QT_QPA_PLATFORMTHEME_DISABLE_PORTAL="1"

# Запуск без вывода ошибок в консоль
exec python3 main.py 2>/dev/null
