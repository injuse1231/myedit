# MyEdit

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![PyQt6](https://img.shields.io/badge/PyQt6-6.0+-green?logo=qt)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey?logo=linux)

> Лёгкий редактор кода для Ubuntu в стиле VS Code. Полностью на Python + PyQt6.

## 📸 Скриншоты

![MyEdit — Dark Modern](https://raw.githubusercontent.com/injuse1231/myedit/main/screenshots/dark-modern.png)
*Тема VS Code Dark Modern*

![MyEdit — Light+](https://raw.githubusercontent.com/injuse1231/myedit/main/screenshots/light.png)
*Тема VS Code Light+*

## ✨ Возможности

- 🎨 **4 темы** в стиле VS Code (Dark+, Dark Modern, Light+, Light Modern)
- 📁 **Дерево файлов** с контекстным меню (создать, переименовать, удалить)
- 🗂 **Вкладки** с перетаскиванием и закрытием
- 🎯 **Подсветка синтаксиса** — Python, JS, HTML, CSS, JSON, C/C++, Bash, SQL
- 🔍 **Поиск и замена** — `Ctrl+F`, `Ctrl+H`, поиск по проекту `Ctrl+Shift+F`
- ⚡ **Быстрое открытие** файла `Ctrl+P` и **командная палитра** `Ctrl+Shift+P`
- 💡 **Автодополнение** — ключевые слова, встроенные функции, PyQt6, слова из файла
- 🗺 **Minimap** — уменьшенная карта файла справа
- ▶️ **Запуск Python** — `F5`, вывод в панели снизу
- 💾 **Сохранение сессии** — тема, файлы, размер окна
- ⚙️ **Настройки** — шрифт, табы, отображение (`Ctrl+,`)
- 🌳 **Сворачивание блоков** кода
- 📏 **Номера строк** с авто-шириной
- 🔤 **Серые индикаторы отступов**
- 🖥 **Свой gutter** с номерами строк и стрелочками

## 🚀 Установка

### Ubuntu / Debian

```bash
# 1. Зависимости
sudo apt install python3-pyqt6 python3-pyqt6.qsci

# 2. Клонируем репозиторий
git clone https://github.com/injuse1231/myedit.git
cd myedit

# 3. Запуск
python3 main.py