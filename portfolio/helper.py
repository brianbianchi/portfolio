from decimal import Decimal
import yfinance as yf


def get_stock_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        stock_price = stock.history(period="1d")["Close"].iloc[0]
        return round(Decimal(stock_price), 2)
    except Exception as e:
        return f"Error: {str(e)}"
