from django.contrib import admin
from .models import (
    Asset,
    FollowAsset,
    League,
    LeagueUser,
    Portfolio,
    Snapshot,
    StripeSession,
    Transaction,
)

models = [
    Asset,
    FollowAsset,
    League,
    LeagueUser,
    Portfolio,
    Snapshot,
    StripeSession,
    Transaction,
]
admin.site.register(models)
