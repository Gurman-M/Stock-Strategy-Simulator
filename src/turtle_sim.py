#!/usr/bin/env python

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calculate_atr(data, period):
    # calculate TR for each day using necessary price values
    data['Previous Close'] = data['Close'].shift(1)
    data['High-Low'] = data['High'] - data['Low']
    data['High-PrevClose'] = abs(data['High'] - data['Previous Close'])
    data['Low-PrevClose'] = abs(data['Low'] - data['Previous Close'])

    # axis=1 ensures that one value is taken from each column to find max, axis=0 finds max of each column's values
    data['TR'] = data[['High-Low', 'High-PrevClose', 'Low-PrevClose']].max(axis=1)

    # calculate ATR using a rolling window of 14 days
    data['ATR'] = data['TR'].rolling(window=period).mean()
    
    return data

# Function to simulate Turtle Trading
def turtle_trading_simulation(ticker, start_date, end_date, initial_balance, risk_percent, high_days, loss_days):
    # Fetch historical data
    data = yf.download(ticker, start=start_date, end=end_date)
    
    data = calculate_atr(data, 14)
    
    max_gain = -9999999
    drawdown = 9999999
    prev_balance = 0
    
    # Calculate necessary indicators
    # Finds highest and lowest prices for last x number of days for each "day" in the data
    # If the highest price returned on a certain day is equal to current day's high, then buy
    # Else if the lowest price return on a day is equal to current day's low, sell
    data['High_20'] = data['High'].rolling(window=high_days).max()
    data['Low_10'] = data['Low'].rolling(window=loss_days).min()
    
    # Initialize variables
    balance = initial_balance
    position_size = 0 # of shares
    in_position = False # whether we current own shares
    trade_log = [] # all trades we have made
    buy_date = ""
    sell_date = ""
    last_balance = 0

    for i in range(len(data)):
        if data['High_20'].iloc[i] > 0:  # Ensure there's a valid 20-day high
            if buy_date == "":
                buy_date = str(data.index[i].tz_localize(None))[0:10]
            # Entry signal
            if data['Close'].iloc[i] > data['High_20'].iloc[i-1] and not in_position:
                prev_balance = balance
                position_size = (balance * risk_percent) // data['ATR'].iloc[i]  # Calculate position size
                balance -= position_size * data['Close'].iloc[i]  # Deduct from balance
                trade_log.append(('BUY', data.index[i], data['Close'].iloc[i], balance))
                in_position = True

            # Exit signal
            elif in_position and data['Close'].iloc[i] < data['Low_10'].iloc[i-1]:
                balance += position_size * data['Close'].iloc[i]  # Add to balance
                max_gain = max(max_gain, ((balance - prev_balance)/prev_balance) * 100)
                drawdown = min(drawdown, ((balance - prev_balance)/prev_balance) * 100)
                trade_log.append(('SELL', data.index[i], data['Close'].iloc[i], balance))
                in_position = False
                sell_date = str(data.index[i].tz_localize(None))[0:10]
                last_balance = balance

    # Create a DataFrame for trade logs
    trade_df = pd.DataFrame(trade_log, columns=['Action', 'Date', 'Price', 'Balance'])

    
    # Plotting account balance over trades
    # plt.figure(figsize=(12, 6))
    # plt.plot(trade_df['Date'], trade_df['Balance'], marker='o')
    # plt.title(f'Account Balance Over Trades for {ticker}')
    # plt.xlabel('Date')
    # plt.ylabel('Account Balance ($)')
    # plt.grid()
    # plt.xticks(rotation=45)
    # plt.tight_layout()
    # plt.show()

    total_return = format(((prev_balance - initial_balance)/initial_balance) * 100, ".2f")
    trade_df['Balance'] = trade_df['Balance'].apply(lambda x: f"{x:.2f}")
    trade_df['Price'] = trade_df['Price'].apply(lambda x: f"{x:.2f}")
    print(trade_df)
    annualized_return = 0
    html_table = trade_df.to_html(index=True)
    
    if int(end_date[0:4]) - int(buy_date[0:4]) > 0:
        annualized_return = format((pow((prev_balance/initial_balance), 1/(int(end_date[0:4]) - int(buy_date[0:4]))) - 1) * 100, ".2f")
    
    return html_table, initial_balance, format(last_balance, ".2f"), format(max_gain, ".2f"), format(drawdown, ".2f"), total_return, annualized_return, buy_date, sell_date

# Run the simulation
# trade_results = turtle_trading_simulation('AAPL', '2020-01-01', '2023-01-01', 10000, 0.02, 20, 10)

# Display the trade log
# print(trade_results)
