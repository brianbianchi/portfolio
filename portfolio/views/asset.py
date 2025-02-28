from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
import yfinance as yf
from ..helper import paginate
from ..forms import TransactionForm
from ..models import FollowAsset


def asset(request, ticker):
    try:
        is_following = False
        if request.user.is_authenticated:
            follow_assets = FollowAsset.objects.filter(user=request.user, ticker=ticker)
            if follow_assets.first():
                is_following = True
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
                existing_follow = FollowAsset.objects.filter(
                    user=request.user, ticker=ticker
                ).first()
                if not existing_follow:
                    FollowAsset.objects.create(user=request.user, ticker=ticker)
                return redirect(f"/portfolio/{txn.portfolio.id}")
        context = {
            "ticker": ticker,
            "price": current_price,
            "info": info,
            "is_following": is_following,
            "form": form,
        }
        return render(request, "core/asset.html", context)
    except Exception as e:
        print(e)
        return render(request, "shared/404.html")


@login_required
def follow_ticker(request, ticker):
    existing_follow = FollowAsset.objects.filter(
        user=request.user, ticker=ticker
    ).first()

    if not existing_follow:
        FollowAsset.objects.create(user=request.user, ticker=ticker)
        action = "followed"
    else:
        existing_follow.delete()
        action = "unfollowed"

    return JsonResponse({"action": action})


def popular_assets(request):
    most_followed_tickers = (
        FollowAsset.objects.values("ticker")
        .annotate(follow_count=Count("user"))
        .order_by("-follow_count")
    )
    follow_page = request.GET.get("follow-page") or 1
    follow_paged = paginate(most_followed_tickers, follow_page)
    context = {"followed": follow_paged}
    return render(request, "core/popular_assets.html", context)
