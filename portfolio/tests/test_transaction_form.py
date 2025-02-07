from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
import pandas as pd
from ..forms import TransactionForm
from ..models import Asset, League, Portfolio, Transaction


class TransactionFormTest(TestCase):

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
            name="Test Portfolio",
            user=self.user,
            league=self.league,
            value=self.league.start_value,
        )
        self.portfolio.save()
        self.transaction1 = Transaction(
            portfolio=self.portfolio,
            is_purchase=True,
            ticker="aapl",
            quantity=10,
            value=20.0,
        )
        self.transaction1.save()
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

    @patch("yfinance.Ticker.history")
    def test_form_buy_valid(self, mock_get_stock_price):
        mock_price = 150.25
        mock_get_stock_price.return_value = pd.DataFrame({"Close": [mock_price]})
        form_data = {
            "quantity": 3,
            "portfolio": self.portfolio.id,
            "is_purchase": True,
        }
        form = TransactionForm(
            data=form_data,
            user=self.user,
            ticker="aapl",
        )

        cash = Asset.objects.get(portfolio=self.portfolio, is_currency=True)
        self.assertLessEqual(mock_price * form.data["quantity"], cash.value)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    @patch("yfinance.Ticker.history")
    def test_form_buy_invalid(self, mock_get_stock_price):
        mock_price = 150.25
        mock_get_stock_price.return_value = pd.DataFrame({"Close": [mock_price]})
        form_data = {
            "quantity": 10,
            "portfolio": self.portfolio.id,
            "is_purchase": True,
        }
        form = TransactionForm(
            data=form_data,
            user=self.user,
            ticker="aapl",
        )

        cash = Asset.objects.get(portfolio=self.portfolio, is_currency=True)
        self.assertGreater(mock_price * form.data["quantity"], cash.value)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    @patch("yfinance.Ticker.history")
    def test_form_sell_valid(self, mock_get_stock_price):
        mock_price = 150.25
        mock_get_stock_price.return_value = pd.DataFrame({"Close": [mock_price]})
        form_data = {
            "quantity": 2,
            "portfolio": self.portfolio.id,
            "is_purchase": False,
        }
        form = TransactionForm(
            data=form_data,
            user=self.user,
            ticker="aapl",
        )
        stock = Asset.objects.get(
            portfolio=self.portfolio, ticker=self.transaction1.ticker
        )
        self.assertGreaterEqual(stock.quantity, form.data["quantity"])
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)

    @patch("yfinance.Ticker.history")
    def test_form_sell_invalid(self, mock_get_stock_price):
        mock_price = 150.25
        mock_get_stock_price.return_value = pd.DataFrame({"Close": [mock_price]})
        form_data = {
            "quantity": 10,
            "portfolio": self.portfolio.id,
            "is_purchase": False,
        }
        form = TransactionForm(
            data=form_data,
            user=self.user,
            ticker="aapl",
        )

        stock = Asset.objects.get(
            portfolio=self.portfolio, ticker=self.transaction1.ticker
        )
        self.assertLess(stock.quantity, form.data["quantity"])
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)
