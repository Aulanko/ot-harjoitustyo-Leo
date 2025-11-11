import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget,QVBoxLayout, QGridLayout, QTextEdit

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget, setThemeColor)

from layout_colorwidget import Color
from finance_api import Finance_machine

#https://qfluentwidgets.com/pages/components/navigationbar/#structure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUI()
        self.finance_machine = Finance_machine()
        self.symbols = ["AAPL", "GOOGL", "MSFT"]

        
    def setupUI(self):
        self.setWindowTitle("Financi App")

        main_layout = QVBoxLayout()
    
      
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)  
        self.navigationBar = NavigationInterface(self)


        left_layout.addWidget(self.navigationBar)
        
       
        right_widget = QWidget()
        right_layout = QGridLayout(right_widget)


        #right_layout.addWidget(Color("orange"), 0, 0)
        basic_visual = QTextEdit()
        basic_visual.setPlaceholderText("Stock visualization will appear here")
        right_layout.addWidget(basic_visual, 0,0)


        #right_layout.addWidget(Color("red"), 0, 1)
        basic_info_text = QTextEdit()
        basic_info_text.setPlaceholderText("Stock info logs will appear here")
        right_layout.addWidget(basic_info_text, 0,1)


        #right_layout.addWidget(Color("green"), 1, 0)
        basic_analysis_text = QTextEdit()
        basic_analysis_text.setPlaceholderText("Stock analysis info will appear here")
        right_layout.addWidget(basic_analysis_text, 1,0)


        #right_layout.addWidget(Color("blue"), 1, 1)
       
        main_layout.addWidget(left_widget, 1)   
        main_layout.addWidget(right_widget, 3)   
        
        centralWidget = QWidget()
        centralWidget.setLayout(main_layout)
        self.setCentralWidget(centralWidget)

    
    def load_data(self):

        data = self.finance_machine.get_last_n_data_points(
            symbols=self.symbols,
            interval="1m", 
            n_points=15
        )




        pass

    def construct_basic_info_text(self, data):
        texti = ""
        for symbol, stockData in data.items():
            texti =f"   stock price data for {symbol}   \n"

            texti += stockData[[ 'High', 'Low', 'Close']].to_string()
            text += "\n\n"
            latest = stockData.iloc[-1]
            texti += f"latest close: ${latest['Close']} \n"
            texti += f"Data points: ${len(stockData)}\n"

        self.basic_info_text.setText(texti)




      





app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()

