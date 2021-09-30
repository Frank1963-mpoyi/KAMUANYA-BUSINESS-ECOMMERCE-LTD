from django.contrib import admin

from .models import OrderItem, Product, Order
# Register your models here.


admin.site.register([OrderItem, Product, Order])