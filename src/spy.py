from datetime import date
from datetime import datetime
from dateutil.relativedelta import relativedelta
import yfinance as yf

startDate = "2020-03-01"
endDate = "2024-03-01"

#investing in spy without monthly deposit
def spy_static(investment):
    dividend_gains = 0
    cash = investment
    shares = 0
    last_price = 0
    last_month = ""
    months = 0
    counter = 0

    ticker = yf.Ticker("SPY")

    df = ticker.history(period='max')

    dividend_days = df[(df["Dividends"] > 0.0)]
    
    for index, row in df.iterrows():
        if counter == 20:
            months += 1
            counter = 0
        if cash > row["Open"]:
            shares += (cash // row["Open"])
            cash -= shares * row["Open"]
            print("Shares Bought:", shares)
            print("Total Shares:", shares)
            print()
        
        if row["Dividends"] > 0.0:
            dividend_gains += row["Dividends"] * shares
            months += 1
            last_month = index
        
        counter += 1
            
        last_price = row["Close"]

    print(last_price)
    print("Initial Investment: $", investment, sep='')
    print("Shares:", shares)
    print("Cash After Sell:", format(((shares * last_price) + cash), ".2f"))
    print("Total Dividend Gain:", format(dividend_gains, ".2f"))
    print("Total Cash After Sell:", format(((shares * last_price) + cash + dividend_gains), ".2f"))
    print("Total Return (Percentage): ", format((((shares * last_price) + cash + dividend_gains)/3000) * 100, ".2f"), "%", sep='')
    print("Total Years: 30")
    print(last_month)

spy_static(100)