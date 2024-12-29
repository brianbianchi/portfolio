from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Asset, League, LeagueUser, Portfolio, Transaction


@receiver(post_save, sender=League)
def league_post_save(sender, instance, created, **kwargs):
    if created:
        league_user = LeagueUser()
        league_user.user = instance.author
        league_user.league = instance
        league_user.save()


@receiver(post_save, sender=Portfolio)
def portfolio_post_save(sender, instance, created, **kwargs):
    if created:
        asset = Asset()
        asset.is_currency = True
        asset.ticker = ""
        asset.quantity = 1
        asset.portfolio = instance
        asset.value = instance.league.start_value
        asset.save()


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
    except Exception as e:
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
