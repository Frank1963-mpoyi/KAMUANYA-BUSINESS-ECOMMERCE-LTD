from django.contrib.auth                                import views as auth_views

from django.conf.urls.static                            import static
from django.contrib                                     import admin
from django.conf                                        import settings
from django.urls                                        import path, include


urlpatterns = [
    path('',                    include("store.urls")),
    path('admin/',              admin.site.urls),
   # path('accounts/', include('allauth.urls')),

]

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)