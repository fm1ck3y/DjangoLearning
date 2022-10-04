from django.db import models
from django.contrib.auth.models import User
import random

class Stock(models.Model):
    name = models.CharField(max_length=40)
    ticker = models.CharField(max_length=4, default="NULL")
    description = models.TextField(null=True, blank=True)
    currency = models.ForeignKey('Currency', null=True, on_delete=models.SET_NULL)
    logo = models.ImageField(null=True, blank=True)

    def get_random_price(self):
        return random.randint(0, 3000)

    def __str__(self):
        return f"{self.ticker}"

class Currency(models.Model):
    name = models.CharField(max_length=40)
    ticker = models.CharField(max_length=4)
    sign = models.CharField(max_length=1)

    def __str__(self):
        return self.sign


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class AccountCurrency(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    class Meta:
        unique_together = ['account', 'currency']

    def __str__(self):
        return f'{self.account.user.username} {self.currency.sign}'

class AccountStock(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    average_buy_cost = models.DecimalField(null=True, blank=True, decimal_places=2, max_digits=6)

    class Meta:
        unique_together = ['account', 'stock']

    def __str__(self):
        return f'{self.account.user.username} {self.stock.ticker}'
