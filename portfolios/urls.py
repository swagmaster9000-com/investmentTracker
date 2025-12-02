# portfolios/urls.py
from django.urls import path
from rest_framework import routers

from . import views
from .api import InvestmentAPI

urlpatterns = [
    path("", views.portfolio_list, name="portfolio_list"),
    path("add/", views.add_investment, name="add_investment"),
    path("edit/<int:id>/", views.edit_investment, name="edit_investment"),
    path("delete/<int:id>/", views.delete_investment, name="delete_investment"),
    path("home/", views.portfolio_home, name="portfolio_home"),
    path("edit-portfolio/", views.edit_portfolio, name="edit_portfolio"),
]

# DRF router for API (for TDD / tests later)
router = routers.DefaultRouter()
router.register("api/investments", InvestmentAPI, basename="api-investments")

urlpatterns += router.urls
