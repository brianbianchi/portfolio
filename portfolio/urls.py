from django.urls import path
from .views import asset, core, league, league_user, portfolio, user

urlpatterns = [
    path("", core.home, name="home"),
    path("search", core.search, name="search"),
    path("register", user.register, name="register"),
    path("user/<name>/", user.user, name="user"),
    path("asset/<ticker>/", asset.asset, name="asset"),
    path("portfolio/<int:id>/", portfolio.view_portfolio, name="view_portfolio"),
    path(
        "create_portfolio/<int:league_id>/",
        portfolio.create_portfolio,
        name="create_portfolio",
    ),
    path("edit_portfolio/<int:id>/", portfolio.edit_portfolio, name="edit_portfolio"),
    path(
        "delete_portfolio/<int:id>/",
        portfolio.delete_portfolio,
        name="delete_portfolio",
    ),
    path("league/<int:id>/", league.view_league, name="view_league"),
    path("leagues/", league.view_leagues, name="view_leagues"),
    path("create_league/", league.create_league, name="create_league"),
    path("edit_league/<int:id>/", league.edit_league, name="edit_league"),
    path("delete_league/<int:id>/", league.delete_league, name="delete_league"),
    path("invite/<int:league_id>/", league_user.invite, name="invite"),
]
