import os, sys, datetime, shutil
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QFileDialog, QLabel)

def make_reserve_arc(source: str, dest: str) -> str:
    """Архивирует source в dest, имя содержит дату/время до секунды. Возвращает путь."""
    if not os.path.isdir(source):
        raise NotADirectoryError(source)
    os.makedirs(dest, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_name = f"reserve_{os.path.basename(os.path.normpath(source))}_{ts}"
    out_path = shutil.make_archive(
        base_name=os.path.join(dest, base_name),
        format="zip",
        root_dir=os.path.dirname(os.path.abspath(source)),
        base_dir=os.path.basename(os.path.abspath(source)),
    )
    return out_path

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№4 — Резервная архивация")
        self.resize(600, 400)
        lay = QVBoxLayout(self)
        self.src = QLineEdit(); self.dst = QLineEdit()
        b_src = QPushButton("Источник...")
        b_dst = QPushButton("Назначение...")
        b_run = QPushButton("Создать архив")
        self.out = QTextEdit(); self.out.setReadOnly(True)

        b_src.clicked.connect(lambda: self.pick_dir(self.src))
        b_dst.clicked.connect(lambda: self.pick_dir(self.dst))
        b_run.clicked.connect(self.run)

        lay.addWidget(QLabel("source:")); lay.addWidget(self.src); lay.addWidget(b_src)
        lay.addWidget(QLabel("dest:")); lay.addWidget(self.dst); lay.addWidget(b_dst)
        lay.addWidget(b_run); lay.addWidget(self.out)

    def pick_dir(self, le):
        d = QFileDialog.getExistingDirectory(self, "Папка")
        if d: le.setText(d)

    def run(self):
        try:
            p = make_reserve_arc(self.src.text().strip(), self.dst.text().strip())
            self.out.setPlainText(f"Создан архив:\n{p}")
        except Exception as e:
            self.out.setPlainText(f"Ошибка: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
