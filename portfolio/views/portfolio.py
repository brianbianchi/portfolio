from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from ..forms import PortfolioForm
from ..models import Asset, League, Portfolio, Snapshot, Transaction


def view_portfolio(request, id):
    if request.method != "GET":
        return HttpResponseNotAllowed
    try:
        portfolio = Portfolio.objects.get(id=id)
        txns = Transaction.objects.filter(portfolio=portfolio)
        assets = Asset.objects.filter(portfolio=portfolio)
        snapshots = Snapshot.objects.all().order_by("created")
        print(snapshots)

        dates = [snapshot.created.strftime("%Y-%m-%d") for snapshot in snapshots]
        print(dates)
        values = [str(snapshot.value) for snapshot in snapshots]
        print(values)
        context = {
            "portfolio": portfolio,
            "txns": txns,
            "assets": assets,
            "graph_dates": dates,
            "graph_values": values,
        }
        return render(request, "portfolio/portfolio.html", context)
    except Exception as e:
        print(f"Error: {str(e)}")
        return render(request, "shared/404.html")


@login_required(login_url="/login")
def create_portfolio(request, league_id):
    league = League.objects.get(id=league_id)
    if request.method == "POST":
        form = PortfolioForm(request.POST, user=request.user, default_league=league)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user
            portfolio.save()
            return redirect(f"/portfolio/{portfolio.id}")
    else:
        form = PortfolioForm(user=request.user, default_league=league)

    return render(request, "portfolio/create_portfolio.html", {"form": form})


@login_required(login_url="/login")
def edit_portfolio(request, id):
    portfolio = Portfolio.objects.get(id=id)
    if request.user != portfolio.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = PortfolioForm(request.POST, instance=portfolio, user=request.user)
        if form.is_valid():
            form.save()
            return redirect(f"/portfolio/{portfolio.id}")
    form = PortfolioForm(instance=portfolio, user=request.user)
    return render(request, "portfolio/edit_portfolio.html", {"form": form})


@login_required(login_url="/login")
def delete_portfolio(request, id):
    portfolio = Portfolio.objects.get(id=id)
    if request.user != portfolio.user:
        return HttpResponseForbidden()
    portfolio.delete()
    return redirect(f"/user/{request.user.username}")
