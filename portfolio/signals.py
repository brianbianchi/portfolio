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
        LeagueUser.objects.create(user=instance, league=league)
        Portfolio.objects.create(
            user=instance,
            league=league,
            value=league.start_value,
            name=instance.username,
        )


@receiver(post_save, sender=League)
def league_post_save(sender, instance, created, **kwargs):
    if created:
        LeagueUser.objects.create(user=instance.author, league=instance)


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
        Asset.objects.create(
            is_currency=True,
            ticker="",
            quantity=1,
            portfolio=instance,
            value=instance.league.start_value,
        )
        Snapshot.objects.create(portfolio=instance, value=instance.league.start_value)


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
        Asset.objects.create(
            portfolio=instance.portfolio,
            is_currency=False,
            ticker=instance.ticker,
            value=instance.value,
            quantity=instance.quantity,
        )

    cash = Asset.objects.get(portfolio=instance.portfolio, is_currency=True)
    if instance.is_purchase:
        cash.value -= Decimal(instance.value * instance.quantity)
    else:
        cash.value += Decimal(instance.value * instance.quantity)
    cash.save()
