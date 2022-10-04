from django.urls import path

from stock.views import stock_list


urlpatterns = [
    path('list/', stock_list)
]