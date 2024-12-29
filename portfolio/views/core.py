from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
import yfinance as yf
from ..models import League


def home(request):
    return render(request, "portfolio/home.html")


def search(request):
    query = request.GET.get("q", "")
    # https://ranaroussi.github.io/yfinance/reference/api/yfinance.Search.html#yfinance.Search
    quotes = yf.Search(query, max_results=10, enable_fuzzy_query=False).quotes
    users = User.objects.filter(username__icontains=query)
    leagues = League.objects.filter(name__icontains=query)
    context = {"users": users, "leagues": leagues, "quotes": quotes}
    return render(request, "portfolio/search.html", context)
