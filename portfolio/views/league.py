from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from ..forms import LeagueForm
from ..models import League, LeagueUser, Portfolio


def view_league(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed
    league = League.objects.get(id=id)
    portfolios = Portfolio.objects.filter(league=league)
    league_users = LeagueUser.objects.filter(league=league)
    context = {"league": league, "portfolios": portfolios, "league_users": league_users}
    return render(request, "portfolio/league.html", context)


def view_leagues(request):
    if request.method != "GET":
        return HttpResponseNotAllowed
    PAGE_SIZE = 25
    page = request.GET.get("page") or 1
    leagues = League.objects.all()
    paginator = Paginator(leagues, PAGE_SIZE)
    leagues_page = paginator.get_page(page)
    return render(request, "portfolio/leagues.html", {"leagues": leagues_page})


@login_required(login_url="/login")
def create_league(request):
    if request.method == "POST":
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.author = request.user
            league.save()
            # create LeagueUser
            return redirect(f"/league/{league.id}")
    else:
        form = LeagueForm()

    return render(request, "portfolio/create_league.html", {"form": form})


@login_required(login_url="/login")
def edit_league(request, id):
    league = League.objects.get(id=id)
    if request.user != league.author:
        return HttpResponseForbidden
    if request.method == "POST":
        form = LeagueForm(request.POST, instance=league)
        if form.is_valid():
            form.save()
            return redirect(f"/league/{league.id}")
    form = LeagueForm(instance=league)
    return render(request, "portfolio/edit_league.html", {"form": form})


@login_required(login_url="/login")
def delete_league(request, id):
    league = League.objects.get(id=id)
    if request.user != league.author:
        return HttpResponseForbidden
    league.delete()
    return redirect(f"/user/{request.user.username}")
