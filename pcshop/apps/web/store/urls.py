from django.urls import path

from .views import HomeView, AddToCartView, UpdateItemView, CheckoutView, \
                        ProcessOrderView, ContactView, AboutView, search_view

app_name = "store"

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('cart/', AddToCartView.as_view(), name="cart"),
    path('update/', UpdateItemView.as_view(), name="update"),
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path('process_order/', ProcessOrderView.as_view(), name="process_order"),
    path('contact/', ContactView.as_view(), name="contact"),
    path('about/', AboutView.as_view(), name="about"),
    path('search/', search_view, name="search"),
]