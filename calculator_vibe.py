import sys
import re
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QLabel, QPushButton
)
from PyQt5.QtCore import Qt

class ModernVibeCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vibe Calculator ✨")
        self.setFixedSize(360, 520)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121214;
            }
            QPushButton {
                background-color: #202024;
                color: #e1e1e6;
                border: none;
                border-radius: 12px;
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
        """)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # Màn hình hiển thị biểu thức nhỏ phía trên
        self.history_label = QLabel("")
        self.history_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.history_label.setStyleSheet("color: #7c7c8a; font-size: 15px; min-height: 24px;")
        layout.addWidget(self.history_label)

        # Màn hình kết quả chính
        self.main_display = QLabel("0")
        self.main_display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.main_display.setStyleSheet("color: #04d361; font-size: 38px; font-weight: bold; min-height: 55px;")
        layout.addWidget(self.main_display)

        # Bàn phím máy tính
        grid = QGridLayout()
        grid.setSpacing(10)
        layout.addLayout(grid)

        buttons = [
            [("AC", "danger"), ("⌫", "action"), ("%", "operator"), ("/", "operator")],
            [("7", "num"), ("8", "num"), ("9", "num"), ("*", "operator")],
            [("4", "num"), ("5", "num"), ("6", "num"), ("-", "operator")],
            [("1", "num"), ("2", "num"), ("3", "num"), ("+", "operator")],
            [("0", "num"), (".", "num"), ("=", "action")]
        ]

        for r, row in enumerate(buttons):
            for c, (text, btype) in enumerate(row):
                btn = QPushButton(text)
                btn.setProperty("btn_type", btype)
                btn.setFixedHeight(55)

                if text == "=":
                    grid.addWidget(btn, r, c, 1, 2)
                else:
                    grid.addWidget(btn, r, c)

                btn.clicked.connect(lambda checked, val=text: self.handle_input(val))

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
        elif val == "%":
            try:
                res = float(current) / 100
                self.main_display.setText(f"{res:.6g}")
            except Exception:
                self.main_display.setText("Lỗi cú pháp")
        else:
            ops = ["+", "-", "*", "/"]
            if val in ops:
                if current[-1] in ops:
                    self.main_display.setText(current[:-1] + val)
                    return
            elif val == ".":
                last_number = re.split(r"[+\-*/]", current)[-1]
                if "." in last_number:
                    return

            if current == "0" and val not in ops and val != ".":
                self.main_display.setText(val)
            else:
                self.main_display.setText(current + val)

    def calculate(self):
        expr = self.main_display.text()
        self.history_label.setText(expr + " =")
        try:
            if expr[-1] in ["+", "-", "*", "/"]:
                raise SyntaxError

            # Kiểm tra phép chia cho 0
            if re.search(r"/\s*0(?!\.\d+)", expr):
                raise ZeroDivisionError

            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.main_display.setText(f"{result:.8g}" if isinstance(result, float) else str(result))
        except ZeroDivisionError:
            self.main_display.setText("Lỗi chia cho 0")
        except Exception:
            self.main_display.setText("Lỗi cú pháp")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ModernVibeCalculator()
    window.show()
    sys.exit(app.exec_())