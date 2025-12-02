# portfolios/views.py
from decimal import Decimal
import json

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .forms import InvestmentForm
from .models import Investment


@login_required
def portfolio_list(request):
    """
    Main portfolio page:
    - Lists investments
    - Provides search & type filter
    - Shows totals & profit/loss
    - Provides data for the Chart.js chart
    """
    investments = Investment.objects.filter(user=request.user)

    # --- Search ---
    search = request.GET.get("search", "").strip()
    if search:
        investments = investments.filter(name__icontains=search)

    # --- Filter by type ---
    filter_type = request.GET.get("type", "").strip()
    if filter_type:
        investments = investments.filter(investment_type__iexact=filter_type)

    # --- Totals ---
    total_invested = (
        investments.aggregate(total=Sum("amount_invested"))["total"]
        or Decimal("0")
    )
    total_current = (
        investments.aggregate(total=Sum("current_value"))["total"]
        or Decimal("0")
    )
    profit = total_current - total_invested

    # --- Chart data (simple: each investment's current value) ---
    labels = list(investments.values_list("name", flat=True))
    values = list(investments.values_list("current_value", flat=True))
    values = [float(v) for v in values]  # make JSON serializable

    context = {
        "investments": investments.order_by("-date_added"),
        "total_invested": total_invested,
        "total_current": total_current,
        "profit": profit,
        "chart_labels": json.dumps(labels),
        "chart_values": json.dumps(values),
    }
    return render(request, "portfolios/portfolio_list.html", context)


@login_required
def add_investment(request):
    if request.method == "POST":
        form = InvestmentForm(request.POST)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.user = request.user
            inv.save()
            return redirect("portfolio_list")
    else:
        form = InvestmentForm()

    return render(request, "portfolios/add_investment.html", {"form": form})


@login_required
def edit_investment(request, id):
    investment = get_object_or_404(Investment, id=id, user=request.user)

    if request.method == "POST":
        form = InvestmentForm(request.POST, instance=investment)
        if form.is_valid():
            form.save()
            return redirect("portfolio_list")
    else:
        form = InvestmentForm(instance=investment)

    return render(request, "portfolios/edit_investment.html", {"form": form, "investment": investment})


@login_required
def delete_investment(request, id):
    investment = get_object_or_404(Investment, id=id, user=request.user)
    investment.delete()
    return redirect("portfolio_list")


@login_required
def portfolio_home(request):
    return render(request, "portfolios/portfolio_home.html")


@login_required
def edit_portfolio(request):
    return render(request, "portfolios/edit_portfolio.html")
