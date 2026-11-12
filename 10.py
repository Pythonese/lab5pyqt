import sys, argparse, textwrap
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QSpinBox, QFileDialog, QLabel)

def format_text_block(frame_height: int, frame_width: int, file_name: str) -> str:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            raw = f.read()
    except Exception as e:
        return str(e)

    # textwrap сохраняет абзацы, переносит длинные строки по словам
    # Для пустых строк сохраняем пустую строку
    wrapped_lines = []
    for paragraph in raw.splitlines():
        if paragraph == "":
            wrapped_lines.append("")
            continue
        chunk = textwrap.wrap(
            paragraph,
            width=frame_width,
            break_long_words=True,
            break_on_hyphens=False,
            replace_whitespace=False,
        ) or [""]
        wrapped_lines.extend(chunk)

    return "\n".join(wrapped_lines[:frame_height])

def build_parser():
    p = argparse.ArgumentParser(add_help=False)
    p.add_argument("--frame-height", type=int, required=False)
    p.add_argument("--frame-width", type=int, required=False)
    p.add_argument("file", nargs="?")
    return p

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№10 — Форматирование в рамке")
        self.resize(700, 600)
        lay = QVBoxLayout(self)
        self.h = QSpinBox(); self.h.setRange(1, 200); self.h.setValue(10)
        self.w = QSpinBox(); self.w.setRange(1, 300); self.w.setValue(30)
        self.path = QLineEdit()
        b_file = QPushButton("Файл...")
        b_file.clicked.connect(self.pick)
        b_run = QPushButton("Форматировать")
        b_run.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        self.out.setStyleSheet("font-family: monospace;")

        lay.addWidget(QLabel("frame-height")); lay.addWidget(self.h)
        lay.addWidget(QLabel("frame-width")); lay.addWidget(self.w)
        lay.addWidget(self.path); lay.addWidget(b_file)
        lay.addWidget(b_run); lay.addWidget(self.out)

    def pick(self):
        f, _ = QFileDialog.getOpenFileName(self, "Файл")
        if f: self.path.setText(f)

    def run(self):
        self.out.setPlainText(
            format_text_block(self.h.value(), self.w.value(), self.path.text().strip())
        )

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p = build_parser()
        ns = p.parse_args()
        print(format_text_block(ns.frame_height, ns.frame_width, ns.file))
    else:
        app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
