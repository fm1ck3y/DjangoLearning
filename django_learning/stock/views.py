from django.shortcuts import render, get_object_or_404, redirect
from stock.models import Stock, AccountCurrency, AccountStock
from stock.forms import BuySellForm
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

def stock_list(request):
    stocks = Stock.objects.all()
    context = {
        'stocks': stocks,
    }
    return render(request, 'stocks.html', context)

@login_required
def stock_detail(request, pk):
    stock = get_object_or_404(Stock, pk=pk)
    random_price = stock.get_random_price()
    context = {
        'stock': stock,
        'form_sell': BuySellForm(initial={'price': random_price}),
        'form_buy': BuySellForm(initial={'price': random_price})
    }
    return render(request, 'stock.html', context)

@login_required
def stock_buy(request, pk):
    if request.method != "POST":
        return redirect('stock:detail', pk=pk)

    stock = get_object_or_404(Stock, pk=pk)
    form = BuySellForm(request.POST)

    if form.is_valid():
        amount = form.cleaned_data['amount']
        price = form.cleaned_data['price']

        acc_currency, created = AccountCurrency.objects.get_or_create(account=request.user.account, currency=stock.currency,
                                                                      defaults={'amount': 0})
        if not acc_currency.buy(amount, price, stock):
            form.add_error(None, f'На счёте недостаточно средств в валюте {stock.currency.sign}')
        else:
            return redirect('stock:list')

    context = {
        'stock': get_object_or_404(Stock, pk=pk),
        'form_sell': BuySellForm(initial={'price': form.cleaned_data['price']}),
        'form_buy': form
    }

    return render(request, 'stock.html', context)

@login_required
def stock_sell(request, pk):
    if request.method != "POST":
        return redirect('stock:detail', pk=pk)

    stock = get_object_or_404(Stock, pk=pk)
    form = BuySellForm(request.POST)

    if form.is_valid():
        amount = form.cleaned_data['amount']
        price = form.cleaned_data['price']
        
        acc_currency, created = AccountCurrency.objects.get_or_create(account=request.user.account, currency=stock.currency,
                                                                      defaults={'amount': 0})
        if not acc_currency.sell(amount, price, stock):
            form.add_error(None, f'Вы ввели неверное количество продаваемой акции или у вас недостаточно акций для продажи.')
        else:
            return redirect('stock:list')

    context = {
        'stock': get_object_or_404(Stock, pk=pk),
        'form_buy': BuySellForm(initial={'price': form.cleaned_data['price']}),
        'form_sell': form
    }

    return render(request, 'stock.html', context)

@login_required
def account(request):
    currencies = cache.get(f'currencies_{request.user.username}')
    stocks = cache.get(f'stocks_{request.user.username}')

    if currencies is None:
        print(currencies)
        currencies = [
            {
                'amount': acc_currency.amount,
                'sign': acc_currency.currency.sign
            } for acc_currency in request.user.account.accountcurrency_set.select_related('currency')
        ]
        cache.set(f'currencies_{request.user.username}', currencies, 300)

    if stocks is None:
        stocks = [
            {
                'ticker': acc_stock.stock.ticker,
                'amount': acc_stock.amount,
                'avg': acc_stock.average_buy_cost
            } for acc_stock in request.user.account.accountstock_set.select_related('stock').all()
        ]
        cache.set(f'stocks_{request.user.username}', stocks, 300)

    context = {
        'currencies': currencies,
        'stocks': stocks
    }

    return render(request, template_name='account.html', context=context)