import sys, argparse
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit)

def build_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("a", nargs="?", default=None)
    p.add_argument("b", nargs="?", default=None)
    return p

def run_calc(argv):
    p = build_parser()
    try:
        ns = p.parse_args(argv)
    except SystemExit:
        return "TOO MANY PARAMS"
    raws = [x for x in (ns.a, ns.b) if x is not None]
    if not raws:
        return "NO PARAMS"
    # считаем «целочисленные параметры»
    ints = []
    other_error = None
    for r in raws:
        try:
            ints.append(int(r))
        except Exception as e:
            other_error = type(e).__name__
    if other_error:
        return other_error
    if len(ints) == 1 and len(raws) == 1:
        return "TOO FEW PARAMS"
    if len(raws) > 2:
        return "TOO MANY PARAMS"
    if len(ints) == 2:
        return str(ints[0] + ints[1])
    return "TOO FEW PARAMS"

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№8 — Калькулятор (argparse)")
        self.resize(500, 300)
        lay = QVBoxLayout(self)
        self.inp = QLineEdit("3 5")
        b = QPushButton("Считать")
        b.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.inp); lay.addWidget(b); lay.addWidget(self.out)

    def run(self):
        self.out.setPlainText(run_calc(self.inp.text().split()))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(run_calc(sys.argv[1:]))
    else:
        app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
