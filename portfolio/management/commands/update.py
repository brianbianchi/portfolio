from datetime import datetime
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
            if not assets:
                continue
            total_value = Decimal(0)
            for asset in assets:
                if asset.is_currency:
                    total_value += asset.value
                    continue
                price = Decimal(0)
                if asset.ticker in cache:
                    price = cache[asset.ticker]
                else:
                    price = get_stock_price(asset.ticker)
                    cache[asset.ticker] = price
                asset.previous_close = asset.value
                asset.value = price
                asset.save()
                total_value += price * asset.quantity
            Snapshot.objects.create(portfolio=portfolio, value=total_value)
            portfolio.value = total_value
            portfolio.save()
