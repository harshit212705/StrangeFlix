# importing django modules
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static


# defining url routes and corresponding files to be included
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    # url(r'^accounts/',include('allauth.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('accounts/', include('accounts.urls')),
    path('subscribe/', include('subscribe.urls')),
    path('transaction/', include('transaction.urls')),
    path('provider/', include('provider.urls')),
    path('room/',include('room.urls')),
    path('admin/',include('Admin.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)
