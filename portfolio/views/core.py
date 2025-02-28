from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
import yfinance as yf
from ..helper import paginate
from ..models import League, Portfolio


def home(request):
    return render(request, "core/home.html")


def search(request):
    query = request.GET.get("q", "")
    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.Search.html#yfinance.Search
    quotes = yf.Search(query, max_results=10, enable_fuzzy_query=False).quotes
    users = User.objects.filter(username__icontains=query).order_by("username")
    users_page = request.GET.get("users-page") or 1
    users_paged = paginate(users, users_page)
    portfolios = Portfolio.objects.filter(
        name__icontains=query, league__is_default=True
    ).order_by("-value")
    portfolios_page = request.GET.get("portfolios-page") or 1
    portfolios_paged = paginate(portfolios, portfolios_page)
    context = {"users": users_paged, "portfolios": portfolios_paged, "quotes": quotes}
    return render(request, "core/search.html", context)
