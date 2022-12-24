"""dndwebsite URL Configuration """
from django.urls import path

import django.contrib.auth.views as auth_views

from . import views

urlpatterns = [
    path('login', views.loginView, name='login'),
    path('profile', views.accountView, name='account'),
    path('logout', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout'),
    path('create-account', views.createAccountView, name='create_account'),
    # TODO: Catch-all redirect to profile for account/ paths
]
