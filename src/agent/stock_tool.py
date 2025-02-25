import yfinance as yf
import datetime


def get_stock_price(symbol: str, date: str) -> str:
    """
    This tool retrieves the historical closing price for a specified stock symbol on a given date.
    It uses Yahoo Finance's API to fetch stock data and returns the closing price formatted as a string.
    Args:
        symbol: the first argument
        date: the second argument
    """
    # Convert string date to datetime
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
    
    # Get stock data for the specified symbol
    ticker = yf.Ticker(symbol)
    
    # Get historical data including the specified date
    hist = ticker.history(start=date_obj, end=date_obj + datetime.timedelta(days=1))
    
    if len(hist) == 0:
        return f"No stock price data available for {symbol} on {date}"
        
    # Get closing price for the date
    price = hist['Close'][0]
    return f"{symbol} price for {date}: ${price:.2f}"