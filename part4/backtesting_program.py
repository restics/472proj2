
#################################### Initialization - DONE ####################################
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import warnings

warnings.filterwarnings("ignore")
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



# adding path to part3\brokerbot.py to system path
sys.path.insert(1, "..\\part3")

from brokerbot import SentimentDecision # as Module

part3_path = "..\\part3\\out\\"
historical_data = pd.read_csv(part3_path + "combined_sentiment_results.csv", parse_dates=True)
historical_data = historical_data.drop(columns=['Unnamed: 0'])

historical_data = historical_data[(np.abs(stats.zscore(historical_data[['change']])) < 3).all(axis=1)] #remove outliers

decision_module = SentimentDecision( buy_threshold=upp_threshold, sell_threshold=low_threshold)
decision_module.train_model(historical_data)

# only keep dates for when we have sentiment scores

# prepare for merge
historical_data = historical_data.reset_index()

X = historical_data[['change']]
y = historical_data['daily_sentiment_score']

plt.plot(X, y, 'o')
prices = prices.reset_index()


# make them both datetime objects
historical_data['date'] = pd.to_datetime(historical_data['date'])
prices['date'] = pd.to_datetime(prices['date'])

columns = prices.columns
prices = prices.merge(historical_data, on='date', how='left').dropna(subset=['daily_sentiment_score'])
prices = prices[columns]
prices = prices.set_index('date')

# import backtesting framework via backtesting.py
import backtrader as bt
import numpy as np

class SentimentStrategy(bt.Strategy):
    def __init__(self):
        self.sma = bt.indicators.SimpleMovingAverage(self.data.close, period=20)

    def next(self):
        # check for the padded NaN vals
        if np.isnan(self.sma[-1]):
            return # skipping
            
        # trading logik
        date = self.data.datetime.datetime().date()
        if date in historical_data['date'].dt.date.values:
            decision = decision_module.make_decision(date,
                                                     historical_data.loc[historical_data['date'].dt.date == date, 'daily_sentiment_score'].values[0],
                                                     historical_data.loc[historical_data['date'].dt.date == date, 'change'].values[0])
            if decision == 'BUY':
                self.buy()
            elif decision == 'SELL':
                self.sell()
            else:
                pass
        else:
            print(f"Date {date} not found in historical data.")
            return  # Skip this iteration

        
        """
        if self.sma[-1] < self.data.Close[-1]:
            self.buy()
        elif self.sma[-1] > self.data.Close[-1]:
            self.sell()
        """


print("*Initialization done*")

#################################### Backtesting -  ####################################

# runing with Cerebro
cerebro = bt.Cerebro()
cerebro.addstrategy(SentimentStrategy)

# Load data 
data = bt.feeds.PandasData(dataname=prices)
cerebro.adddata(data)
cerebro.broker.setcash(cash_entered)
cerebro.broker.setcommission(commission=0.002)

starting_value = cerebro.broker.getvalue()
print('Starting Portfolio Value: %.2f' % starting_value)
cerebro.run()
final_value = cerebro.broker.getvalue()
print('Final Portfolio Value: %.2f' % final_value)

# Print statistics:
# Calculate ROI (Return on Investment)
roi = (final_value - starting_value) / starting_value * 100
print(f"Return on Investment (ROI): {roi:.2f}%")

# Performance metrics using Backtrader's built-in analyzer


# Add analyzers to cerebro
cerebro.addanalyzer(bt.analyzers.SharpeRatio)
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addanalyzer(bt.analyzers.TradeAnalyzer)

# Run the backtest again with analyzers
result = cerebro.run()

# Extract the Sharpe ratio and maximum drawdown
sharpe = result[0].analyzers.sharperatio.get_analysis()
max_drawdown = result[0].analyzers.drawdown.get_analysis()

print(f"Sharpe Ratio: {sharpe['sharperatio']:.2f}")
print(f"Maximum Drawdown: {max_drawdown['max']['drawdown']:.2f}%")

# Win/Loss Ratio (count wins and losses)
trade_stats = result[0].analyzers.tradeanalyzer.get_analysis()
total_trades = trade_stats.get('total', {}).get('total', 0)
wins = trade_stats.get('won', {}).get('total', 0)
losses = trade_stats.get('lost', {}).get('total', 0)

win_loss_ratio = wins / losses if losses > 0 else float('inf')
print(f"Win/Loss Ratio: {win_loss_ratio:.2f}")

# Plot results
cerebro.plot()
print("*Backtesting done*")

X = decision_module.get_trade_log()["date"]
y = decision_module.get_trade_log()["predicted_price_change"]

plt.plot(X, y, 'o')
plt.show()

# Drafts & dumps
