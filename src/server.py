from flask import Flask, render_template_string

# app.py
from flask import jsonify, request
from flask_cors import CORS
from single_mixed import single_stock
from single_mixed import mixed_invest
from turtle_sim import turtle_trading_simulation
from dow import test_simulation
from dow import get_dow_tickers
from dow import update_ticker
# from functions.stocks import analyze_stocks

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/update_tickers": {"origins": "http://localhost:8000"}})

@app.route('/single_stock', methods=['POST'])
def simulate_single_stock():
    data = request.json
    ticker = data.get('arg1')
    start_date = data.get('arg2')
    end_date = data.get('arg3')
    initial = data.get('arg4')
    monthly = data.get('arg5')
    
    start_price, last_price, total_shares, total_contribution, cash_after_sell, total_return, annualized, buy_date, sell_date = single_stock(start_date, end_date, int(initial), ticker, int(monthly))
    return jsonify({"start": start_price, "end": last_price, "total_shares": total_shares, "contribution": total_contribution, 
                    "total cash": cash_after_sell, "total return": total_return, "annualized": annualized, "buy_date": buy_date, "sell_date": sell_date})

@app.route('/mixed_stocks', methods=['POST'])
def simulate_mixed_stock():
    # start_date, end_date, investment, stock_one, stock_two, monthly, allocation, buy_date, sell_date
    data = request.json
    arg1 = data.get('arg1')
    arg2 = data.get('arg2')
    arg3 = data.get('arg3')
    arg4 = data.get('arg4')
    arg5 = data.get('arg5')
    arg6 = data.get('arg6')
    arg7 = data.get('arg7')
    
    start_price_one, last_price_one, start_price_two, last_price_two, total_shares_one, total_shares_two, total_contribution, total_value, total_return, annualized_return, buy_date_one, sell_date_one, buy_date_two, sell_date_two = mixed_invest(arg1, arg2, int(arg3), arg4, arg5, int(arg6), float(arg7))
    return jsonify({"start_one": start_price_one, "end_one": last_price_one, "start_two": start_price_two, "end_two": last_price_two, "total_shares_one": total_shares_one, "total_shares_two": total_shares_two, "contribution": total_contribution, 
                    "total cash": total_value, "total return": total_return, "annualized": annualized_return, "buy_date_one": buy_date_one, "sell_date_one": sell_date_one, "buy_date_two": buy_date_two, "sell_date_two": sell_date_two})

@app.route('/turtle', methods=['POST'])
def simulate_turtle_trading():
    # ticker, start_date, end_date, initial_balance, risk_percent, high_days, loss_days
    data = request.json
    ticker = data.get('arg1')
    start_date = data.get('arg2')
    end_date = data.get('arg3')
    initial = data.get('arg4')
    risk_percent = data.get('arg5')
    high_days = data.get('arg6')
    loss_days = data.get('arg7')
    
    trade_df, initial_balance, prev_balance, max_gain, drawdown, total_return, annualized_return, buy_date, sell_date = turtle_trading_simulation(ticker, start_date, end_date, int(initial), float(risk_percent), int(high_days), int(loss_days))
    return jsonify({"trade_df": trade_df, "initial": initial_balance, "prev_balance": prev_balance, "max_gain": max_gain, "drawdown": drawdown,
                    "total return": total_return, "annualized": annualized_return, "buy_date": buy_date, "sell_date": sell_date})

@app.route('/dow', methods=['POST'])
def simulate_dogs_of_dow():
    # start_year, end_year, initial_investment, yearly_deposit, num_dogs
    data = request.json
    start_year = data.get('arg1')
    end_year = data.get('arg2')
    initial = data.get('arg3')
    yearly = data.get('arg4')
    num_dogs = data.get('arg5')
    
    portfolio_table, performers_table, total_return, annualized_return = test_simulation(int(start_year), int(end_year), int(initial), int(yearly), int(num_dogs))
    return jsonify({"portfolio_table": portfolio_table, "performers_table": performers_table, "total_return": total_return, "annualized_return": annualized_return})

@app.route('/get_tickers', methods=['GET'])
def get_tickers():
    print("getting tickers")
    tickers = get_dow_tickers()
    return jsonify({"tickers": tickers})


@app.route('/update_tickers', methods=['POST'])
def update_dow_tickers():
    data = request.json
    add = data.get('add')
    remove = data.get('remove')
    
    update_ticker(add, remove)
    
    return jsonify({"data":""})

if __name__ == '__main__':
    app.run(debug=True)

# GET LIST OF DOGS DISPLAYED ON PAGE ONLOAD, SETUP FUNCTION FOR IT AND NEW ROUTE
# ADD TWO FIELDS AND UPDATE DOGS BUTTON TO ALLOW FOR CHANGES TO DOGS OF DOW
# THEN CODE CLEANUP AND DONE