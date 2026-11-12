import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QLabel)

def parse(argv):
    """argv — список аргументов ПОСЛЕ имени программы (как sys.argv[1:])."""
    do_sort = "--sort" in argv
    pairs = []
    for a in argv:
        if a == "--sort":
            continue
        if "=" in a:
            k, v = a.split("=", 1)
            pairs.append((k, v))
    if do_sort:
        pairs.sort(key=lambda kv: kv[0])
    return "\n".join(f"Key: {k} Value: {v}" for k, v in pairs)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№6 — sys.argv парсер")
        self.resize(600, 400)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Аргументы (как в командной строке):"))
        self.inp = QLineEdit("--sort name=Vasya age=42")
        b = QPushButton("Разобрать")
        b.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.inp); lay.addWidget(b); lay.addWidget(self.out)

    def run(self):
        args = self.inp.text().split()
        self.out.setPlainText(parse(args))

if __name__ == "__main__":
    # Если запущено с аргументами — работаем как CLI, иначе GUI
    if len(sys.argv) > 1:
        print(parse(sys.argv[1:]))
    else:
        app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
