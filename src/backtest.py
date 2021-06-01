from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import os
import pandas as pd
crypto_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'crypto'))
stock_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'stockprice'))
forex_json_path = os.path.abspath(os.path.join(
    (__file__), '..', '..', 'json', 'forex'))
btcusd_df = pd.read_json(os.path.join(crypto_json_path, 'ethusd_30Min'))
stock_df = pd.read_json(os.path.join(stock_json_path, 'GME_daily'))
forex_df = pd.read_json(os.path.join(forex_json_path, 'USDJPY_60min'))
'''
you can import any library 
'''


class SmaCross(Strategy):
    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, 2)
        self.ma2 = self.I(SMA, price, 4)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()


'''
more data is required
'''
bt = Backtest(btcusd_df, SmaCross, cash=100000000, commission=.002,
              exclusive_orders=True)
stats = bt.run()
bt.plot()

'''
toy example
'''
bt = Backtest(GOOG, SmaCross, commission=.002,
              exclusive_orders=True)
stats = bt.run()
bt.plot()
