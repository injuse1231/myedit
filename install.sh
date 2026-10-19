#!/bin/bash
# Установщик MyEdit — ярлык в меню приложений

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Установка MyEdit..."

# Иконка
mkdir -p ~/.local/share/icons/hicolor/scalable/apps
if [ -f "$SCRIPT_DIR/icon.svg" ]; then
    cp "$SCRIPT_DIR/icon.svg" ~/.local/share/icons/hicolor/scalable/apps/myedit.svg
    echo "✅ Иконка установлена"
else
    echo "⚠ icon.svg не найден — иконка не будет установлена"
fi

# .desktop файл
mkdir -p ~/.local/share/applications
cat > ~/.local/share/applications/myedit.desktop << DESKEOF
[Desktop Entry]
Version=1.0
Type=Application
Name=MyEdit
GenericName=Текстовый редактор
Comment=Лёгкий редактор кода в стиле VS Code
Exec=python3 $SCRIPT_DIR/main.py
Icon=myedit
Terminal=false
Categories=Development;TextEditor;IDE;
Keywords=editor;code;text;python;ide;myedit;
StartupNotify=true
StartupWMClass=MyEdit
DESKEOF

chmod +x ~/.local/share/applications/myedit.desktop

# Обновляем базы
update-desktop-database ~/.local/share/applications 2>/dev/null || true
gtk-update-icon-cache -f -t ~/.local/share/icons/hicolor 2>/dev/null || true

echo "✅ Готово! Найди MyEdit в меню приложений."
