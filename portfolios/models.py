from django.db import models
from django.contrib.auth.models import User


INVESTMENT_CHOICES = (
    ('MMA', 'Money Market Account'),
    ('LI', 'Life Insurance'),
    ('BTC', 'Bitcoin'),
    ('STK', 'Stock'),
    # Add more types as needed
)

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=12, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=3, choices=INVESTMENT_CHOICES)

    def __str__(self):
        return f"{self.name} - ${self.value}"
