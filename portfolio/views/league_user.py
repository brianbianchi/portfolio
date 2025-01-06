from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from ..forms import LeagueUserForm
from ..models import League, LeagueUser


@login_required(login_url="/login")
def invite(request, league_id):
    league = League.objects.get(id=league_id)
    if request.method == "POST":
        form = LeagueUserForm(request.POST, user=request.user, default_league=league)
        if form.is_valid():
            league_user = LeagueUser()
            league_user.user = form.cleaned_data["username"]
            league_user.league = form.cleaned_data["league"]
            if not LeagueUser.objects.filter(
                user=league_user.user, league=league_user.league
            ).exists():
                league_user.save()
            return redirect(f"/league/{league_user.league.id}")
        else:
            return render(request, "portfolio/invite.html", {"form": form})
    else:
        form = LeagueUserForm(user=request.user, default_league=league)

    return render(request, "portfolio/invite.html", {"form": form})
