import sys
import math
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QListWidget, QListWidgetItem, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence, QFont


class ModernVibeCalculatorPro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vibe Calculator PRO ✨")
        self.setMinimumSize(420, 640)
        self.resize(760, 640)

        self.memory = 0.0
        self.scientific_mode = False
        self.history = []  # list[(expr, result)]

        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QWidget#panel {
                background-color: #121214;
            }
            QPushButton {
                background-color: #202024;
                color: #e1e1e6;
                border: none;
                border-radius: 14px;
                font-size: 18px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #29292e;
            }
            QPushButton:pressed {
                background-color: #323238;
            }
            QPushButton[btn_type="operator"] {
                background-color: #ff9800;
                color: #ffffff;
            }
            QPushButton[btn_type="operator"]:hover {
                background-color: #ffa726;
            }
            QPushButton[btn_type="action"] {
                background-color: #00875f;
                color: #ffffff;
            }
            QPushButton[btn_type="action"]:hover {
                background-color: #04d361;
            }
            QPushButton[btn_type="danger"] {
                background-color: #e53e3e;
                color: #ffffff;
            }
            QPushButton[btn_type="danger"]:hover {
                background-color: #fc8181;
            }
            QPushButton[btn_type="sci"] {
                background-color: #2b2b3a;
                color: #b9b9ff;
                font-size: 15px;
            }
            QPushButton[btn_type="sci"]:hover {
                background-color: #38385a;
            }
            QPushButton[btn_type="mem"] {
                background-color: #1c2b2f;
                color: #7fdbca;
                font-size: 14px;
            }
            QPushButton[btn_type="mem"]:hover {
                background-color: #24393f;
            }
            QPushButton#modeToggle {
                background-color: #29292e;
                color: #f5c542;
                font-size: 13px;
                border-radius: 10px;
            }
            QPushButton#modeToggle:hover {
                background-color: #3a3a42;
            }
            QListWidget {
                background-color: #17171a;
                color: #a8a8b3;
                border: none;
                border-radius: 12px;
                font-size: 14px;
                padding: 6px;
            }
            QListWidget::item {
                padding: 8px 6px;
                border-bottom: 1px solid #232327;
            }
            QListWidget::item:hover {
                background-color: #202024;
                border-radius: 8px;
            }
            QLabel#historyTitle {
                color: #7c7c8a;
                font-size: 13px;
                font-weight: 600;
                padding: 4px 2px;
            }
        """)

        root = QWidget()
        root.setObjectName("panel")
        self.setCentralWidget(root)
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # ---------- Cột trái: máy tính ----------
        calc_widget = QWidget()
        layout = QVBoxLayout(calc_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        root_layout.addWidget(calc_widget, 3)

        # Thanh trên: nút chuyển chế độ + copy
        top_bar = QHBoxLayout()
        self.mode_btn = QPushButton("🧪 Khoa học")
        self.mode_btn.setObjectName("modeToggle")
        self.mode_btn.setFixedHeight(32)
        self.mode_btn.clicked.connect(self.toggle_mode)
        top_bar.addWidget(self.mode_btn)
        top_bar.addStretch()
        self.copy_btn = QPushButton("📋 Copy")
        self.copy_btn.setObjectName("modeToggle")
        self.copy_btn.setFixedHeight(32)
        self.copy_btn.clicked.connect(self.copy_result)
        top_bar.addWidget(self.copy_btn)
        layout.addLayout(top_bar)

        # Màn hình hiển thị biểu thức nhỏ phía trên
        self.history_label = QLabel("")
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.history_label.setStyleSheet("color: #7c7c8a; font-size: 15px; min-height: 24px;")
        layout.addWidget(self.history_label)

        # Màn hình kết quả chính
        self.main_display = QLabel("0")
        self.main_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.main_display.setStyleSheet("color: #04d361; font-size: 38px; font-weight: bold; min-height: 55px;")
        self.main_display.setWordWrap(True)
        layout.addWidget(self.main_display)

        # Hàng bộ nhớ (memory)
        mem_row = QHBoxLayout()
        mem_row.setSpacing(8)
        for text in ["MC", "MR", "M+", "M-", "MS"]:
            btn = QPushButton(text)
            btn.setProperty("btn_type", "mem")
            btn.setFixedHeight(34)
            btn.clicked.connect(lambda checked, v=text: self.handle_memory(v))
            mem_row.addWidget(btn)
        layout.addLayout(mem_row)

        # Bàn phím khoa học (ẩn/hiện)
        self.sci_grid_widget = QWidget()
        sci_grid = QGridLayout(self.sci_grid_widget)
        sci_grid.setSpacing(8)
        sci_buttons = [
            ("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("π", "pi"),
            ("log", "log10("), ("ln", "log("), ("√", "sqrt("), ("e", "e"),
            ("x²", "**2"), ("x^y", "**"), ("1/x", "1/("), ("(", "("), (")", ")"),
        ]
        for i, (label, code) in enumerate(sci_buttons):
            btn = QPushButton(label)
            btn.setProperty("btn_type", "sci")
            btn.setFixedHeight(38)
            btn.clicked.connect(lambda checked, v=code: self.insert_sci(v))
            sci_grid.addWidget(btn, i // 4, i % 4)
        layout.addWidget(self.sci_grid_widget)
        self.sci_grid_widget.setVisible(False)

        # Bàn phím máy tính chính
        grid = QGridLayout()
        grid.setSpacing(10)
        layout.addLayout(grid)

        buttons = [
            [("AC", "danger"), ("⌫", "action"), ("%", "operator"), ("/", "operator")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("*", "operator")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("-", "operator")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "operator")],
            [("±", "action"), ("0", "num"), (".", "num"), ("=", "action")]
        ]

        for r, row in enumerate(buttons):
            for c, (text, btype) in enumerate(row):
                btn = QPushButton(text)
                btn.setProperty("btn_type", btype)
                btn.setFixedHeight(55)
                btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                grid.addWidget(btn, r, c)
                btn.clicked.connect(lambda checked, val=text: self.handle_input(val))

        # ---------- Cột phải: lịch sử ----------
        history_widget = QWidget()
        history_widget.setObjectName("panel")
        h_layout = QVBoxLayout(history_widget)
        h_layout.setContentsMargins(0, 20, 20, 20)
        h_layout.setSpacing(6)
        title = QLabel("LỊCH SỬ (bấm để dùng lại)")
        title.setObjectName("historyTitle")
        h_layout.addWidget(title)
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.reuse_history)
        h_layout.addWidget(self.history_list)
        clear_hist_btn = QPushButton("Xóa lịch sử")
        clear_hist_btn.setProperty("btn_type", "danger")
        clear_hist_btn.setFixedHeight(34)
        clear_hist_btn.clicked.connect(self.clear_history)
        h_layout.addWidget(clear_hist_btn)
        root_layout.addWidget(history_widget, 2)

    # ---------- Chế độ ----------
    def toggle_mode(self):
        self.scientific_mode = not self.scientific_mode
        self.sci_grid_widget.setVisible(self.scientific_mode)
        self.mode_btn.setText("🔢 Cơ bản" if self.scientific_mode else "🧪 Khoa học")

    def insert_sci(self, code):
        current = self.main_display.text()
        if current in ["Lỗi cú pháp", "Lỗi chia cho 0", "0"]:
            current = ""
        self.main_display.setText(current + code)

    # ---------- Bộ nhớ ----------
    def handle_memory(self, action):
        try:
            current_val = float(self.evaluate_expr(self.main_display.text()))
        except Exception:
            current_val = None

        if action == "MC":
            self.memory = 0.0
        elif action == "MR":
            self.main_display.setText(self.format_result(self.memory))
        elif action == "M+" and current_val is not None:
            self.memory += current_val
        elif action == "M-" and current_val is not None:
            self.memory -= current_val
        elif action == "MS" and current_val is not None:
            self.memory = current_val

    # ---------- Copy ----------
    def copy_result(self):
        QApplication.clipboard().setText(self.main_display.text())

    # ---------- Lịch sử ----------
    def add_history(self, expr, result):
        self.history.append((expr, result))
        item = QListWidgetItem(f"{expr} = {result}")
        self.history_list.addItem(item)
        self.history_list.scrollToBottom()

    def clear_history(self):
        self.history.clear()
        self.history_list.clear()

    def reuse_history(self, item):
        text = item.text()
        result = text.split("=")[-1].strip()
        self.main_display.setText(result)
        self.history_label.setText("")

    # ---------- Nhập liệu ----------
    def handle_input(self, val):
        current = self.main_display.text()

        if current in ["Lỗi cú pháp", "Lỗi chia cho 0"]:
            current = "0"
            self.main_display.setText("0")

        if val == "AC":
            self.main_display.setText("0")
            self.history_label.setText("")
        elif val == "⌫":
            self.main_display.setText(current[:-1] if len(current) > 1 else "0")
        elif val == "=":
            self.calculate()
        elif val == "±":
            self.toggle_sign()
        elif val == "%":
            try:
                res = float(self.evaluate_expr(current)) / 100
                self.main_display.setText(self.format_result(res))
            except Exception:
                self.main_display.setText("Lỗi cú pháp")
        else:
            ops = ["+", "-", "*", "/"]
            if val in ops:
                if current and current[-1] in ops:
                    self.main_display.setText(current[:-1] + val)
                    return
            elif val == ".":
                last_number = re.split(r"[+\-*/()]", current)[-1]
                if "." in last_number:
                    return

            if current == "0" and val not in ops and val != ".":
                self.main_display.setText(val)
            else:
                self.main_display.setText(current + val)

    def toggle_sign(self):
        current = self.main_display.text()
        try:
            val = float(self.evaluate_expr(current))
            self.main_display.setText(self.format_result(-val))
        except Exception:
            pass

    # ---------- Tính toán ----------
    def evaluate_expr(self, expr):
        safe_globals = {
            "__builtins__": None,
            "sqrt": math.sqrt,
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "log10": math.log10,
            "log": math.log,
            "pi": math.pi,
            "e": math.e,
        }
        return eval(expr, safe_globals, {})

    def format_result(self, result):
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"{result:.10g}" if isinstance(result, float) else str(result)

    def calculate(self):
        expr = self.main_display.text()
        try:
            if expr[-1] in ["+", "-", "*", "/"]:
                raise SyntaxError

            if re.search(r"/\s*0(?!\.\d+)(?!\d)", expr):
                raise ZeroDivisionError

            result = self.evaluate_expr(expr)
            formatted = self.format_result(result)
            self.history_label.setText(expr + " =")
            self.main_display.setText(formatted)
            self.add_history(expr, formatted)
        except ZeroDivisionError:
            self.main_display.setText("Lỗi chia cho 0")
        except Exception:
            self.main_display.setText("Lỗi cú pháp")

    # ---------- Hỗ trợ bàn phím ----------
    def keyPressEvent(self, event):
        key = event.text()
        if key.isdigit() or key in "+-*/.%()":
            self.handle_input(key)
        elif event.key() in (Qt.Key_Enter, Qt.Key_Return):
            self.handle_input("=")
        elif event.key() == Qt.Key_Backspace:
            self.handle_input("⌫")
        elif event.key() == Qt.Key_Escape:
            self.handle_input("AC")
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    window = ModernVibeCalculatorPro()
    window.show()
    sys.exit(app.exec_())