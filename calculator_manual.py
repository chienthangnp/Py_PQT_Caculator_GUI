import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QGridLayout, QLineEdit, QPushButton
)
from PyQt5.QtCore import Qt

class StandardCalculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Máy Tính Cá Nhân - Bản Code Tay")
        self.setFixedSize(320, 420)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self.display = QLineEdit()
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 22px; padding: 5px;")
        main_layout.addWidget(self.display)

        grid_layout = QGridLayout()
        main_layout.addLayout(grid_layout)

        buttons = [
            ('C', 0, 0), ('CE', 0, 1), ('<', 0, 2), ('/', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('*', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('-', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('+', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2, 1, 2)
        ]

        for item in buttons:
            text = item[0]
            row, col = item[1], item[2]
            row_span = item[3] if len(item) > 3 else 1
            col_span = item[4] if len(item) > 4 else 1

            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setStyleSheet("font-size: 16px; font-weight: bold;")
            btn.clicked.connect(lambda checked, ch=text: self.on_button_click(ch))
            grid_layout.addWidget(btn, row, col, row_span, col_span)

    def on_button_click(self, char):
        current_text = self.display.text()

        if current_text in ["Lỗi cú pháp", "Lỗi chia cho 0"]:
            self.display.clear()
            current_text = ""

        if char == 'C' or char == 'CE':
            self.display.clear()
        elif char == '<':
            self.display.setText(current_text[:-1])
        elif char == '=':
            self.calculate_result()
        else:
            ops = ['+', '-', '*', '/']
            if char in ops:
                if not current_text:
                    if char != '-': 
                        return
                elif current_text[-1] in ops:
                    self.display.setText(current_text[:-1] + char)
                    return
            elif char == '.':
                parts = current_text.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
                if parts and '.' in parts[-1]:
                    return
                if not current_text or current_text[-1] in ops:
                    char = "0."

            self.display.setText(current_text + char)

    def calculate_result(self):
        expr = self.display.text().strip()
        if not expr:
            return

        if expr[-1] in ['+', '-', '*', '/']:
            self.display.setText("Lỗi cú pháp")
            return

        try:
            if "/0" in expr:
                import re
                if re.search(r"/\s*0(?!\.\d+)", expr):
                    raise ZeroDivisionError

            result = eval(expr, {"__builtins__": None}, {})
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.display.setText(str(result))
        except ZeroDivisionError:
            self.display.setText("Lỗi chia cho 0")
        except Exception:
            self.display.setText("Lỗi cú pháp")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StandardCalculator()
    window.show()
    sys.exit(app.exec_())