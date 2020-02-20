from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from web.core.views import HomePageView
from web.health.views import health_default, health_db
from web.users.views import generic_logout


urlpatterns = [

    path('', HomePageView.as_view(), name='home'),

    path('health', health_default),
    path('omslagroute/health', health_default),
    path('omslagroute/health-db', health_db),

    path('documenten/', include('web.documents.urls')),

    path('uitloggen/', generic_logout, name='uitloggen'),

    path('admin/', admin.site.urls),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
