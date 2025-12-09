from typing import Dict
import logging
import sys
from PyQt6.QtWidgets import (QApplication,
                             QMainWindow,
                             QWidget,
                             QVBoxLayout,
                             QHBoxLayout,
                             QLabel,
                             QGridLayout,
                             QTextEdit,
                             QPushButton,
                             QLineEdit)


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import yfinance as yf


from analysis.analyzer import StockAnalysis
from models.stock import StockData
from repositories.stock_repo import StockRepository
from ui.get_immeadiate_info import GetImmediateInfo


class MainWindow(QMainWindow):
    """
    Tämä luokka on vastuussa suurimmilta osin käyttöliittymän rakentamisesta ja
    yhdistää toiminnallisia luokkia käyttöliittymään.
    """
    def __init__(self):
        """
        
        
        Args:
            current_symbols: Alustavat osakesymbolit
            logger: debuggaukseen tarkoitettu loggeri
            data_ticker_widgets: ylläpitää osakesymbolien ja "välittömän" infon arvon välistä
            suhdetta.
            symbols: symbolit, joita käytetään koodissa
            new_symbol: uuden symbolin luontia varten varastointi muuttujaan
            price_chart: Kuvaaja, joka tulee visualisoimaan osakkeiden hintoja pylväs diagrammina
            data_display: näyttää yksityiskohtaisempaa raakadataa osakkeista
            analysis_display: näyttää teknisempiä analyysi tuloksia (esim Williams %R)
        
        """
        super().__init__()
        self.current_symbols = ["AAPL", "GOOGL"]

        self.logger = logging.getLogger(__name__)
        self.data_ticker_widgets = {}
        self.symbols = None
        self.new_symbol = None
        self.price_chart = None
        self.data_display = None
        self.analysis_display = None

        self.analyzer = StockAnalysis(StockRepository())
        self.set_ui_up()

    def set_ui_up(self):
        """
        Alustaa käyttöliittymän + vasemman ja oikean paneelin asettelun.
        """
        self.setWindowTitle("Stock data application")

        center_widget = QWidget()
        self.setCentralWidget(center_widget)
        main_layout = QHBoxLayout()
        center_widget.setLayout(main_layout)

        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)

        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel)

    def create_left_panel(self):
        """
        Luo vasemman puoleisen paneelin, jossa symbolien syöttämisen,
        lisäämisen ja analyysin käynnistämisen toiminnot.
        """
        panel = QWidget()
        layout = QVBoxLayout()
        panel.setLayout(layout)

        title = QLabel("Analyze Stocks")
        layout.addWidget(title)

        layout.addWidget(QLabel("Symbols:"))
        self.symbols = QTextEdit(f"{self.current_symbols}")
        layout.addWidget(self.symbols)

        symbol_layout = QHBoxLayout()
        self.new_symbol = QLineEdit()
        self.new_symbol.setPlaceholderText("Add a new symbol")
        symbol_layout.addWidget(self.new_symbol)

        add_button = QPushButton("Add")
        add_button.clicked.connect(self.handle_add_symbol)
        symbol_layout.addWidget(add_button)

        layout.addLayout(symbol_layout)

        analyze_button = QPushButton("Analyze")
        analyze_button.clicked.connect(self.refresh_data)

        layout.addWidget(analyze_button)

        return panel

    def create_right_panel(self):
        """
        Luo oikean puoleista paneelia, jossa osaketietojen "hätä" tiedot, hintakuvaajan,
        raaka-datan ja analyysitulosten näyttöalueet
        """
        panel = QWidget()
        layout = QGridLayout()
        panel.setLayout(layout)

        self.data_ticker_widgets = {}
        for i, symbol in enumerate(self.current_symbols):
            tick = GetImmediateInfo(symbol, 0, 0)
            self.data_ticker_widgets[symbol] = tick
            layout.addWidget(tick, 0, i)

        self.price_chart = FigureCanvas(Figure(figsize=(10, 4)))
        layout.addWidget(self.price_chart, 1, 0, 1, len(self.current_symbols))

        self.data_display = QTextEdit()
        self.data_display.setPlaceholderText("Stock Data shall appear..")
        layout.addWidget(self.data_display, 2, 0, 1, 2)

        self.analysis_display = QTextEdit()
        self.analysis_display.setPlaceholderText(
            "Analysis Data shall appear..")
        layout.addWidget(self.analysis_display, 2, 2, 1, 2)

        return panel

    def add_ticker_widget(self, symbol: str):
        """
        Luo ja lisää uuden GetImmediateInfon ticker widget yläinfoon kun käyttäjä lisää
        uuden osakkeen
        """
        tick = GetImmediateInfo(symbol, 0, 0)
        self.data_ticker_widgets[symbol] = tick

        right_panel = self.price_chart.parentWidget()
        layout = right_panel.layout()

        col = len(self.data_ticker_widgets) - 1
        layout.addWidget(tick, 0, col)

    def handle_add_symbol(self):
        """
        Päivittää nykyisten symbolien tilaa uudella symbolilla 
        + validoi symbolia. 
        """
        symbol = self.new_symbol.text().strip().upper()
        if symbol in self.current_symbols:
            return
        if not symbol:
            return

        try:
            stock_to_look = yf.Ticker(symbol)
            info = stock_to_look.history(period="1d")
            if info.empty:
                self.logger.warning(
                    "Symbol tried to be added not found in Yahoo Finance")
                self.new_symbol.clear()
                return
        except (ConnectionError, TimeoutError) as e:
            self.logger.waring(
                "Error trying to add a symbol to current_symbols: %s", e)

        self.current_symbols.append(symbol)
        self.symbols.setText(str(self.current_symbols))
        self.add_ticker_widget(symbol)
        self.new_symbol.clear()

    def refresh_data(self):
        """
        Päivittää paneeleja ja tekstikenttiä + kuvaajan, nykyisen datan mukaan
        """
        try:
            current_data = self.analyzer.get_current_data_for_multiple_symbols(
                self.current_symbols)
            if current_data:
                self.update_data_ticker_widgets(current_data)
                self.update_displayed_data(current_data)
                self.visualized_comparison(current_data)
        except (ConnectionError, TimeoutError) as e:
            self.logger.warning("error on refresh_data: %s", e)

    def update_data_ticker_widgets(self, stock_data: Dict[str, StockData]):
        """
        Päivittää yläinfossa olevien hintojen muutoksia. 
        """

        for symbol, data in stock_data.items():
            if data and symbol in self.data_ticker_widgets:

                change_percentage = (
                    data.close-data.open_price)/data.open_price*100
                self.data_ticker_widgets[symbol].update_data(
                    data.close, change_percentage)

    def update_displayed_data(self, stock_data: Dict[str, StockData]):
        texti = "Stock data \n\n"
        analysis_texti = "Stock analysis \n\n"

        for symbol, data in stock_data.items():
            if data:
                real_change_percent = (
                    data.close-data.open_price)/data.open_price*100

                texti += f"symbol: {symbol}\n"
                texti += f"Timestamp on close: {data.timestamp.replace(tzinfo=None)}\n"
                texti += f"change: {real_change_percent} \n"
                texti += f"opening price: {data.open_price} \n"
                texti += f"closing price: {data.close} \n"
                texti += f"Volume: {data.volume} \n\n\n"

                williams_r = self.analyzer.calculate_over_bought_and_oversold(
                    symbol)

                analysis_texti += "Williams Percent Range (-100 to 0).\
                -50 as the middle point. Under it -> more oversold, over it -> more over bought\n"
                analysis_texti += f"for stock: {symbol}, we got: {williams_r}\n\n"

                sma = self.analyzer.calculate_moving_averages(symbol)
                analysis_texti += f"For symbol: {symbol}. \n Moving averages of 20 days:\
                {sma["closed_list20"]} \n"
                analysis_texti += f"Moving averages of 50 days: {sma["closed_list50"]}\n"
                analysis_texti += f"Moving averages of 200 days: {sma["closed_list200"]}\n\n"

        self.data_display.setText(texti)
        self.analysis_display.setText(analysis_texti)

    def visualized_comparison(self, stock_data: Dict[str, StockData]):
        figure = self.price_chart.figure

        figure.clear()
        axes = figure.add_subplot(111)

        symbols = []
        prices = []

        for symbol, data in stock_data.items():
            symbols.append(symbol)
            prices.append(data.close)

        bars = axes.bar(symbols, prices)
        axes.set_ylabel("Price")
        axes.set_xlabel("Companies")
        axes.set_title("Stock prices")

        for baari, price in zip(bars, prices):
            bar_height = baari.get_height()
            axes.text(baari.get_x() + baari.get_width()/2., bar_height,
                      f'{price:.3f}$', ha='center', va='bottom')
        self.price_chart.draw()


def main_window():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main_window()
