from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^login/$', auth_views.login, name='login'),
    url(r'^login/$', auth_views.login, {'template_name': 'webpage/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^$', views.home, name = 'home'),
    url(r'^reporterSignup/$', views.reporterSignup, name = 'reporterSignup'),
    url(r'^agentSignup/$', views.agentSignup, name = 'agentSignup'),
    url(r'^account/profile/$', views.viewProfile, name = 'profile'),
    url(r'^account/dashboard/$', views.dashboard, name = 'dashboard'),
    url(r'^account/profile/$', views.viewProfile, name = 'profile'),
    url(r'^account/submitConcern/', views.submitConcern, name = 'submitConcern'),

	url(r'^account/dashboard$', views.dashboard, name = 'dashboard'),
    url(r'^account$', views.dashboard, name = 'dashboard'),
    url(r'^.*$', views.notFound, name = '404notFound'),
]