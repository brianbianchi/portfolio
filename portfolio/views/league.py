from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from ..helper import paginate
from ..forms import LeagueForm
from ..models import League, LeagueUser, Portfolio


def view_league(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed("This method is not allowed.")
    try:
        league = League.objects.get(id=id)
        portfolios = Portfolio.objects.filter(league=league).order_by("-value")
        portfolios_page = request.GET.get("portfolios-page") or 1
        portfolios_paged = paginate(portfolios, portfolios_page)
        league_users = LeagueUser.objects.filter(league=league).values("user")
        users = User.objects.filter(id__in=league_users).order_by("username")
        users_page = request.GET.get("users-page") or 1
        users_paged = paginate(users, users_page)
        has_access = request.user in users
        context = {
            "league": league,
            "portfolios": portfolios_paged,
            "users": users_paged,
            "has_access": has_access,
        }
        return render(request, "league/league.html", context)
    except Exception as e:
        print(e)
        raise e


@login_required(login_url="/login")
def create_league(request):
    if request.method == "POST":
        form = LeagueForm(request.POST)
        if form.is_valid():
            league = form.save(commit=False)
            league.author = request.user
            league.save()
            return redirect(f"/league/{league.id}")
    else:
        form = LeagueForm()

    return render(request, "league/create_league.html", {"form": form})


@login_required(login_url="/login")
def edit_league(request, id):
    league = League.objects.get(id=id)
    if request.user != league.author:
        return HttpResponseForbidden("You're forbidden from editing this league.")
    if request.method == "POST":
        form = LeagueForm(request.POST, instance=league)
        if form.is_valid():
            form.save()
            return redirect(f"/league/{league.id}")
    form = LeagueForm(instance=league)
    return render(request, "league/edit_league.html", {"form": form})
