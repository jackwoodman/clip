
import time
from typing import Optional
class SystemConfig:
    def __init__(self):
        self.main_loop_continue = True
        self.start_time = time.time()


    def freeze(self):
        self.end_time = time.time()
        self.uptime = self.end_time - self.start_time


class Portfolio:
    def __init__(self):
        self.positions = []


class Ticker:
    def __init__(self, ticker_name: str, descriptions: Optional[str] = None) 

class Position:
    def __init__(self, share_count: float, share_value: float):
        self.value = share_count * share_value
        self.number_of_shares = share_count
        self.value_per_share = share_value