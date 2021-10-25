from django.contrib.auth                                import views as auth_views

from django.conf.urls.static                            import static
from django.contrib                                     import admin
from django.conf                                        import settings
from django.urls                                        import path, include


urlpatterns = [
    path('',                                    include('pcshop.apps.web.urls')),
]

if settings.DEBUG:

    import debug_toolbar

    urlpatterns = [

        path('mpoyi-admin/',                              admin.site.urls),
        path('__debug__/',                          include(debug_toolbar.urls)),

    ] + urlpatterns

    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static( settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)