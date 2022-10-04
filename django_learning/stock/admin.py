from django.contrib import admin
from stock.models import Stock, Currency

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("ticker", "name", "description")

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

# Register your models here.
