import sys, datetime, threading, time
import schedule
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLabel)
from PyQt6.QtCore import QObject, pyqtSignal

class Signals(QObject):
    log = pyqtSignal(str)

sig = Signals()

def koo_job():
    now = datetime.datetime.now()
    h12 = now.hour % 12 or 12
    line = "Ку\n" * h12
    sig.log.emit(f"[{now:%H:%M:%S}] {h12} раз(а):\n{line.strip()}")

def scheduler_loop():
    schedule.every().hour.at(":00").do(koo_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№5 — Планировщик «Ку»")
        self.resize(500, 400)
        lay = QVBoxLayout(self)
        self.btn_start = QPushButton("Запустить планировщик")
        self.btn_test = QPushButton("Проверить сейчас")
        self.out = QTextEdit(); self.out.setReadOnly(True)
        self.btn_start.clicked.connect(self.start)
        self.btn_test.clicked.connect(koo_job)
        sig.log.connect(self.append)
        lay.addWidget(self.btn_start); lay.addWidget(self.btn_test); lay.addWidget(self.out)

    def append(self, text):
        self.out.append(text)

    def start(self):
        threading.Thread(target=scheduler_loop, daemon=True).start()
        self.out.append("Планировщик запущен (каждый час в :00).")

if __name__ == "__main__":
    app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
