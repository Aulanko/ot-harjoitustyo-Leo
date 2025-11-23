
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QGridLayout, QTextEdit,
                             QPushButton)
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setUpUI()

    def setUpUI(self):
        pass





def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__=="__main_window__":
    main_window()