from django.urls                                                    import path

from .views                                                         import store,  cart, \
                                                                    updateitem, checkout#, remove_from_cart

app_name = "store"

urlpatterns = [

    path('',                                            store,              name="home"),
    path('cart/',                                       cart,               name="cart"),
    path('update/',                                     updateitem,         name="update"),
    path('checkout/',                                   checkout,           name="checkout"),
    #path('remove_from_cart/<pk>/',                                   remove_from_cart,           name="remove_from_cart"),
]