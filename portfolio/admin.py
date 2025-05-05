from django.contrib import admin
from .models import (
    Asset,
    FollowAsset,
    League,
    LeagueUser,
    Portfolio,
    Snapshot,
    Transaction,
)

models = [
    Asset,
    FollowAsset,
    League,
    LeagueUser,
    Portfolio,
    Snapshot,
    Transaction,
]
admin.site.register(models)
