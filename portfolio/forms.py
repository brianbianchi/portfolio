from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Asset, League, LeagueUser, Portfolio, Transaction
from .helper import get_stock_price


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["ticker", "quantity", "portfolio", "is_purchase", "value"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        ticker = kwargs.pop("ticker", None)
        default_portfolio = kwargs.pop("default_portfolio", None)
        default_is_purchase = kwargs.pop("default_is_purchase", True)
        super().__init__(*args, **kwargs)

        if user:
            portfolios = Portfolio.objects.filter(user=user)
            self.fields["portfolio"].queryset = portfolios
        else:
            self.fields["portfolio"].queryset = Portfolio.objects.none()

        if default_portfolio:
            self.fields["portfolio"].initial = default_portfolio

        self.fields["ticker"].initial = ticker
        self.fields["ticker"].disabled = True
        self.fields["ticker"].widget = forms.HiddenInput()
        self.fields["value"].disabled = True
        self.fields["value"].required = False
        self.fields["value"].widget = forms.HiddenInput()
        self.fields["is_purchase"].label = "Purchase?"
        self.fields["is_purchase"].initial = default_is_purchase

    def clean(self):
        cleaned_data = super().clean()
        is_purchase = self.cleaned_data.get("is_purchase")
        portfolio = self.cleaned_data.get("portfolio")
        ticker = self.cleaned_data.get("ticker")
        quantity = self.cleaned_data.get("quantity")
        price = get_stock_price(ticker)
        cleaned_data["value"] = price
        if is_purchase:
            cash = Asset.objects.get(is_currency=True, portfolio=portfolio)
            if price * quantity > cash.value:
                self.add_error(
                    None, f"You don't own enough cash to purchase {quantity} {ticker}."
                )
            cleaned_data["value"] = price
        else:
            try:
                asset = Asset.objects.get(ticker=ticker, portfolio=portfolio)
                if asset.quantity < quantity:
                    self.add_error(
                        None, f"You don't own enough {ticker} to sell {quantity}."
                    )
            except:
                self.add_error(
                    None, f"You don't own enough {ticker} to sell {quantity}."
                )

        return cleaned_data


class LeagueForm(forms.ModelForm):
    class Meta:
        model = League
        fields = ["name", "description", "start_value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            self.fields["start_value"].disabled = True


class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ["name", "league"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        default_league = kwargs.pop("default_league", None)
        super().__init__(*args, **kwargs)

        if user:
            league_users = LeagueUser.objects.filter(user=user).values("league")
            leagues = League.objects.filter(id__in=league_users)
            self.fields["league"].queryset = leagues
        else:
            self.fields["league"].queryset = League.objects.none()

        if default_league:
            self.fields["league"].initial = default_league


class LeagueUserForm(forms.ModelForm):
    username = forms.CharField(max_length=150, label="Username")

    class Meta:
        model = LeagueUser
        fields = ["league"]

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        default_league = kwargs.pop("default_league", None)
        super().__init__(*args, **kwargs)

        if user:
            league_users = LeagueUser.objects.filter(user=user).values("league")
            leagues = League.objects.filter(id__in=league_users)
            self.fields["league"].queryset = leagues
        else:
            self.fields["league"].queryset = League.objects.none()

        if default_league:
            self.fields["league"].initial = default_league

    def clean_username(self):
        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except:
            self.add_error("username", "Invalid user.")
        return user
