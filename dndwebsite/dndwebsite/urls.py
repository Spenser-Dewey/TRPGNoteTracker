"""dndwebsite URL Configuration """
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('campaign-info/', include('campaign_info.urls'), name='campaign_info'),
    path('accounts/', include('user_info.urls'), name='accounts'),
    path('', RedirectView.as_view(url = 'accounts/profile', permanent = False), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
