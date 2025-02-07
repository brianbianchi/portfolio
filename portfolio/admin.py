from django.contrib import admin
from .models import Asset, League, LeagueUser, Portfolio, Snapshot, Transaction

models = [Asset, League, LeagueUser, Portfolio, Snapshot, Transaction]
admin.site.register(models)
