from django.contrib import admin

# Register your models here.
# portfolios/admin.py


from .models import Investment # Import your Investment model

# Register your model with the admin site
admin.site.register(Investment)