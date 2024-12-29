from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from ..forms import RegisterForm
from ..models import League, Portfolio


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


def user(request, name):
    user = User.objects.get_by_natural_key(username=name)
    portfolios = Portfolio.objects.filter(user=user)
    context = {"user": user, "portfolios": portfolios}
    return render(request, "portfolio/user.html", context)
