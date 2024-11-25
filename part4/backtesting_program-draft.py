
#################################### Initialization - DONE ####################################
import os
import sys
import pandas as pd

# loop for threshold prompt
while True:
    # obtainign thresholds from user
    upp_threshold = int(input("Please enter the upper threshold for the desired sentiment range (-100 <= lower_threshold <= upper_threshold <= 100): "))
    low_threshold = int(input("Please enter the lower threshold for the desired sentiment range (-100 <= lower_threshold <= upper_threshold <= 100): "))

    # check thresholds
    if -100 <= low_threshold and low_threshold <= upp_threshold and upp_threshold <= 100:
        break
    else:
        print(f"\nInvalid thresholds, please try again\n")
    
#print(upp_threshold, low_threshold)

# loop for threshold prompt
while True:
    # input cash for backtesting
    cash_entered = int(input("Please enter the amount of cash in USD for the backtest: $"))

    # check amt
    if cash_entered > 0:
        break
    else:
        print(f"\nInvalid cash entered, must be more than $0, please try again\n")
        

#print(cash_entered)

# import dataset conceerning NVDA
part1_path = "..\\part1\\"

# read csv, set date col to datetime and set it to index
prices = pd.read_csv(part1_path + "year_daily_NVDA_prices.csv", index_col='date', parse_dates=True)

#print(prices.columns)

# reset columns to 'Open', 'High', 'Low', 'Close', and (optionally) 'Volume' if lower case
if (prices.columns == ['symbol', 'open', 'high', 'low', 'close', 'volume']).all():
    prices.rename(columns={'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'}, inplace=True)

#print(prices)

# adding path to part3\brokerbot.py to system path
sys.path.insert(1, "..\\part3")

from brokerbot import SentimentDecision # as Module

part3_path = "..\\part3\\out\\"
historical_data = pd.read_csv(part3_path + "combined_sentiment_results.csv")
historical_data = historical_data.drop(columns=['Unnamed: 0'])

decision_module = SentimentDecision()
decision_module.train_model(historical_data)


# import backtesting framework via backtesting.py
import tulipy
import numpy as np
from backtesting import Backtest, Strategy
from backtesting.lib import crossover

class SentimentStrategy(Strategy):
    def init(self):
        close_prices = self.data.Close
        # initializing pre-defined indicators with padding
        sma = tulipy.sma(close_prices, period=20)
        padding = np.full(len(close_prices) - len(sma), np.nan)
        padded_sma = np.concatenate((padding, sma))
        
        self.sma = self.I(lambda: padded_sma)

    def next(self):
        # check for the padded NaN vals
        if np.isnan(self.sma[-1]):
            return # skipping
            
        # trading logik
        
        
        """
        if self.sma[-1] < self.data.Close[-1]:
            self.buy()
        elif self.sma[-1] > self.data.Close[-1]:
            self.sell()
        """


print("*Initialization done*")

#################################### Backtesting -  ####################################

# run with Backtest
bt = Backtest(prices, SentimentStrategy, cash=cash_entered, commission=.002)
stats = bt.run()
#bt.plot()


print("*Backtesting done*")

# Drafts & dumps
