
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QLabel, QGridLayout, QTextEdit,
                             QPushButton, QLineEdit)
import sys




class DataTickerWidget(QLabel):
    pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.CurrentSymbols = ["AAPL","GOOGL"]
        self.setUpUI()
        

        

    def setUpUI(self):
        self.setWindowTitle("Stock data application")

        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QHBoxLayout()
        center_widget.setLayout(main_layout)

        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)

        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)



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
    
    def create_right_panel(self):
        panel = QWidget()
        layout = QGridLayout()
        panel.setLayout(layout)

        self.data_ticker_widgets = {}
        for i, symbol in enumerate(self.CurrentSymbols):
            print("koira")




        pass
    











def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main__":
    main_window()