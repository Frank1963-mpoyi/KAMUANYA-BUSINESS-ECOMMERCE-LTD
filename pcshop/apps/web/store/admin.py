from django.contrib import admin

from .models import OrderItem, Product, Order, ShippingAddress
# Register your models here.


admin.site.register([OrderItem, Product, Order, ShippingAddress])