from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import yfinance as yf
from ..forms import TransactionForm
from ..models import FollowAsset


def asset(request, ticker):
    try:
        is_following = False
        if request.user.is_authenticated:
            follow_assets = FollowAsset.objects.filter(user=request.user, ticker=ticker)
            if follow_assets.first():
                is_following = True
        info = yf.Ticker(ticker).info
        news = yf.Search(ticker).news
        form = TransactionForm(request=request, ticker=ticker)
        if request.method == "POST":
            form = TransactionForm(request.POST, request=request, ticker=ticker)
            if form.is_valid():
                txn = form.save(commit=False)
                txn.is_purchase = "buy-btn" in request.POST
                txn.save()
                existing_follow = FollowAsset.objects.filter(
                    user=request.user, ticker=ticker
                ).first()
                if not existing_follow:
                    FollowAsset.objects.create(
                        user=request.user, ticker=ticker, name=info.longName
                    )
                return redirect(f"/portfolio/{txn.portfolio.id}")
        context = {
            "ticker": ticker,
            "info": info,
            "news": news,
            "is_following": is_following,
            "form": form,
        }
        return render(request, "core/asset.html", context)
    except Exception as e:
        print(e)
        return render(request, "shared/404.html")


@login_required
def follow_ticker(request, ticker, name):
    existing_follow = FollowAsset.objects.filter(
        user=request.user, ticker=ticker
    ).first()

    if not existing_follow:
        FollowAsset.objects.create(user=request.user, ticker=ticker, name=name)
        action = "followed"
    else:
        existing_follow.delete()
        action = "unfollowed"

    return JsonResponse({"action": action})
