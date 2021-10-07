from django.contrib import admin

from .models import OrderItem, Product, Order, ShippingAddress, GetInTouch, Staff
# Register your models here.


admin.site.register([OrderItem, Product, Order, ShippingAddress, GetInTouch, Staff])