from django.contrib import admin
from market.models import Market, Product, Redirect
# Register your models here.

admin.site.register(Market)
admin.site.register(Product)
admin.site.register(Redirect)