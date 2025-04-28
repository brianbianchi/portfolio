from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.shortcuts import render
import yfinance as yf
from ..helper import paginate
from ..models import FollowAsset, Portfolio


def home(request):
    # month_query = request.GET.get("month") or 1
    # convert to datetime
    # portfolios = MyModel.objects.filter(
    #     datetime_field__gte=start_of_month,
    #     datetime_field__lte=current_time
    # )
    portfolios = Portfolio.objects.filter(league__is_default=True).order_by("-value")
    protfolios_page = request.GET.get("portfolios-page") or 1
    protfolios_paged = paginate(portfolios, protfolios_page)
    my_protfolios_paged = None
    if request.user.is_authenticated:
        my_portfolios = portfolios.filter(user=request.user)
        my_protfolios_page = request.GET.get("my-portfolios-page") or 1
        my_protfolios_paged = paginate(my_portfolios, my_protfolios_page)
    most_followed_tickers = (
        FollowAsset.objects.values("ticker", "name")
        .annotate(follow_count=Count("user"))
        .order_by("-follow_count")
    )
    follow_page = request.GET.get("follow-page") or 1
    follow_paged = paginate(most_followed_tickers, follow_page)
    context = {
        "portfolios": protfolios_paged,
        "my_portfolios": my_protfolios_paged,
        "followed": follow_paged,
    }
    return render(request, "core/home.html", context)


def search(request):
    query = request.GET.get("q", "")
    if query == "":
        return render(
            request,
            "core/search.html",
            {
                "query": query,
                "users": None,
                "portfolios": None,
                "quotes": None,
            },
        )
    quotes = yf.Search(query, max_results=10, enable_fuzzy_query=False).quotes
    users = User.objects.filter(username__icontains=query).order_by("username")
    users_page = request.GET.get("users-page") or 1
    users_paged = paginate(users, users_page)
    portfolios = Portfolio.objects.filter(
        name__icontains=query, league__is_default=True
    ).order_by("-value")
    portfolios_page = request.GET.get("portfolios-page") or 1
    portfolios_paged = paginate(portfolios, portfolios_page)
    context = {
        "query": query,
        "users": users_paged,
        "portfolios": portfolios_paged,
        "quotes": quotes,
    }
    return render(request, "core/search.html", context)
