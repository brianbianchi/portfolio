from decimal import Decimal
from django.core.management.base import BaseCommand
from ...helper import get_stock_price
from ...models import Asset, Portfolio, Snapshot


class Command(BaseCommand):
    help = "Update portfolio prices"

    def handle(self, *args, **kwargs):
        print("Update portfolio prices")
        cache = {}
        portfolios = Portfolio.objects.all()
        for portfolio in portfolios:
            assets = Asset.objects.filter(portfolio=portfolio)
            total_value = Decimal(0)
            for asset in assets:
                if asset.is_currency:
                    continue
                price = Decimal(0)
                if asset.ticker in cache:
                    price = cache[asset.ticker]
                else:
                    price = get_stock_price(asset.ticker)
                    cache[asset.ticker] = price
                asset.value = price
                asset.save()
                total_value += price
            snapshot = Snapshot()
            snapshot.portfolio = portfolio
            snapshot.value = total_value
            snapshot.save()
