from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Asset, League, Portfolio, Transaction


class AssetsTest(TestCase):

    def setUp(self):
        self.user = User(username="exampleuser", email="exampleuser@gmail.com")
        self.user.save()
        self.league = League(
            name="Test League",
            description="Description of the Test League",
            start_value=1000,
            author=self.user,
        )
        self.league.save()
        self.portfolio = Portfolio(
            name="Test Portfolio", user=self.user, league=self.league
        )
        self.portfolio.save()

    def test_assets_created(self):
        transaction1 = Transaction(
            portfolio=self.portfolio,
            is_purchase=True,
            ticker="aapl",
            quantity=10,
            value=20.0,
        )
        transaction1.save()
        transaction2 = Transaction(
            portfolio=self.portfolio,
            is_purchase=False,
            ticker="aapl",
            quantity=4,
            value=20.0,
        )
        transaction2.save()
        transaction3 = Transaction(
            portfolio=self.portfolio,
            is_purchase=False,
            ticker="aapl",
            quantity=3,
            value=20.0,
        )
        transaction3.save()

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
