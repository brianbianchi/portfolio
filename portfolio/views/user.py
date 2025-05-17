from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from ..helper import paginate
from ..forms import RegisterForm
from ..models import FollowAsset, League, LeagueUser, Portfolio


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    else:
        form = RegisterForm()

    return render(request, "registration/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("/")


def user(request, name):
    try:
        user = User.objects.get_by_natural_key(username=name)
        league_users = LeagueUser.objects.filter(user=user).values("league")
        leagues = League.objects.filter(id__in=league_users).order_by("-num_users")
        leagues_page = request.GET.get("leagues-page") or 1
        leagues_paged = paginate(leagues, leagues_page)
        portfolios = Portfolio.objects.filter(user=user).order_by("-value")
        portfolios_page = request.GET.get("portfolios-page") or 1
        portfolios_paged = paginate(portfolios, portfolios_page)
        followed = FollowAsset.objects.filter(user=user).order_by("ticker")
        followed_page = request.GET.get("follow-page") or 1
        followed_paged = paginate(followed, followed_page)
        context = {
            "user": user,
            "leagues": leagues_paged,
            "portfolios": portfolios_paged,
            "followed": followed_paged,
        }
        return render(request, "core/user.html", context)
    except Exception as e:
        print(f"Error: {str(e)}")
        raise e
