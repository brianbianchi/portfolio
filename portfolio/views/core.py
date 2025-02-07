from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
import yfinance as yf
from ..helper import paginate
from ..models import League, Portfolio


def home(request):
    league = League.objects.order_by("created").first()
    portfolios = Portfolio.objects.filter(league=league).order_by("-value")[:5]
    return render(request, "core/home.html", {"portfolios": portfolios})


def search(request):
    query = request.GET.get("q", "")
    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.Search.html#yfinance.Search
    quotes = yf.Search(query, max_results=10, enable_fuzzy_query=False).quotes
    users = User.objects.filter(username__icontains=query).order_by("username")
    users_page = request.GET.get("users-page") or 1
    users_paged = paginate(users, users_page)
    leagues = League.objects.filter(name__icontains=query).order_by("-num_users")
    leagues_page = request.GET.get("leagues-page") or 1
    leagues_paged = paginate(leagues, leagues_page)
    context = {"users": users_paged, "leagues": leagues_paged, "quotes": quotes}
    return render(request, "core/search.html", context)
