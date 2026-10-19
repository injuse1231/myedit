from PyQt6.QtGui import QColor
from PyQt6.Qsci import (
    QsciLexerPython, QsciLexerJavaScript, QsciLexerHTML,
    QsciLexerCSS, QsciLexerJSON, QsciLexerCPP, QsciLexerBash, QsciLexerSQL,
    QsciLexer,
)

LEXERS = {
    ".py":   QsciLexerPython,
    ".js":   QsciLexerJavaScript,
    ".ts":   QsciLexerJavaScript,
    ".html": QsciLexerHTML,
    ".htm":  QsciLexerHTML,
    ".css":  QsciLexerCSS,
    ".json": QsciLexerJSON,
    ".c":    QsciLexerCPP,
    ".cpp":  QsciLexerCPP,
    ".h":    QsciLexerCPP,
    ".hpp":  QsciLexerCPP,
    ".sh":   QsciLexerBash,
    ".bash": QsciLexerBash,
    ".sql":  QsciLexerSQL,
}


def get_lexer(ext, parent=None):
    cls = LEXERS.get(ext.lower())
    return cls(parent) if cls else None


def apply_lexer_colors(lexer, colors, bg):
    """
    Красит конкретный лексер под тему.
    colors — словарь из themes.py['lexer_colors'].
    bg — фон редактора (hex-строка) для setPaper.
    """
    if lexer is None:
        return

    # Для QsciLexerPython используем именованные константы стилей —
    # это надёжнее, чем номера.
    if isinstance(lexer, QsciLexerPython):
        L = QsciLexerPython
        try:
            lexer.setDefaultColor(QColor(colors["default"]))
            lexer.setDefaultPaper(QColor(bg))
            lexer.setColor(QColor(colors["default"]),  L.Default)
            lexer.setColor(QColor(colors["comment"]),  L.Comment)
            lexer.setColor(QColor(colors["comment"]),  L.CommentBlock)
            lexer.setColor(QColor(colors["number"]),   L.Number)
            lexer.setColor(QColor(colors["keyword"]),  L.Keyword)
            lexer.setColor(QColor(colors["string"]),   L.DoubleQuotedString)
            lexer.setColor(QColor(colors["string"]),   L.SingleQuotedString)
            lexer.setColor(QColor(colors["string"]),   L.TripleSingleQuotedString)
            lexer.setColor(QColor(colors["string"]),   L.TripleDoubleQuotedString)
            lexer.setColor(QColor(colors["class_"]),   L.ClassName)
            lexer.setColor(QColor(colors["function"]), L.FunctionMethodName)
            lexer.setColor(QColor(colors["decorator"]),L.Decorator)
            lexer.setColor(QColor(colors["operator"]), L.Operator)
            # Фоны всех стилей = фон редактора
            for style in range(0, 128):
                try:
                    lexer.setPaper(QColor(bg), style)
                except Exception:
                    pass

        except Exception:
            pass
        return

    # Для остальных лексеров используем универсальные номера стилей.
    # Это не идеально, но визуально тема будет меняться.
    comment_styles = {1, 2, 3, 12, 13, 14}
    keyword_styles = {5, 6, 7, 8, 15, 16, 17}
    string_styles  = {6, 7, 8, 9, 10, 11}
    number_styles  = {4, 9, 10}

    try:
        lexer.setDefaultColor(QColor(colors["default"]))
        lexer.setDefaultPaper(QColor(bg))
    except Exception:
        pass

    for style in range(0, 128):
        color = colors["default"]
        if style in comment_styles:
            color = colors["comment"]
        elif style in keyword_styles:
            color = colors["keyword"]
        elif style in string_styles:
            color = colors["string"]
        elif style in number_styles:
            color = colors["number"]
        try:
            lexer.setColor(QColor(color), style)
            lexer.setPaper(QColor(bg), style)
        except Exception:
            pass

