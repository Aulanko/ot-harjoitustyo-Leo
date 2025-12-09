import logging

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

import sqlite3
import json
from datetime import datetime

import yfinance as yf
import pandas as pd

from redis import Redis
from redis.exceptions import RedisError


from models.stock import StockData, DataFactory


class SpotStockDataError(Exception):
    """
    Virheiden käsittelyä tehty luokka, jota käytetään, 
    jos tulee osakedatan käsittelyn kanssa ongelmia
    """

    def __init__(self, symbol: str, message: str = None):
        self.symbol = symbol
        self.message = message or \
            f"An error occurred when doing operation on stockData symbol: {self.symbol}"
        super().__init__(self.message)

    def log_error(self):
        print(f"[SpotStockDataError] {self.symbol}:{self.message}")

    def dict_form_log(self):
        return {"stock_data for symbol": self.symbol, "message": self.message}


class DataSourceFailed(Exception):
    """
    Virheiden käsittelyluokka, jota käytetään jos datan hakemisen kanssa tulee ongelmia
    """

    def __init__(self, source=None, message: str = None):
        self.source = source
        self.message = message or f"An error occured when trying to fetch data from: {self.source}"
        super().__init__(self.message)

    def log_error(self):
        print(f"[DataSourceFailed] {self.source}:{self.message}")

    def dict_form_log(self):
        return {"source": self.source, "message": self.message}


class InvalidSymbol(Exception):
    """
    Virheiden käsittely luokka, jota käytetään jos osakesymbolien kanssa tulee ongelmia
    """

    def __init__(self, symbol, message: str = None):
        self.symbol = symbol
        self.message = message
        super().__init__(self.message)

    def log_error(self):
        print(f"[InvalidSymbol] {self.symbol}:{self.message}")

    def dict_form_log(self):
        return {"symbol": self.symbol, "message": self.message}


class BaseStockClass(ABC):
    """
    Pakollinen perusrakenne luokka,
    jota käytetään perustus luokkana ja pohjana osake datan noutamis luokkaa varten
    """

    @abstractmethod
    def get_current_data(self, symbol: str, ) -> Optional[StockData]:

        raise NotImplementedError("subclasses must implement get_current_data")

    @abstractmethod
    def get_historical_data(self, symbol: str, period: str = "1mo",
                            interval: str = "1d") -> pd.DataFrame:
        raise NotImplementedError(
            "subclasses must implement get_historical_data")

    @abstractmethod
    def get_multiple_current_data(self, symbols: List[str]) -> Dict[str, Optional[StockData]]:
        raise NotImplementedError(
            "Subclasses must implement get_multiple_current_data")


class StockRepository(BaseStockClass):
    """
    Hoitaa datan hakemista yfinance kirjaston avulla, ja varastoi sitä välimuistiin tai/ja
    tietokantaan
    """

    def __init__(self, db_path="stocks.db", cache_enabled: bool = True):
        self.logger = logging.getLogger(__name__)
        self.cache_enabled = cache_enabled

        self.redis_client = None

        if cache_enabled:
            try:
                self.redis_client = Redis(
                    host='localhost', port=6379, decode_responses=True)
                self.redis_client.ping()
            except (ValueError, RedisError) as e:
                self.logger.warning(
                    "Redis unavailable, lets use SQL lite instead. Error: %s",
                    e)
                self.redis_client = None

        self.db_path = db_path
        self.init_database()

    def init_database(self):
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute(
                    """CREATE TABLE IF NOT EXISTS Stock_hist
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT NOT NULL,
                high REAL NOT NULL,
                low  REAL NOT NULL,
                close REAL NOT NULL,
                open_price REAL NOT NULL,
                volume INT NOT NULL,
                timestamp DATETIME NOT NULL 
                )
                """)
                connection.execute(
                    "CREATE INDEX IF NOT EXISTS idx_symbol_timestamp"
                    " ON Stock_hist(symbol, timestamp)")
        except sqlite3.Error as e:
            self.logger.warning(
                "Error creating the db table: %s", e)
            raise SpotStockDataError(
                "Database initialization failed", e) from e

    def cache_key(self, symbol: str, data_type: str) -> str:
        return f"stock:{symbol}:{data_type}"

    def _get_from_cache(self, key: str) -> Optional[str]:
        if not self.cache_enabled or self.redis_client is None:
            return None
        try:
            return self.redis_client.get(key)
        except RedisError as e:
            self.logger.warning("Failed to read cache: %s", e)
            return None

    def set_to_cache(self, key: str, data: str, expire_seconds=300) -> None:
        if not self.cache_enabled or self.redis_client is None:
            return
        try:
            self.redis_client.setex(key, expire_seconds, data)
        except RedisError as e:
            self.logger.warning("failed to set the data to cache: %s", e)

    def get_current_data(self, symbol: str) -> Optional[StockData]:
        if not symbol or not isinstance(symbol, str):
            raise InvalidSymbol("invalid symbol or not symbol at all")

        cached_data = self._get_cached_current_data(symbol)
        if cached_data:
            return cached_data

        return self._fetch_and_cache_current_data(symbol)

    def _get_cached_current_data(self, symbol: str) -> Optional[StockData]:
        cache_key = self.cache_key(symbol, "current")
        cached_data = self._get_from_cache(cache_key)
        if not cached_data:
            return None

        try:
            cache_dict = json.loads(cached_data)
            cache_dict["timestamp"] = datetime.fromisoformat(
                cache_dict["timestamp"])
            return StockData(**cache_dict)
        except Exception as e:
            raise SpotStockDataError(
                symbol, f"error getting stock data from cache: {e}") from e

    def _fetch_and_cache_current_data(self, symbol: str) -> Optional[StockData]:
        try:
            ticker = yf.Ticker(symbol)
            time_frame = ticker.history(period="1d", interval="1m")
            if time_frame.empty:
                self.logger.warning(
                    "No stock data available for symbol: %s", symbol)
                return None
            stock_data = DataFactory.create_stock_data_from_yf(
                symbol, time_frame)
            self._cache_current_data(symbol, stock_data)
            return stock_data

        except json.JSONDecodeError as e:
            self.logger.warning(
                "The operation to get current data failed for %s: %s",
                symbol, e
            )
            raise DataSourceFailed(f"Error with the data source: {e}") from e

    def _cache_current_data(self, symbol: str, stock_data: StockData) -> None:
        cache_key = self.cache_key(symbol, "current")
        try:
            self.set_to_cache(cache_key, stock_data.to_dict())
        except (ValueError, RedisError) as e:
            self.logger.warning(
                "Failed to set cache data for %s: %s", symbol, e)

    def get_historical_data(
            self,
            symbol: str,
            period: str = "1mo",
            interval: str = "1d"
    ) -> pd.DataFrame:
        """

        Args:
        symbol: osakkeen symboolinen nimi esim. AAPL (Apple) tai GOOGL (Google)
       
        period:Kuinka pitkältä jaksolta, verrattuna nykyhetkeen, haetaan historiallista dataa 
        
        interval: Minkä aika yksiköiden välein kerätään historiallista dataa
          kyseiseltä jaksolta
        
        return: palauttaa pandas DataFramen, jossa osakkeesta tietoja period ajan takaa ja
        interval aikavälien välein. 
        """

        try:
            ticker = yf.Ticker(symbol)
            time_frame = ticker.history(period=period, interval=interval)
            if time_frame.empty:
                self.logger.warning(
                    "No historical stock data available for symbol: %s", symbol)
                return pd.DataFrame()
            return time_frame

        except json.JSONDecodeError as e:
            self.logger.warning(
                "failed to fetch historical data for %s: %s", symbol, e)
            raise DataSourceFailed(
                f"Perhaps no data source for this symbol {symbol}: {e}"
            ) from e

    def get_multiple_current_data(self, symbols: List[str],) -> Dict[str, Optional[StockData]]:
        """
       
        Args:
        symbols: Lista symboleita, osakenimi muodossa ["AAPL", "GOOGL"]
        
        return: palauttaa kirjaston, jossa osakkeen nimet avaimina, ja StockData olio arvona
        
        """
        results = {}

        for symbol in symbols:
            try:
                results[symbol] = self.get_current_data(symbol)
            except (InvalidSymbol, DataSourceFailed) as e:
                self.logger.error("failed to fetch data: %s", e)
                results[symbol] = None

        return results

    def store_historical_data(self, stock_data: StockData) -> None:
        try:
            with sqlite3.connect(self.db_path) as connection:
                connection.execute(
                    """INSERT INTO Stock_hist (symbol, timestamp,
                        high, low,close,open_price,
                        volume)
                        VALUES (?,?,?,?,?,?,?)  """, (
                        stock_data.symbol,
                        stock_data.timestamp,
                        stock_data.high,
                        stock_data.low,
                        stock_data.close,
                        stock_data.open_price,
                        stock_data.volume
                    ))
        except sqlite3.Error as e:
            self.logger.warning(
                "Failed to save stock data into the Stock_hist table: %s", e)

    def get_historical_timeframe_data(self, symbol: str, start_date: str, end_date: str, interval):
        """
        Samantyylinen kuin get_historical_data metodi, mutta osaa hakea dataa
        määriteltyn aloitus päivän ja lopetus päivän väliltä.
        Sen sijasta, että rinnastaisi nykyhetkestä

        Args:
        symbol: osakkeen symboolinen nimi esim. AAPL (Apple) tai GOOGL (Google)
       
        start_date: aloitus päivämäärä

        end_data: lopetus päivämäärä 
        
        interval: Minkä aika yksiköiden välein kerätään historiallista dataa
          kyseiseltä jaksolta
        
        return: palauttaa pandas DataFramen, jossa osakkeesta tietoja
          aloituksen ja lopetuksen väliltä, 
        interval aikavälien välein. 

        """
        try:
            ticker = yf.Ticker(symbol)
            time_frame = ticker.history(
                start=start_date, end=end_date, interval=interval)
            if time_frame.empty:
                self.logger.warning(
                    "No historical stock data available for symbol: %s", symbol)
                return pd.DataFrame()
            return time_frame
        except json.JSONDecodeError as e:
            self.logger.warning(
                "failed to fetch historical data for %s: %s", symbol, e)
            raise DataSourceFailed(
                f"Perhaps no data source for this symbol {symbol}: {e}"
            ) from e
