import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

# the current dow 30 tickers
dow_tickers = [
        'AAPL', 'MSFT', 'JNJ', 'VZ', 'KO', 'PG', 'DIS', 'IBM', 'CSCO', 'XOM',
        'NKE', 'MRK', 'PFE', 'MCD', 'INTC', 'CRM', 'WMT', 'V', 'AMGN', 'TXN', 'CAT'
    ]

# get the Dogs of the Dow for a specific year
def get_dogs_of_dow(year, num_dogs):
    print(dow_tickers)
    
    # get historical data for the tickers
    data = yf.download(dow_tickers, start=f'{year}-01-01', end=f'{year}-12-31')['Adj Close']
    
    # creates dict of ticker data where each key is ticker and entry is the dividend dates and values
    dividends = {ticker: yf.Ticker(ticker).dividends for ticker in dow_tickers}
    
    # calculate the dividend yield for the last available price of the year
    # dividend yield is found by adding all dividends paid in the past year and divided it by the last price in the year
    yields = {}
    for ticker in dow_tickers:
        last_price = data[ticker].iloc[-1] # get the last adj price of the year for each ticker
        total_dividend = dividends[ticker][dividends[ticker].index.year == year].sum() # filters dividend values from column where date year must match given year and then finds sum
        dividend_yield = 0
        
        if last_price > 0:
            dividend_yield = total_dividend / last_price
            
        yields[ticker] = dividend_yield
    
    # create a DataFrame to sort and get the Dogs of the Dow
    yield_df = pd.DataFrame(list(yields.items()), columns=['Symbol', 'Dividend_Yield']) # creates a dataframe from list of tuples where one value is ticker and the other is dividend yield
    # gets the top 10 rows based on dividend yield value and then converts the associated symbols to list
    dogs_of_dow = yield_df.nlargest(num_dogs, 'Dividend_Yield')['Symbol'].tolist()
    dogs_ranked = yield_df.nlargest(len(dow_tickers), 'Dividend_Yield')['Symbol']
    print(dogs_ranked)
    
    return dogs_of_dow

def simulate_dogs_performance(start_year, end_year, initial_investment, yearly_deposit, num_dogs=10):
    yearly_returns = []
    performers = {}
    portfolio_balance = {}
    total_yearly_returns = {}
    total_contribution = initial_investment
    
    for year in range(start_year, end_year + 1):
        dogs = get_dogs_of_dow(year, num_dogs)
        
        # Download historical price data for the selected Dogs
        data = yf.download(dogs, start=f'{year}-01-01', end=f'{year}-12-31')['Adj Close']
        
        # Calculate investment per stock
        investment_per_stock = initial_investment / len(dogs)
        
        stock_value_held = {}
        
        for i in dogs:
            stock_value_held[i] = investment_per_stock
        
        
        # Calculate returns for the end of the year
        yearly_return = {}
        for stock in dogs:
            final_price = data[stock].iloc[-1]
            return_percentage = (final_price - data[stock].iloc[0]) / data[stock].iloc[0]
            yearly_return[stock] = return_percentage
            if stock not in performers:
                performers[stock] = []
            
            performers[stock].append(yearly_return[stock])
            
        total_yearly_returns[year] = (sum(yearly_return.values()) / len(yearly_return)) * 100
        
        for stock in yearly_return:
            return_value = stock_value_held[stock] * yearly_return[stock]
            stock_value_held[stock] += return_value

        # Calculate total portfolio return for the year
        total_yearly_return = sum(yearly_return.values()) / len(yearly_return)
        
        # Update the total value with the performance
        yearly_returns.append(total_yearly_return * 100)
        
        portfolio_balance[year] = sum(stock_value_held.values())
        
        initial_investment = sum(stock_value_held.values())
        initial_investment += yearly_deposit
        total_contribution += yearly_deposit
        
    
    return portfolio_balance, total_yearly_returns, performers, total_contribution

def test_simulation(start_year, end_year, initial_investment, yearly_deposit, num_dogs):
    # Define parameters for the test
    start_year = 2020
    end_year = 2023
    initial_investment = 10000  # Total investment amount
    yearly_deposit = 0        # Amount to deposit each year
    num_dogs = 10

    # Run the simulation
    results, yearly_returns, performers, total_contribution = simulate_dogs_performance(start_year, end_year, initial_investment, yearly_deposit, num_dogs)
    
    df = pd.DataFrame(list(results.items()), columns=['Year End', 'Portfolio Value']).set_index('Year End')
    df['Portfolio Value'] = df['Portfolio Value'].apply(lambda x: f"{x:.2f}")
    df["Return (%)"] = yearly_returns.values()
    
    # Calculate average returns for each ticker
    average_returns = {ticker: np.mean(returns) for ticker, returns in performers.items()}

    # Convert to a DataFrame and rank by average return
    avg_returns_df = pd.DataFrame(list(average_returns.items()), columns=['Ticker', 'Average Return (%)'])
    avg_returns_df['Rank'] = avg_returns_df['Average Return (%)'].rank(ascending=False)
    avg_returns_df['Rank'] = avg_returns_df['Rank'].astype(int)
    avg_returns_df.set_index('Rank', inplace=True) 
    avg_returns_df = avg_returns_df.sort_values(by='Rank')
    
    avg_returns_df['Average Return (%)'] = avg_returns_df['Average Return (%)'] * 100
    avg_returns_df['Average Return (%)'] = avg_returns_df['Average Return (%)'].apply(lambda x: f"{x:.2f}")

    total_return = format((sum(yearly_returns.values()) / len(yearly_returns)), ".2f")
    annualized_return = format((pow(float(df['Portfolio Value'].iloc[-1])/total_contribution, (1/len(yearly_returns))) - 1) * 100, ".2f")
    
    df['Return (%)'] = df['Return (%)'].apply(lambda x: f"{x:.2f}")
    
    df = df.reset_index()
    avg_returns_df = avg_returns_df.reset_index()
    
    # convert df and avg_returns_df to html table
    portfolio_table = df.to_html(index=False)
    performers_table = avg_returns_df.to_html(index=False)
    
    return portfolio_table, performers_table, total_return, annualized_return
    
def update_ticker(added_ticker, removed_ticker):
    if (added_ticker != ""):
        if added_ticker not in dow_tickers:
            dow_tickers.append(added_ticker)
    
    if (removed_ticker != ""):
        if removed_ticker in dow_tickers:
            dow_tickers.remove(removed_ticker)

def get_dow_tickers():
    return dow_tickers