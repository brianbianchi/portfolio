from django.urls import path
from .views import asset, core, league, league_user, portfolio, stripe, user

urlpatterns = [
    # core
    path("", core.home, name="home"),
    path("search", core.search, name="search"),
    path("register", user.register, name="register"),
    path("logout", user.logout_view, name="logout"),
    path("user/<name>/", user.user, name="user"),
    # assets
    path("asset/<ticker>/", asset.asset, name="asset"),
    path("follow/<str:ticker>/", asset.follow_ticker, name="follow_ticker"),
    path("popular_assets", asset.popular_assets, name="popular_assets"),
    # portfolio
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
    path("leaderboard/", portfolio.leaderboard, name="leaderboard"),
    # league
    path("league/<int:id>/", league.view_league, name="view_league"),
    path("create_league/", league.create_league, name="create_league"),
    path("edit_league/<int:id>/", league.edit_league, name="edit_league"),
    path("invite/<int:league_id>/", league_user.invite, name="invite"),
    # stripe
    path("checkout/", stripe.checkout, name="checkout"),
    path("manage_stripe/", stripe.manage_stripe, name="manage_stripe"),
    path("stripe-webhook/", stripe.stripe_webhook, name="stripe-webhook"),
]
