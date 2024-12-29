from decimal import Decimal
from django.shortcuts import redirect, render
from django.http import (
    HttpResponseForbidden,
    HttpResponseNotAllowed,
    HttpResponseBadRequest,
)
import yfinance as yf
from ..helper import get_stock_price
from ..forms import TransactionForm
from ..models import Asset, League, Portfolio, Transaction


def asset(request, ticker):
    portfolios = None
    if request.user:
        portfolios = Portfolio.objects.filter(user=request.user.id)
    asset = yf.Ticker(ticker)
    current_price = asset.history(period="1d")["Close"].iloc[0]
    info = asset.info
    form = TransactionForm(user=request.user, ticker=ticker, default_is_purchase=True)
    if request.method == "POST":
        form = TransactionForm(
            request.POST, user=request.user, ticker=ticker, default_is_purchase=True
        )
        if form.is_valid():
            txn = form.save(commit=False)
            txn.save()
            return redirect(f"/portfolio/{txn.portfolio.id}")
    context = {
        "price": current_price,
        "info": info,
        "portfolios": portfolios,
        "form": form,
    }
    return render(request, "portfolio/asset.html", context)
