from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.management import call_command
from ..models import Asset, League, Portfolio, Snapshot, Transaction


class AssetsTest(TestCase):

    def setUp(self):
        self.superuser = User.objects.create_superuser(username="admin")
        call_command("init")
        self.user = User.objects.create(
            username="exampleuser", email="exampleuser@gmail.com"
        )
        self.league = League.objects.create(
            name="Test League",
            description="Description of the Test League",
            start_value=1000,
            author=self.user,
        )
        self.portfolio = Portfolio.objects.create(
            name="Test Portfolio",
            user=self.user,
            league=self.league,
            value=self.league.start_value,
        )

    def test_assets_created(self):
        transaction1 = Transaction.objects.create(
            portfolio=self.portfolio,
            is_purchase=True,
            ticker="aapl",
            quantity=10,
            value=20.0,
        )
        transaction2 = Transaction.objects.create(
            portfolio=self.portfolio,
            is_purchase=False,
            ticker="aapl",
            quantity=4,
            value=20.0,
        )
        transaction3 = Transaction.objects.create(
            portfolio=self.portfolio,
            is_purchase=False,
            ticker="aapl",
            quantity=3,
            value=20.0,
        )

        assets = Asset.objects.filter(portfolio=self.portfolio)
        self.assertEqual(assets.count(), 2)
        cash = assets.get(is_currency=True)
        self.assertEqual(
            cash.value,
            self.league.start_value
            - transaction1.total_value
            + transaction2.total_value
            + transaction3.total_value,
        )
        stock = assets.get(ticker=transaction1.ticker)
        self.assertEqual(
            stock.quantity,
            transaction1.quantity - transaction2.quantity - transaction3.quantity,
        )
        self.assertEqual(stock.value, transaction1.value)
        self.assertEqual(stock.total_value, stock.quantity * stock.value)

    def test_initial_cash_asset_created(self):
        assets = Asset.objects.filter(portfolio=self.portfolio)
        self.assertEqual(assets.count(), 1)
        cash = assets.get(is_currency=True)
        self.assertEqual(cash.value, self.league.start_value)

    def test_initial_snapshot_created(self):
        snapshots = Snapshot.objects.filter(portfolio=self.portfolio)
        self.assertEqual(snapshots.count(), 1)
        self.assertEqual(snapshots[0].value, self.league.start_value)
