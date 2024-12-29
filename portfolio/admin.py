from django.contrib import admin
from .models import League, LeagueUser, Portfolio, Asset, Transaction

models = [League, LeagueUser, Portfolio, Asset, Transaction]
admin.site.register(models)
