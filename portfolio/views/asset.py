from django.shortcuts import redirect, render
import yfinance as yf
from ..forms import TransactionForm
from ..models import Portfolio


def asset(request, ticker):
    try:
        portfolios = None
        if request.user:
            portfolios = Portfolio.objects.filter(user=request.user.id)
        asset = yf.Ticker(ticker)
        current_price = asset.history(period="1d")["Close"].iloc[0]
        info = asset.info
        form = TransactionForm(request=request, ticker=ticker)
        if request.method == "POST":
            form = TransactionForm(request.POST, request=request, ticker=ticker)
            if form.is_valid():
                txn = form.save(commit=False)
                txn.is_purchase = "buy-btn" in request.POST
                txn.save()
                return redirect(f"/portfolio/{txn.portfolio.id}")
        context = {
            "price": current_price,
            "info": info,
            "portfolios": portfolios,
            "form": form,
        }
        return render(request, "core/asset.html", context)
    except Exception as e:
        print(e)
        return render(request, "shared/404.html")
