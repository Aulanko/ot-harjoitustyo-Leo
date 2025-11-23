
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QGridLayout, QTextEdit,
                             QPushButton, QLineEdit)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setUpUI()

        

    def setUpUI(self):
        self.setWindowTitle("Stock data application")

        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QHBoxLayout()
        center_widget.setLayout(main_layout)

        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel)



        pass

    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        title = QLabel("Analyze Stocks")
        layout.addWidget(title)

        layout.addWidget(QLabel("Symbols:"))
        self.symbols = QTextEdit()

        layout.addWidget(self.symbols)

        symbol_layout = QHBoxLayout()
        self.new_symbol = QLineEdit()
        self.new_symbol.setPlaceholderText("Add a new symbol (for example; NVDA)")
        symbol_layout.addWidget(self.new_symbol)

        add_button = QPushButton("Add")
        #add_button.clicked.connect()
        symbol_layout.addWidget(add_button)
        layout.addLayout(symbol_layout)

        analyze_button = QPushButton("Analyze")
        #analyze_button.clicked.connect()

        layout.addWidget(analyze_button)

        return panel
    











def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main_window()