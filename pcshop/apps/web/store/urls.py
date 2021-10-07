from django.urls                                                    import path

from .views                                                         import store,  cart, \
                                                                    updateitem, checkout, processOrder

app_name = "store"

urlpatterns = [

    path('',                                            store,              name="home"),
    path('cart/',                                       cart,               name="cart"),
    path('update/',                                     updateitem,         name="update"),
    path('checkout/',                                   checkout,           name="checkout"),
    path('process_order/',                              processOrder,       name="process_order"),



]