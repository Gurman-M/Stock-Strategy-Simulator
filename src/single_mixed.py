'''
This page should be about index investing + bonds and should have different styles:

Single stock: invest in pure SPY/VOO or just bonds like VBTLX. Also have option to invest in one company, but advise them that it may be risky.
    - have checkboxes for reinvesting dividends to improve gains
Mix: Show performance for having index + bonds (keep a 50/50 split using couch potato formula)
    - also have option to allocate specific percentage of bonds and stocks, write that age - 10 or age - 20 is a recommended allocation
'''

from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf
import math
import pandas as pd

'''
Calculates returns for a single stock over a max period
 @params
    investment: the initial cash investment
    stock: the ticker of the company
    bond: bool indicating if the ticker is a bond stock
    reinvest: bool indicating if dividends should be reinvested
'''

def single_stock(start_date, end_date, investment, stock, monthly):
    curr_month = -1
    cash = investment
    total_shares = 0
    last_price = 0
    counter = 0
    start_price = 0
    total_contribution = investment
    buy_date = ""
    sell_date = ""

    df = yf.download(stock, start=start_date, end=end_date)

    for index, row in df.iterrows():
        if (index.month != curr_month):
            cash += monthly
            curr_month = index.month
            total_contribution += monthly

        if (counter == 0):
            start_price = row["Adj Close"]
            buy_date = str(index.tz_localize(None))[0:10]

        if cash > row["Adj Close"]:
            shares = (cash // row["Adj Close"])
            cash -= shares * row["Adj Close"]
            total_shares += shares
            
        last_price = row["Adj Close"]
        counter += 1
        sell_date = str(index.tz_localize(None))[0:10]

    return summarize_data(start_date, end_date, investment, start_price, last_price, total_shares, cash, total_contribution, monthly, buy_date, sell_date)


'''
Prints applicable data using the values calculated from stock simulation
@params
    start_date: starting date of stock simulation
    end_date: ending date of stock simulation
    investment: total starting capital
    start_price: start price of stock
    last_price: last price of stock (before sell)
    total_shares: the total number of shares held
    dividend_gains: total amount of cash gained from dividends
    cash: total cash left after buying as many shares as possible
    total_contribution: how much cash was contributed by the investor
'''

def summarize_data(start_date, end_date, investment, start_price, last_price, total_shares, cash, total_contribution, monthly, buy_date, sell_date):
    total_return = format((((total_shares * last_price) + cash - total_contribution)/total_contribution) * 100, ".2f")
    annualized_return = 0
    if (int(sell_date[0:4]) - int(buy_date[0:4])) > 0:
        annualized_return = format((pow((((total_shares * last_price) + cash)/total_contribution), 1/(int(sell_date[0:4]) - int(buy_date[0:4]))) - 1) * 100, ".2f")
    
    return format(start_price, ".2f"), format(last_price, ".2f"), total_shares, total_contribution, format((total_shares * last_price) + cash, ".2f"), total_return, annualized_return, buy_date, sell_date

'''
Prints applicable data using the values calculated from mixed investment stock simulation
@params
    start_date: starting date of stock simulation
    end_date: ending date of stock simulation
    investment: total starting capital
    stock_one, stock_two: name of each stock
    start_price_one, start_price_two: start price of each stock
    last_price_one, last_price_two: last price of each stock (before sell)
    total_shares_one, total_shares_two: the total number of shares held in each stock
    cash: total cash left after buying as many shares as possible
    total_contribution: how much cash was contributed by the investor
'''

def summarize_data_mixed(start_date, end_date, investment, stock_one, stock_two, start_price_one, start_price_two, last_price_one, last_price_two, total_shares_one, total_shares_two, cash, total_contribution, monthly, buy_date_one, sell_date_one, buy_date_two, sell_date_two):
    print("Buy Period:", start_date, end_date)
    print("Initial Investment:", investment)
    print(f"Start/End Price For {stock_one}:", format(start_price_one, ".2f"), format(last_price_one, ".2f"))
    print(f"Start/End Price For {stock_two}:", format(start_price_two, ".2f"), format(last_price_two, ".2f"))
    print(f"Total Shares For {stock_one}:", total_shares_one)
    print(f"Total Shares For {stock_two}:", total_shares_two)
    print(f"Cash From {stock_one} Shares:", format((total_shares_one * last_price_one), ".2f"))
    print(f"Cash From {stock_two} Shares:", format((total_shares_two * last_price_two), ".2f"))
    print("Total Cash After Selling All Shares:", format(((total_shares_one * last_price_one) + cash + (total_shares_two * last_price_two)), ".2f"))
    print("Total Return (Percentage): ", format(((((total_shares_one * last_price_one) + cash + (total_shares_two * last_price_two)))/total_contribution) * 100, ".2f"), "%", sep='')
    
    total_return = format(((((total_shares_one * last_price_one) + cash + (total_shares_two * last_price_two)))/total_contribution) * 100, ".2f")
    total_value = (total_shares_one * last_price_one) + (total_shares_two * last_price_two) + cash
    annualized_return = 0
    years = max(int(sell_date_one[0:4]) - int(buy_date_one[0:4]), int(sell_date_two[0:4]) - int(buy_date_two[0:4]))
    if years > 0:
        annualized_return = format((pow((total_value/total_contribution), 1/years) - 1) * 100, ".2f")
    
    return format(start_price_one, ".2f"), format(last_price_one, ".2f"), format(start_price_two, ".2f"), format(last_price_two, ".2f"), total_shares_one, total_shares_two, total_contribution, format(total_value, ".2f"), total_return, annualized_return, buy_date_one, sell_date_one, buy_date_two, sell_date_two


'''
Calculates returns from investing in two different stocks with some allocation percentage
@params
    investment: starting investment
    stock_one: first stock to invest
    stock_two: second stock to invest
    reinvest: bool for whether dividends are reinvested or not
    allocation: what percentage of invested funds are placed into stock_one, rest is placed into stock_two
'''
def mixed_invest(start_date, end_date, investment, stock_one, stock_two, monthly, allocation):
    print(start_date, end_date, investment, stock_one, stock_two, monthly, allocation)
    print(type(start_date), type(end_date), type(investment), type(stock_one), type(stock_two), type(monthly), type(allocation))
    curr_month = -1
    curr_year = -1
    
    cash = investment
    shares_one = 0
    shares_two = 0
    start_price_one = 0
    start_price_two = 0
    last_price_one = 0
    last_price_two = 0
    total_contribution = investment
    buy_date_one = ""
    sell_date_one = ""
    buy_date_two = ""
    sell_date_two = ""
    counter = 0

    data_str = stock_one + " " + stock_two
    df = yf.download(data_str, start=start_date, end=end_date)

    # code for if we are not able to use the adj close
    
    # dividends_one = yf.Ticker(stock_one).dividends
    # dividends_two = yf.Ticker(stock_two).dividends

    # dividends_one.index = dividends_one.index.tz_localize(None)
    # dividends_two.index = dividends_two.index.tz_localize(None)

    # df[("Dividends", stock_one)] = 0.0
    # df[("Dividends", stock_two)] = 0.0

    # for index, row in df.iterrows():
    #    if index in dividends_one.index:
    #        df.at[index, ("Dividends", stock_one)] = dividends_one.at[index]
    #    
    #    if index in dividends_two.index:
    #        df.at[index, ("Dividends", stock_two)] = dividends_two.at[index]

    for index, row in df.iterrows():
        if (index.month != curr_month):
            cash += monthly
            curr_month = index.month
            total_contribution += monthly
            
            if (index.year != curr_year):
                if (math.isnan(row["Close"][stock_one])):
                    if (not math.isnan(row["Close"][stock_two])):
                        shares_one, shares_two, cash = adjust_allocation(shares_one, shares_two, row["Adj Close"][stock_one], row["Adj Close"][stock_two], cash, 0)
                else:
                    if (math.isnan(row["Close"][stock_two])):
                        shares_one, shares_two, cash = adjust_allocation(shares_one, shares_two, row["Adj Close"][stock_one], row["Adj Close"][stock_two], cash, 100)
                    else:
                        shares_one, shares_two, cash = adjust_allocation(shares_one, shares_two, row["Adj Close"][stock_one], row["Adj Close"][stock_two], cash, allocation)
                        
                curr_year = index.year

        if (start_price_one == 0 and not math.isnan(row["Adj Close"][stock_one])):
            start_price_one = row["Adj Close"][stock_one]
            buy_date_one = str(index.tz_localize(None))[0:10]
            
        if (start_price_two == 0 and not math.isnan(row["Adj Close"][stock_two])):
            start_price_two = row["Adj Close"][stock_two]
            buy_date_two = str(index.tz_localize(None))[0:10]
        
        if (not math.isnan(row["Adj Close"][stock_one])):
            last_price_one = row["Adj Close"][stock_one]
            sell_date_one = str(index.tz_localize(None))[0:10]
            
        if (not math.isnan(row["Adj Close"][stock_two])):
            last_price_two = row["Adj Close"][stock_two]
            sell_date_two = str(index.tz_localize(None))[0:10]

    # change original function to basically account for 2 stocks, but put 0 for all second stock values in single_stock
    return summarize_data_mixed(start_date, end_date, investment, stock_one, stock_two, start_price_one, start_price_two, last_price_one, last_price_two, shares_one, shares_two, cash, total_contribution, monthly, buy_date_one, sell_date_one, buy_date_two, sell_date_two)

def adjust_allocation(shares_one, shares_two, price_one, price_two, cash, allocation):
    if (allocation == 100):
        shares_one += cash // price_one
        cash -= shares_one * price_one
    elif (allocation == 0):
        shares_two += cash // price_two
        cash -= shares_two * price_two
    else:
        total_value = (shares_one * price_one) + (shares_two * price_two) + cash
        target_val_one = total_value * allocation
        target_val_two = total_value * (1 - allocation)

        required_funds_one = target_val_one - (shares_one * price_one)
        required_funds_two = target_val_two - (shares_two * price_two)
        
        if (required_funds_one < 0):
            # sell excess shares
            shares_to_sell = (-1 * required_funds_one) // price_one
            shares_one -= shares_to_sell
            cash += shares_to_sell * price_one
        
        if (required_funds_two < 0):
            # sell excess shares
            shares_to_sell = (-1 * required_funds_two) // price_two
            shares_two -= shares_to_sell
            cash += shares_to_sell * price_two
        
        if (required_funds_one > 0):
            # time to buy shares
            shares_needed = required_funds_one // price_one
            shares_needed_cost = shares_needed * price_one
            
            if cash >= shares_needed_cost:
                # we have enough cash to buy the shares needed for allocation
                shares_one += shares_needed
                cash -= shares_needed_cost
            else:
                # buy as many as cash lets you
                shares_bought = cash // price_one
                shares_one += shares_bought
                cash -= shares_bought * price_one
        
        if (required_funds_two > 0):
            # time to buy shares
            shares_needed = required_funds_two // price_two
            shares_needed_cost = shares_needed * price_two
            
            if cash >= shares_needed_cost:
                # we have enough cash to buy the shares needed for allocation
                shares_two += shares_needed
                cash -= shares_needed_cost
            else:
                # buy as many as cash lets you
                shares_bought = cash // price_two
                print("Bought shares two:", shares_bought)
                shares_two += shares_bought
                cash -= shares_bought * price_two
    
    return shares_one, shares_two, cash
    

# single_stock("2001-01-01", "2024-01-01", 1000, "SPY", 0, True)

# mixed_invest("2001-01-01", "2024-01-01", 1000, "SPY", "VBTLX", 0, 0.5)