"""
Панель вывода снизу — показывает stdout/stderr запущенного процесса.
"""

import os
import signal
from PyQt6.QtCore import Qt, QProcess
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLabel,
    QPushButton, QComboBox,
)


class OutputPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._process = None

        self._build_ui()
        self.hide()

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # Верхняя строка с заголовком и кнопками
        header = QWidget()
        header.setStyleSheet("background: #2d2d2d;")
        hl = QHBoxLayout(header)
        hl.setContentsMargins(8, 4, 8, 4)
        hl.setSpacing(8)

        self.lbl_title = QLabel("Вывод программы")
        self.lbl_title.setStyleSheet("color: #ddd; font-weight: bold;")
        hl.addWidget(self.lbl_title)

        hl.addStretch(1)

        self.lbl_status = QLabel("")
        self.lbl_status.setStyleSheet("color: #888; font-style: italic;")
        hl.addWidget(self.lbl_status)

        self.btn_stop = QPushButton("⏹ Остановить")
        self.btn_stop.clicked.connect(self.stop)
        self.btn_stop.setEnabled(False)
        hl.addWidget(self.btn_stop)

        self.btn_clear = QPushButton("🧹 Очистить")
        self.btn_clear.clicked.connect(self.clear)
        hl.addWidget(self.btn_clear)

        self.btn_close = QPushButton("✕ Закрыть")
        self.btn_close.clicked.connect(self.hide)
        hl.addWidget(self.btn_close)

        root.addWidget(header)

        # Текстовое поле для вывода
        self.text = QTextEdit()
        self.text.setReadOnly(True)
        self.text.setFont(QFont("Monospace", 11))
        root.addWidget(self.text, 1)

    def apply_theme(self, th):
        """Применяет стиль под текущую тему."""
        from theme_helper import qss_outputpanel
        self.setStyleSheet(qss_outputpanel(th))

    # ---------- Запуск процесса ----------

    def run(self, script_path, working_dir=None):
        """Запускает `python3 script_path` и показывает вывод."""
        if self._process is not None:
            self.stop()

        self.show()
        self.text.clear()
        self.text.append(f'<span style="color:#7ec87e;">$ python3 {script_path}</span>\n')

        wd = working_dir or os.path.dirname(script_path)

        self._process = QProcess(self)
        self._process.setWorkingDirectory(wd)
        self._process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        self._process.readyReadStandardOutput.connect(self._on_output)
        self._process.finished.connect(self._on_finished)
        self._process.errorOccurred.connect(self._on_error)

        self.btn_stop.setEnabled(True)
        self.lbl_status.setText("⏳ выполняется…")

        self._process.start("python3", [script_path])

    def stop(self):
        if self._process is not None and self._process.state() != QProcess.ProcessState.NotRunning:
            # SIGINT чтобы python успел корректно завершиться
            try:
                self._process.terminate()
                if not self._process.waitForFinished(1500):
                    self._process.kill()
            except Exception:
                pass
        self.lbl_status.setText("⏹ остановлено")

    def clear(self):
        self.text.clear()

    # ---------- Слоты ----------

    def _on_output(self):
        if self._process is None:
            return
        data = bytes(self._process.readAllStandardOutput()).decode(
            "utf-8", errors="replace"
        )
        # Экранируем HTML-спецсимволы, сохраняем переносы
        safe = (data.replace("&", "&amp;")
                    .replace("<", "&lt;")
                    .replace(">", "&gt;"))
        self.text.moveCursor(self.text.textCursor().MoveOperation.End)
        self.text.insertHtml(
            f'<span style="color:#d4d4d4; white-space:pre-wrap;">{safe}</span>'
        )
        self.text.moveCursor(self.text.textCursor().MoveOperation.End)

    def _on_finished(self, exit_code, exit_status):
        self.btn_stop.setEnabled(False)
        if exit_code == 0:
            self.lbl_status.setText("✅ завершено успешно")
            color = "#7ec87e"
        else:
            self.lbl_status.setText(f"❌ завершено с кодом {exit_code}")
            color = "#ff6666"
        self.text.append(
            f'\n<span style="color:{color};">— Процесс завершён '
            f'(код {exit_code}) —</span>\n'
        )
        self._process = None

    def _on_error(self, error):
        self.lbl_status.setText(f"❌ ошибка запуска: {error}")
        self.btn_stop.setEnabled(False)
        self._process = None
