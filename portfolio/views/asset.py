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
        form = TransactionForm(
            user=request.user, ticker=ticker, default_is_purchase=True
        )
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
        return render(request, "core/asset.html", context)
    except:
        return render(request, "shared/404.html")
