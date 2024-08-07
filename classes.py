import time
import os
import datetime
from enum import Enum
from typing import Optional


class Command(Enum):
    BUY = "buy"
    SELL = "sell"
    QUIT = "quit"
    JOEY = "JOEY"


# (Command, command_arguments)
CommandArgs = list[str]
ParsedCommand = tuple[Command, list[str]]


class SystemConfig:
    """
    Singleton class representing the system settings for a given
    execution of the CLIP program. Used for basic function keeping.

    Attributes:
        main_loop_continue: Bool indicating whether main execution loop
            should be allowed to continue.
        start_time: time.time object represent program initialisation.
    """

    def __init__(self):
        """
        Initialise a new CLIP instance.
        """
        self.main_loop_continue = True
        self.start_time = time.time()

    def freeze(self):
        """
        On 'shutdown' of CLIP, count execution as over and note uptime.
        """
        self.end_time = time.time()
        self.uptime = self.end_time - self.start_time


class Position:
    """Class representing a position, bought or sold.

    Each position is uniquely identified, and serves as a record of transaction,
    either purcahsing a stock, or selling a stock. This is the atomic
    unit used by CLIP.

    Attributes:
        id: Hexadecimal unique identifier string representing this position.
        value: Floating point dollar value of this position.
        number_of_shares: Floating point number of shares purchased/sold for this position.
        share_price: Floating point dollar value of each individual share.
        position_start: Datetime representing when this position was sold/bought.
        is_sell: Boolean value denoting this as a sell position or not.
    """

    def __init__(
        self,
        share_count: float,
        share_value: float,
        is_sell: bool = False,
        position_start: datetime.datetime = datetime.datetime.now(),
    ):
        """
        Generate a new position record.

        Arguments:
            share_count: Number of shares sold/bought.
            share_value: Floating point value of each share.
            is_sell: Optional bool indicating whether this was a sell or not. Defaults False.
            position_start: Optional datetime of the sell/buy. Default is datetime.now().
        """
        self.id = str(os.urandom(5).hex()).upper()

        self.value = share_count * share_value
        self.number_of_shares = share_count
        self.share_price = share_value
        self.position_start = position_start
        self.is_sell = is_sell

    def __str__(self):
        return (
            f"{'Sell ' if self.is_sell else ''}Position {self.id}\n"
            f" - Total position value: ${self.value}\n"
            f" - ({self.number_of_shares} shares at ${self.share_price} per share)\n"
            f" - Created at: {self.position_start}\n"
        )

    def __repr__(self):
        return (
            f"{'Sell ' if self.is_sell else ''}Position: {self.id} -> {self.number_of_shares}"
            f" x ${self.share_price:.2f} = ${self.value:.2f}. "
        )


class Ticker:
    """Class representing a given ticker identity.

    A Ticker is the 3/4 letter identifier of a stock, index, or other group of Positions.
    This class keeps track of the positions open and closed for a given ticker, as well
    as some basic information about the positions.

    Attributes:
        name: String name of the ticker.

    """

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
        self.avg_price = (
            (self.avg_price + new_position.share_price) / 2
            if self.position_count > 1
            else new_position.share_price
        )

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

        self.avg_price = self.total_value / self.total_shares

        self.positions[sell_position.id] = sell_position

        return True

    def __str__(self):
        return (
            f"Ticker: {self.name}\n" f"{self.description}" + "\n"
            if self.description
            else f"Ticker: {self.name}\n"
            f" - Number of positions held: {self.position_count}\n"
            f" - (Number of sold positions: {self.sell_count})\n"
            f" - Total value: ${self.total_value:.2f}\n"
            f" - Average price: ${self.avg_price:.2f}\n"
        )

    def __repr__(self):
        return f"Ticker {self.name} -> {self.position_count} - {self.sell_count} @ ${self.avg_price:.2f}avg = ${self.total_value}"


class Portfolio:
    def __init__(self, name: str):
        self.name = name
        self.tickers: dict[str, Ticker] = {}
        self.ticker_count = 0

    def buy_position(self, ticker_name: str, position: Position, description: Optional[str] = None):
        self.add_ticker(ticker_name)

        this_ticker = self.get_ticker(ticker_name)
        this_ticker.add_position(new_position=position)

    def sell_position(self, ticker_name: str, position: Position):
        this_ticker = self.get_ticker(ticker_name)
        this_ticker.sell_position(sell_position=position)

    def add_ticker(self, ticker_name: str, description: Optional[str] = None) -> bool:
        ticker_uppercase = ticker_name.upper()

        if not self.get_ticker(ticker_uppercase):
            self.ticker_count += 1
            self.tickers[ticker_uppercase] = Ticker(ticker_name=ticker_uppercase, description=description)
            return True

        return False

    def get_ticker(self, ticker_name: str) -> Optional[Ticker]:
        ticker_uppercase = ticker_name.upper()

        return self.tickers.get(ticker_uppercase, None)

    def __str__(self):
        return f"Portfolio: {self.name}" f" - {self.ticker_count} tickers tracked."

    def __repr__(self):
        return f"Portfolio {self.name}, {self.ticker_count} tickers."
