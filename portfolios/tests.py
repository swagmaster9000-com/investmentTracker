from django.test import TestCase

# Create your tests here.
from django.shortcuts import render, redirect
from .models import Investment

def add_investment(request):
    if request.method == 'POST':
        symbol = request.POST['symbol'].upper()
        shares = float(request.POST['shares'])
        purchase_price = float(request.POST['purchase_price'])

        Investment.objects.create(
            user=request.user,
            symbol=symbol,
            shares=shares,
            purchase_price=purchase_price
        )
        return redirect('dashboard')

    return render(request, 'tracker/add_investment.html')


def dashboard(request):
    investments = Investment.objects.filter(user=request.user)
    return render(request, 'tracker/dashboard.html', {'investments': investments})
