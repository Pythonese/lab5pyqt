import os, sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QFileDialog, QLabel)

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

def human_size(n):
    idx, val = 0, float(n)
    while val >= 1023 and idx < len(UNITS) - 1:
        val /= 1024.0; idx += 1
    return f"{round(val)}{UNITS[idx]}"

def dir_sizes(root: str):
    """Возвращает словарь каталог -> суммарный размер всех вложений."""
    sizes = {}
    for dirpath, dirnames, filenames in os.walk(root):
        total = 0
        for f in filenames:
            fp = os.path.join(dirpath, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
        # поднимаемся по дереву, добавляя вклад каждому предку
        cur = dirpath
        while True:
            sizes[cur] = sizes.get(cur, 0) + total
            if os.path.normpath(cur) == os.path.normpath(root):
                break
            parent = os.path.dirname(cur)
            if parent == cur:
                break
            cur = parent
    return sizes

def top10(root: str) -> str:
    sizes = dir_sizes(root)
    # исключим сам корень? В задаче «каталоги» — оставим как есть
    items = sorted(sizes.items(), key=lambda kv: kv[1], reverse=True)[:10]
    res = []
    for path, size in items:
        name = os.path.basename(path.rstrip(os.sep)) or path
        res.append(f"{name}  - {human_size(size)}")
    return "\n".join(res)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№3 — TOP-10 каталогов")
        self.resize(600, 500)
        lay = QVBoxLayout(self)
        self.path = QLineEdit(os.getcwd())
        b1 = QPushButton("Выбрать папку")
        b1.clicked.connect(self.pick)
        b2 = QPushButton("Показать TOP-10")
        b2.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.path); lay.addWidget(b1); lay.addWidget(b2)
        lay.addWidget(self.out)

    def pick(self):
        d = QFileDialog.getExistingDirectory(self, "Папка")
        if d: self.path.setText(d)

    def run(self):
        try:
            self.out.setPlainText(top10(self.path.text().strip()))
        except Exception as e:
            self.out.setPlainText(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
