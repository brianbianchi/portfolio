import calendar
import datetime
from decimal import Decimal
from django.core.paginator import Paginator
import yfinance as yf


def get_stock_price(ticker_symbol):
    try:
        stock = yf.Ticker(ticker_symbol)
        stock_price = stock.history(period="1d")["Close"].iloc[0]
        return round(Decimal(stock_price), 2)
    except Exception as e:
        return f"Error: {str(e)}"


def paginate(list, page_number):
    PAGE_SIZE = 12
    paginator = Paginator(list, PAGE_SIZE)
    return paginator.get_page(page_number)


def get_date_query(dt: datetime):
    min = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = calendar.monthrange(dt.year, dt.month)[1]
    max = dt.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    return min, max
