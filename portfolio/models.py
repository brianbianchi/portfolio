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
    last_updated = models.DateTimeField(auto_now=True)
    value = models.DecimalField(decimal_places=2, max_digits=200)

    @property
    def day_change(self):
        snap = Snapshot.objects.filter(portfolio=self).order_by("-created")[1:2].first()
        if not snap:
            return None
        return round((self.value - snap.value), 2)

    @property
    def day_perc_change(self):
        snap = Snapshot.objects.filter(portfolio=self).order_by("-created")[1:2].first()
        if not snap:
            return None
        return round(((self.value - snap.value) / snap.value) * 100, 2)

    @property
    def total_change(self):
        start_value = self.league.start_value
        return round((self.value - start_value), 2)

    @property
    def total_perc_change(self):
        start_value = self.league.start_value
        return round(((self.value - start_value) / start_value) * 100, 2)

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
    last_updated = models.DateTimeField(auto_now=True)
    quantity = models.DecimalField(decimal_places=6, max_digits=200)
    previous_close = models.DecimalField(decimal_places=2, max_digits=200, default=0)

    @property
    def total_value(self):
        if self.is_currency:
            return self.value
        return self.value * self.quantity

    @property
    def day_change(self):
        return round((self.value - self.previous_close), 2)

    @property
    def day_perc_change(self):
        if self.previous_close == 0:
            return 0
        return round(
            ((self.value - self.previous_close) / self.previous_close) * 100, 2
        )

    def __str__(self):
        return f"{self.portfolio.name} has {self.quantity} {self.ticker}"


class FollowAsset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

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
    quantity = models.DecimalField(decimal_places=6, max_digits=200)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_value(self):
        return self.value * self.quantity

    def __str__(self):
        return f"{self.portfolio.name} bought {self.quantity} {self.ticker}"
