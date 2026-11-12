import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QFileDialog, QLabel)

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ", "ПБ"]

def human_size(n: int) -> str:
    idx, val = 0, float(n)
    while val >= 1023 and idx < len(UNITS) - 1:
        val /= 1024.0
        idx += 1
    return f"{round(val)}{UNITS[idx]}"

def top10_dirs(root: str) -> str:
    """TOP-10 каталогов по суммарному размеру вложений (рекурсивно)."""
    root = os.path.abspath(root)
    # sizes[dir] = суммарный размер всех вложений (файлы + подпапки)
    sizes = {}

    # topdown=False: сначала обрабатываются листья, затем родители
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        total = 0
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
        # добавляем размеры уже посчитанных подпапок
        for d in dirnames:
            sub = os.path.join(dirpath, d)
            total += sizes.get(sub, 0)
        sizes[dirpath] = total

    # исключаем сам корень — интересуют вложенные каталоги
    items = [(p, s) for p, s in sizes.items()
             if os.path.normpath(p) != os.path.normpath(root)]
    items.sort(key=lambda kv: kv[1], reverse=True)
    items = items[:10]

    lines = []
    for path, size in items:
        # показываем путь относительно корня для наглядности
        rel = os.path.relpath(path, root)
        lines.append(f"{rel}  - {human_size(size)}")
    return "\n".join(lines) if lines else "(нет каталогов)"


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№3 — TOP-10 каталогов по размеру вложений")
        self.resize(650, 500)
        lay = QVBoxLayout(self)

        self.path = QLineEdit(os.getcwd())
        b_pick = QPushButton("Выбрать папку...")
        b_pick.clicked.connect(self.pick)
        b_run = QPushButton("Показать TOP-10")
        b_run.clicked.connect(self.run)

        self.out = QTextEdit()
        self.out.setReadOnly(True)
        self.out.setStyleSheet("font-family: monospace;")

        lay.addWidget(QLabel("Корневой путь:"))
        lay.addWidget(self.path)
        lay.addWidget(b_pick)
        lay.addWidget(b_run)
        lay.addWidget(self.out)

    def pick(self):
        d = QFileDialog.getExistingDirectory(self, "Выберите папку")
        if d:
            self.path.setText(d)

    def run(self):
        try:
            self.out.setPlainText(top10_dirs(self.path.text().strip()))
        except Exception as e:
            self.out.setPlainText(f"Ошибка: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
