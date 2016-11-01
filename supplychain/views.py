from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import classonlymethod
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.models import BaseUserManager, User
from django.http import HttpResponse
from django.contrib.admin import ModelAdmin
import logging
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views import generic
from django.views.generic.base import TemplateView
from django.db import models
from utils import get_permission_codename
from mixins  import item, dashboardItemsMixin
from options import ModelAllViews

class helloLoginView(TemplateView):
    """ display the login page """
    template_name = 'supplychain/helloLogin.html'
    @property
    def guest(self):
        guest = settings.GUEST_LOGIN
        return authenticate(username=guest)
        
class LoginView(helloLoginView):
    """ display the login page on get, accept login on post """
    def post(self, request):
        user_name = request.POST['user_name']
        user_pass = request.POST['user_pass']
        logging.info("Login Attempt by " + user_name )
        user = authenticate(username=user_name, password=user_pass)
        if user:
            login(request, user)
            return HttpResponse('successful')
        else:
            return HttpResponse('invalid login/password')

class dashboard(dashboardItemsMixin, LoginRequiredMixin, TemplateView):
    template_name = 'supplychain/dashboard.html'
    dashboard_items = dashboardItemsMixin.dashboard_items
    from django.conf.urls import url, include
    dashboard_models = [ ModelAllViews(item.model) for item in dashboard_items]
    dashboard_urls = [url(item.url[1:], include(dashboard_models[i].urls)) for i, item in enumerate(dashboard_items)]
