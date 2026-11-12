import sys, zipfile
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLabel, QLineEdit, QFileDialog)

UNITS = ["Б", "КБ", "МБ", "ГБ", "ТБ"]

def human_size(n: int) -> str:
    idx, val = 0, float(n)
    while val >= 1023 and idx < len(UNITS) - 1:
        val /= 1024.0
        idx += 1
    return f"{round(val)}{UNITS[idx]}"

def zip_tree(zip_path: str) -> str:
    with zipfile.ZipFile(zip_path) as z:
        infos = z.infolist()
    # словарь: путь -> (это_каталог, размер)
    tree = {}
    for info in infos:
        name = info.filename.rstrip("/")
        if not name:
            continue
        is_dir = info.is_dir()
        tree[name] = (is_dir, info.file_size)

    # формируем иерархию: сортируем и выводим по уровням
    # для каждого пути строим цепочку предков, чтобы вывести каталоги
    # Соберём все узлы (включая промежуточные каталоги)
    nodes = {}
    for path, (is_dir, size) in tree.items():
        parts = path.split("/")
        for i in range(1, len(parts) + 1):
            sub = "/".join(parts[:i])
            if sub not in nodes:
                nodes[sub] = [is_dir or i < len(parts), size if i == len(parts) else None]

    lines = []
    def walk(prefix: str, depth: int):
        children = sorted({p for p in nodes if p.rsplit("/", 1)[0] == prefix} |
                          {p for p in nodes if "/" not in p and prefix == ""})
        # Упростим: рекурсивный обход по полному пути
    # Проще: сортированный вывод с учётом глубины
    all_paths = sorted(nodes.keys(), key=lambda s: (s.lower()))
    # Для корректного дерева: обходим рекурсивно
    def children_of(parent):
        res = []
        plen = len(parent)
        for p in all_paths:
            if parent and not p.startswith(parent + "/"):
                continue
            if not parent and "/" in p:
                continue
            if parent:
                rest = p[plen + 1:]
            else:
                rest = p
            if "/" not in rest:
                res.append(p)
        return sorted(res, key=lambda s: s.lower())

    def dfs(parent, depth):
        for p in children_of(parent):
            is_dir, size = nodes[p]
            name = p.rsplit("/", 1)[-1]
            indent = "  " * depth
            if is_dir:
                lines.append(f"{indent}{name}")
            else:
                lines.append(f"{indent}{name} {human_size(size)}")
            dfs(p, depth + 1)

    dfs("", 0)
    return "\n".join(lines)

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("№2 — Структура zip")
        self.resize(600, 500)
        lay = QVBoxLayout(self)
        self.path = QLineEdit()
        btn_file = QPushButton("Выбрать zip...")
        btn_file.clicked.connect(self.pick)
        btn_run = QPushButton("Показать структуру")
        btn_run.clicked.connect(self.run)
        self.out = QTextEdit(); self.out.setReadOnly(True)
        lay.addWidget(self.path); lay.addWidget(btn_file)
        lay.addWidget(btn_run); lay.addWidget(self.out)

    def pick(self):
        f, _ = QFileDialog.getOpenFileName(self, "zip", "", "*.zip")
        if f: self.path.setText(f)

    def run(self):
        try:
            self.out.setPlainText(zip_tree(self.path.text().strip()))
        except Exception as e:
            self.out.setPlainText(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv); w = App(); w.show(); sys.exit(app.exec())
