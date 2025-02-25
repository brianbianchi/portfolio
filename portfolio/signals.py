from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from .models import Asset, League, LeagueUser, Portfolio, Snapshot, Transaction


@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    if created:
        league = League.objects.filter(is_default=True).first()
        if not league:
            return
        league_user = LeagueUser()
        league_user.user = instance
        league_user.league = league
        league_user.save()
        portfolio = Portfolio()
        portfolio.user = instance
        portfolio.league = league
        portfolio.value = league.start_value
        portfolio.name = instance.username
        portfolio.save()


@receiver(post_save, sender=League)
def league_post_save(sender, instance, created, **kwargs):
    if created:
        league_user = LeagueUser()
        league_user.user = instance.author
        league_user.league = instance
        league_user.save()


@receiver(post_save, sender=LeagueUser)
def league_user_post_save(sender, instance, created, **kwargs):
    if created:
        league = instance.league
        league.num_users += 1
        league.save()


@receiver(post_delete, sender=LeagueUser)
def league_user_deleted(sender, instance, **kwargs):
    league = instance.league
    league.num_users -= 1
    league.save()


@receiver(post_save, sender=Portfolio)
def portfolio_post_save(sender, instance, created, **kwargs):
    if created:
        league = instance.league
        league.num_portfolios += 1
        league.save()
        asset = Asset()
        asset.is_currency = True
        asset.ticker = ""
        asset.quantity = 1
        asset.portfolio = instance
        asset.value = instance.league.start_value
        asset.save()
        snapshot = Snapshot()
        snapshot.portfolio = instance
        snapshot.value = instance.league.start_value
        snapshot.save()


@receiver(post_delete, sender=Portfolio)
def portfolio_deleted(sender, instance, **kwargs):
    league = instance.league
    league.num_portfolios -= 1
    league.save()


@receiver(post_save, sender=Transaction)
def txn_post_save(sender, instance, created, **kwargs):
    try:
        asset = Asset.objects.get(
            portfolio=instance.portfolio, ticker=instance.ticker, is_currency=False
        )
        if instance.is_purchase:
            asset.quantity += instance.quantity
            asset.value = instance.value
            asset.save()
        elif not instance.is_purchase and asset.quantity - instance.quantity == 0:
            asset.delete()
        else:
            asset.quantity -= instance.quantity
            asset.value = instance.value
            asset.save()
    except:
        asset = Asset()
        asset.portfolio = instance.portfolio
        asset.is_currency = False
        asset.ticker = instance.ticker
        asset.value = instance.value
        asset.quantity = instance.quantity
        asset.save()

    cash = Asset.objects.get(portfolio=instance.portfolio, is_currency=True)
    if instance.is_purchase:
        cash.value -= Decimal(instance.value * instance.quantity)
    else:
        cash.value += Decimal(instance.value * instance.quantity)
    cash.save()
