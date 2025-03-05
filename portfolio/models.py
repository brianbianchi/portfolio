from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_value = models.DecimalField(decimal_places=0, max_digits=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(default=False)
    num_portfolios = models.IntegerField(default=0)
    num_users = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class LeagueUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    league = models.ForeignKey(League, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "league"], name="unique_user_in_league"
            )
        ]

    def __str__(self):
        return f"{self.user.username} is a part of {self.league.name}"


class Portfolio(models.Model):
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(decimal_places=2, max_digits=200)

    @property
    def change(self):
        return round((self.value - self.league.start_value), 2)

    @property
    def perc_change(self):
        start_value = self.league.start_value
        perc = ((self.value - start_value) / start_value) * 100
        return round(perc, 2)

    def __str__(self):
        return f"{self.name}"


class Snapshot(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=200)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.portfolio.name} has a value of {self.value} as of {self.created}"


class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    is_currency = models.BooleanField(default=False)
    ticker = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=200)
    quantity = models.IntegerField()

    @property
    def total_value(self):
        if self.is_currency:
            return self.value
        return self.value * self.quantity

    def __str__(self):
        return f"{self.portfolio.name} has {self.quantity} {self.ticker}"


class FollowAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=200)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "ticker"], name="unique_user_following_ticker"
            )
        ]

    def __str__(self):
        return f"{self.user.username} is following {self.ticker}"


class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    is_purchase = models.BooleanField(default=False)
    ticker = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=200)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_value(self):
        return self.value * self.quantity

    def __str__(self):
        return f"{self.portfolio.name} bought {self.quantity} {self.ticker}"


class StripeSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, help_text="The user who initiated the checkout."
    )
    stripe_customer_id = models.CharField(max_length=255)
    stripe_checkout_session_id = models.CharField(max_length=255)
    stripe_price_id = models.CharField(max_length=255)
    league = models.ForeignKey(
        League, on_delete=models.SET_NULL, null=True, blank=True, default=None
    )
    is_paid = models.BooleanField(default=False)
