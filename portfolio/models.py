from django.db import models
from django.contrib.auth.models import User


class League(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    start_value = models.DecimalField(decimal_places=0, max_digits=200)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

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
    value = models.DecimalField(decimal_places=2, max_digits=200)

    def save(self, *args, **kwargs):
        self.value = self.league.start_value
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name}"


class Asset(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    is_currency = models.BooleanField(default=False)
    ticker = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=200)
    quantity = models.IntegerField()
    total_value = models.DecimalField(
        decimal_places=2, max_digits=200, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.total_value = self.value * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.portfolio.name} has {self.quantity} {self.ticker}"


class Transaction(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    is_purchase = models.BooleanField(default=False)
    ticker = models.CharField(max_length=200)
    value = models.DecimalField(decimal_places=2, max_digits=200)
    quantity = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    total_value = models.DecimalField(
        decimal_places=2, max_digits=200, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        self.total_value = self.value * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.portfolio.name} bought {self.quantity} {self.ticker}"
