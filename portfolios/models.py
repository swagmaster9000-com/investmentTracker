from django.db import models
from django.conf import settings

class Investment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    investment_type = models.CharField(max_length=50)  # e.g., Stock, Crypto, Bond
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} (${self.amount_invested})"
