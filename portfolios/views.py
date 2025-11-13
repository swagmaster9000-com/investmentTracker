
# Create your views here.
# from django.shortcuts import render, redirect
# from .models import Investment
# from .forms import InvestmentForm

# def portfolio_view(request):
#     investments = Investment.objects.filter(user=request.user)
#     total_value = sum(i.total_value for i in investments)
#     return render(request, 'portfolios/portfolio.html', {
#         'investments': investments,
#         'total_value': total_value,
#     })

# def add_investment(request):
#     if request.method == 'POST':
#         form = InvestmentForm(request.POST)
#         if form.is_valid():
#             investment = form.save(commit=False)
#             investment.user = request.user
#             investment.save()
#             return redirect('portfolio')
#     else:
#         form = InvestmentForm()
#     return render(request, 'portfolios/add_investment.html', {'form': form})


from django.shortcuts import render, redirect
from .forms import InvestmentForm
from .models import Investment

def add_investment(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect if user is not logged in

    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            investment = form.save(commit=False)
            investment.user = request.user  # Link to the logged-in user
            investment.save()
            return redirect('portfolio')  # Redirect to a portfolio overview page
    else:
        form = InvestmentForm()
    
    return render(request, 'portfolios/add_investment.html', {'form': form})


def portfolio_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    investments = Investment.objects.filter(user=request.user)
    return render(request, 'portfolios/portfolio.html', {'investments': investments})
