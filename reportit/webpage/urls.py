from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', views.home, name = 'home'),
    url(r'^reporterSignup$', views.reporterSignup, name = 'reporterSignup'),
    url(r'^accounts/profile/', views.viewProfile, name = 'profile'),
    url(r'^account/dashboard', views.dashboard, name = 'dashboard'),
]