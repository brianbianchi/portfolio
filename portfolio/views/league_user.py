from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ..forms import LeagueUserForm
from ..models import League, LeagueUser


@login_required(login_url="/login")
def invite(request, league_id):
    league = League.objects.get(id=league_id)
    form = LeagueUserForm(user=request.user, default_league=league)
    if request.method == "POST":
        form = LeagueUserForm(request.POST, user=request.user, default_league=league)
        if form.is_valid():
            league_user = LeagueUser(
                user=form.cleaned_data["username"], league=form.cleaned_data["league"]
            )
            existing = LeagueUser.objects.filter(
                user=league_user, league=league_user.league
            ).exists()
            if not existing:
                league_user.save()
            return redirect(f"/league/{league_user.league.id}")

    return render(request, "league/invite.html", {"form": form})
