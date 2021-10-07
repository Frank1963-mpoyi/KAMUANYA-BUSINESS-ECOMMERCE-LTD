from django.urls                                        import path, include


urlpatterns = [
    path('',                                    include('pcshop.apps.web.store.urls')),
    path('accounts/',                           include('pcshop.apps.web.accounts.urls')),
]
