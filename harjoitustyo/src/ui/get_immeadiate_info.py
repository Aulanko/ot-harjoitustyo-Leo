

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,

    QLabel,
)
from PyQt6.QtCore import Qt


class GetImmediateInfo(QWidget):

    def __init__(self, symbol: str, price: float, change: float):
        super().__init__()
        self.symbol = symbol
        self.stock_service = None
        self.price = price
        self.change = change
        self.color = ""
        self.sign = ""
        self.set_ui_up()

    def set_ui_up(self):

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.symbol_label = QLabel(f"{self.symbol}")
        self.price_label = QLabel(f"{self.price}$")
        self.change_label = QLabel()

        layout.addWidget(self.symbol_label)
        layout.addWidget(self.price_label)
        layout.addWidget(self.change_label)

        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def update_data(self, price: float, change: float):
        self.price = price
        self.change = change

        if self.change >= 0:
            self.color = "green"
            self.sign = "+"
        else:
            self.color = "red"
            self.sign = "-"

        self.price_label.setText(f"{price}$")
        self.change_label.setText(f"{self.sign}{abs(self.change)}%")
        self.change_label.setStyleSheet(f"color: {self.color}")
