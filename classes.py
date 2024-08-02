
import time
import random
import datetime
from typing import Optional, Union
class SystemConfig:
    def __init__(self):
        self.main_loop_continue = True
        self.start_time = time.time()


    def freeze(self):
        self.end_time = time.time()
        self.uptime = self.end_time - self.start_time

class Position:
    def __init__(self, share_count: float, share_value: float, is_sell: bool = False, position_start: datetime.datetime = datetime.datetime.now()):
        self.id = str(random.getrandbits(128))
        self.value = share_count * share_value
        self.number_of_shares = share_count
        self.share_price = share_value
        self.position_start = position_start
        self.is_sell = is_sell



class Ticker:
    def __init__(self, ticker_name: str, description: Optional[str] = None):
        self.name = ticker_name
        self.description = description
        self.positions: dict[str, Position] = {}
        # Start values.
        self.position_count = 0
        self.total_shares = 0.0
        self.total_value = 0.0
        self.sell_count = 0
        self.avg_price = 0.0


    def add_position(self, new_position: Position):
        self.positions[new_position.id] = new_position
        self.total_shares += new_position.number_of_shares
        self.total_value += new_position.value
        self.position_count += 1
        self.avg_price = (self.avg_price + new_position.share_price) / 2

    def get_position(self, position_id: str) -> Position:
        return self.positions.get(position_id, None)


    def remove_position(self, position_id: str) -> bool:
        # inverse of add_position(). not selling

        # Read position so we can strip the info.
        departing_position = self.get_position(position_id)
        self.position_count -= 1
        self.total_shares -= departing_position.number_of_shares
        self.total_value -= departing_position.value 
        self.avg_price = (self.avg_price * 2) - departing_position.share_price

        self.positions.pop(position_id)

        return True

    def sell_position(self, sell_position: Position) -> bool:
        self.sell_count += 1
        self.total_shares -= sell_position.number_of_shares
        self.total_value -= sell_position.value
        self.avg_price = (self.avg_price * 2) - sell_position.share_price

        self.positions[sell_position.id] = sell_position

        return True

class Portfolio:
    def __init__(self):
        self.tickers: dict[str, Ticker] = []

    def buy_position(self, ticker_name: str, position: Position, description: Optional[str] = None):
        self.add_ticker(ticker_name)

        this_ticker = self.get_ticker(ticker_name)
        this_ticker.add_position(new_position=position)

    def sell_position(self, ticker_name: str, position: Position):
        this_ticker = self.get_ticker(ticker_name)
        this_ticker.sell_position(sell_position=position)

    def add_ticker(self, ticker_name: str, description: Optional[str]) -> bool:
        ticker_uppercase = ticker_name.upper()

        if not self.get_ticker(ticker_name):
            self.tickers[ticker_name] = Ticker(ticker_name=ticker_uppercase, description=description)
            return True

        return False


    def get_ticker(self, ticker_name: str) -> Optional[Ticker]:
        ticker_uppercase = ticker_name.upper()

        return self.tickers.get(ticker_uppercase, None)
    

