import os
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout,
                             QPushButton, QTextEdit, QLabel)

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ", "ПБ"]

def human_size(n: int) -> str:
    """Размер только в старших единицах, переход через 1023, round до целого."""
    idx = 0
    val = float(n)
    while val >= 1023 and idx < len(UNITS) - 1:
        val /= 1024.0
        idx += 1
    # round по правилам задачи (обычное округление)
    return f"{round(val)}{UNITS[idx]}"

def collect_files(path: str = ".") -> str:
    lines = []
    for entry in sorted(os.listdir(path)):
        full = os.path.join(path, entry)
        if os.path.isfile(full):
            lines.append(f"{entry} {human_size(os.path.getsize(full))}")
    return "\n".join(lines)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№1 — Человекочитаемые размеры файлов")
        self.resize(500, 500)
        lay = QVBoxLayout(self)
        lay.addWidget(QLabel("Текущая папка: " + os.getcwd()))
        self.btn = QPushButton("Получить список")
        self.out = QTextEdit()
        self.out.setReadOnly(True)
        self.btn.clicked.connect(lambda: self.out.setPlainText(collect_files(".")))
        lay.addWidget(self.btn)
        lay.addWidget(self.out)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App(); w.show()
    sys.exit(app.exec())
