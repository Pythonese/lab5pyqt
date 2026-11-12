import sys, argparse
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit)

def build_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--sort", action="store_true")
    p.add_argument("pairs", nargs="*")
    return p

def process(argv):
    p = build_parser()
    ns = p.parse_args(argv)
    items = []
    for a in ns.pairs:
        if "=" in a:
            k, v = a.split("=", 1)
            items.append((k, v))
    if ns.sort:
        items.sort(key=lambda kv: kv[0])
    return "\n".join(f"Key: {k} Value: {v}" for k, v in items)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№9 — argparse-версия №6")
        self.resize(600, 400)
        lay = QVBoxLayout(self)
        self.inp = QLineEdit("--sort name=Vasya age=42")
        b = QPushButton("Разобрать")
        b.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.inp); lay.addWidget(b); lay.addWidget(self.out)

    def run(self):
        self.out.setPlainText(process(self.inp.text().split()))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(process(sys.argv[1:]))
    else:
        app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
