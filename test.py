import yfinance as yf
import pandas as pd
import numpy as np

# The current Dow 30 tickers
dow_tickers = [
    'AAPL', 'MSFT', 'JNJ', 'VZ', 'KO', 'PG', 'DIS', 'IBM', 'CSCO', 'XOM',
    'NKE', 'MRK', 'PFE', 'MCD', 'INTC', 'CRM', 'WMT', 'V', 'AMGN', 'TXN', 'CAT'
]

# Get the Dogs of the Dow for a specific year
def get_dogs_of_dow(year, num_dogs):
    data = yf.download(dow_tickers, start=f'{year}-01-01', end=f'{year}-12-31')['Adj Close']
    dividends = {ticker: yf.Ticker(ticker).dividends for ticker in dow_tickers}
    
    yields = {}
    for ticker in dow_tickers:
        last_price = data[ticker].iloc[-1]
        total_dividend = dividends[ticker][dividends[ticker].index.year == year].sum()
        dividend_yield = total_dividend / last_price if last_price > 0 else 0
        yields[ticker] = dividend_yield
    
    yield_df = pd.DataFrame(list(yields.items()), columns=['Symbol', 'Dividend_Yield'])
    dogs_of_dow = yield_df.nlargest(num_dogs, 'Dividend_Yield')['Symbol'].tolist()
    
    return dogs_of_dow

def simulate_dogs_performance(start_year, end_year, initial_investment, yearly_deposit=0, cash=0, num_dogs=10):
    total_returns = {}
    performers = {}
    
    for year in range(start_year, end_year + 1):
        dogs = get_dogs_of_dow(year, num_dogs)
        
        # Download historical price data for the selected Dogs
        data = yf.download(dogs, start=f'{year}-01-01', end=f'{year}-12-31')['Adj Close']
        
        # Calculate investment per stock
        investment_per_stock = initial_investment / len(dogs) if dogs else 0
        
        # Track total shares and total value for the portfolio
        total_shares = {stock: 0 for stock in dogs}
        total_value = cash + initial_investment
        
        # Buy shares for each stock
        for stock in dogs:
            if data[stock].iloc[0] > 0:  # Ensure the initial price is valid
                shares_bought = investment_per_stock // data[stock].iloc[0]
                total_shares[stock] += shares_bought
                total_value += shares_bought * data[stock].iloc[0]
        
        # Calculate returns for the end of the year
        yearly_return = {}
        for stock in dogs:
            if data[stock].iloc[0] > 0:  # Ensure the initial price is valid
                final_price = data[stock].iloc[-1]
                return_percentage = (final_price - data[stock].iloc[0]) / data[stock].iloc[0]
                yearly_return[stock] = return_percentage
                if stock not in performers:
                    performers[stock] = []
                performers[stock].append(return_percentage)

        # Calculate total portfolio return based on individual stock performance
        if yearly_return:
            # Start with the current total value
            updated_total_value = total_value
            
            for stock in dogs:
                if stock in total_shares:
                    final_price = data[stock].iloc[-1]
                    shares = total_shares[stock]
                    # Calculate the value of the shares for the stock
                    updated_total_value += shares * (final_price - data[stock].iloc[0])
                    
            total_value = updated_total_value
            
        # Add yearly deposit for the next year
        total_value += yearly_deposit
        
        # Save the total value for the year
        total_returns[year] = total_value
    
    return total_returns, performers


def test_simulation():
    # Define parameters for the test
    start_year = 2020
    end_year = 2023
    initial_investment = 10000  # Total investment amount
    yearly_deposit = 0           # Amount to deposit each year
    cash = 0                     # Initial cash available
    num_dogs = 10

    # Run the simulation
    results, performers = simulate_dogs_performance(start_year, end_year, initial_investment, yearly_deposit, cash, num_dogs)

    # Print the results
    print("Simulation Results:")
    for year, total_value in results.items():
        print(f"Year: {year}, Total Portfolio Value: ${total_value:,.2f}")
    
    df = pd.DataFrame(list(results.items()), columns=['Year', 'Portfolio Value']).set_index('Year')
    df['Portfolio Value'] = df['Portfolio Value'].apply(lambda x: f"{x:.2f}")
    
    # Calculate average returns for each ticker
    average_returns = {ticker: np.mean(returns) for ticker, returns in performers.items()}

    # Convert to a DataFrame and rank by average return
    avg_returns_df = pd.DataFrame(list(average_returns.items()), columns=['Ticker', 'Average Return'])
    avg_returns_df['Rank'] = avg_returns_df['Average Return'].rank(ascending=False)
    avg_returns_df['Rank'] = avg_returns_df['Rank'].astype(int)
    avg_returns_df.set_index('Rank', inplace=True) 
    avg_returns_df = avg_returns_df.sort_values(by='Rank')
    
    avg_returns_df['Average Return'] = avg_returns_df['Average Return'] * 100
    avg_returns_df['Average Return'] = avg_returns_df['Average Return'].apply(lambda x: f"{x:.2f}")

    print(df)
    print(avg_returns_df)

def update_ticker(added_ticker, removed_ticker):
    if (added_ticker != ""):
        dow_tickers.append(added_ticker)
    
    if (removed_ticker != ""):
        if removed_ticker in dow_tickers:
            dow_tickers.remove(removed_ticker)

    return dow_tickers

# Call the test function
test_simulation()
