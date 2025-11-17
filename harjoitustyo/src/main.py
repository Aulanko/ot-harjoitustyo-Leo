import sys

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget,QVBoxLayout, QGridLayout, QTextEdit,
                            QPushButton)

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, MessageBox,
                            isDarkTheme, setTheme, Theme,
                            PopUpAniStackedWidget, setThemeColor)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanva
from matplotlib.figure import Figure

from layout_colorwidget import Color
from finance_api import Finance_machine
from visual import Visualize
from analyze import Analyze

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
        button = QPushButton("Load")
        self.navigationBar.addItem(
            routeKey="/",
            icon="Download",
            text="Load",
            onClick = self.load_data
        )
        
        left_layout.addWidget(self.navigationBar)
        
       
        right_widget = QWidget()
        right_layout = QGridLayout(right_widget)


        #right_layout.addWidget(Color("orange"), 0, 0)
        self.basic_visual = FigureCanva(Figure(figsize=(10,4)))
        #basic_visual = QTextEdit()
        #basic_visual.setPlaceholderText("Stock visualization will appear here")
        right_layout.addWidget(self.basic_visual, 0,0)


        #right_layout.addWidget(Color("red"), 0, 1)
        self.basic_info_text = QTextEdit()
        self.basic_info_text.setPlaceholderText("Stock info logs will appear here")
        right_layout.addWidget(self.basic_info_text, 0,1)


        #right_layout.addWidget(Color("green"), 1, 0)
        self.basic_analysis_text = QTextEdit()
        self.basic_analysis_text.setPlaceholderText("Stock analysis info will appear here")
        right_layout.addWidget(self.basic_analysis_text, 1,0)


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

        self.construct_basic_info_text(data)

        self.construct_basic_analysis(data)

        visual = Visualize()

        first_symbol = list(data.keys())[0]

        stock_data_for_plotting = data[first_symbol] 

        fig = visual.make_a_graph_from_prices(stock_data_for_plotting, "High", first_symbol)

        self.basic_visual.figure.clear()
        self.basic_visual.figure = fig
        self.basic_visual.draw()



        pass

    def construct_basic_info_text(self, data):
        texti = ""
        for symbol, stockData in data.items():
            texti +=f"   stock price data for {symbol}   \n                "

            texti += stockData[['High', 'Low', 'Close']].to_string()
            texti += "\n\n"
            latest = stockData.iloc[-1]
            texti += f"latest close: {latest['Close']} \n"
            texti += f"Data points: {len(stockData)}\n\n"

        self.basic_info_text.setText(texti)

    def construct_basic_analysis(self, data):

        

        analyzer = Analyze()
      

        texti = ""
        for symbol, stock_data_for_plotting in data.items():
            mean = analyzer.mean(stock_data_for_plotting)
            minimum = analyzer.minimum(stock_data_for_plotting)
            maximum = analyzer.maximum(stock_data_for_plotting)

            texti +=f"stock price data analysis for {symbol}   \n         "
            texti += "\n\n"
            texti += f"mean: {mean} \n"
            texti +=f"minimum: {minimum}\n"
            texti += f"maximum: {maximum} \n\n"
            print(stock_data_for_plotting["High"])
        
        self.basic_analysis_text.setText(texti)

        
        pass



   

def main():
    app = QApplication(sys.argv)
    window= MainWindow()
    window.show()
    app.exec()

if __name__=="__main__":
    main()
