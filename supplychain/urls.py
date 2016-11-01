from django.conf.urls import url, include
from django.contrib.auth.views import logout_then_login
from . import views

urlpatterns = [
    url(r'^$', views.helloLoginView.as_view(), name='helloLogin'),
    url(r'^login$', views.LoginView.as_view(), name='login'),
    url(r'^dashboard$', views.dashboard.as_view(), name='dashboard'),
    url(r'^logout$', logout_then_login, name='logout'),
    url(r'^', include(views.dashboard.dashboard_urls)),
]
