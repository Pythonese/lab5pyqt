import sys, argparse
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QLabel)

def build_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("params", nargs="*")
    return p

def process(argv):
    p = build_parser()
    ns = p.parse_args(argv)
    if not ns.params:
        return "no args"
    return "\n".join(ns.params)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№7 — Много параметров (argparse)")
        self.resize(500, 400)
        lay = QVBoxLayout(self)
        self.inp = QLineEdit("5 string 1")
        b = QPushButton("Выполнить")
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
