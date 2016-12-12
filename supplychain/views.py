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
from utils import get_permission_codename
from mixins  import item, dashboardItemsMixin
from options import ModelAllViews
from django.contrib.auth.models import User, Group
from . import models
from . import utils
from django.conf.urls import url
import django.db.models.aggregates as agg
from django.db.models import Case, Value, When, F
        

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
    """ the dashboard page """
    template_name = 'supplychain/dashboard.html'

class StatusView(dashboardItemsMixin, TemplateView):
    template_name = 'supplychain/status.html'

    def volume(self):
        return utils.addDollarSign(models.Order.objects.aggregate(agg.Sum('price'))['price__sum'])

    def all_company_balance(self):
        cs = models.Order.objects.values_list('company__name')
        bs = cs.annotate(balance=agg.Sum(
        Case(When(ordertype=models.Order.BUYIN, then=F('price') * -1),
             When(ordertype=models.Order.SELLOUT, then='price'),
            )))
        return [(b[0], utils.addDollarSign(b[1])) for b in bs]
    def all_inventory_count(self):
        return models.Item.objects.values_list('inventory__name').annotate(
                agg.Count('id'))

class StatusUrls(object):
    urls = urlpatterns = [
            url(r'^$', StatusView.as_view(), name='status'),
        ]

class dashboardItems(object):
    """ generate urls and models """
    items = dashboardItemsMixin.items
    from django.conf.urls import url, include
    ItemModels =  [StatusUrls] + [ModelAllViews(model) for model in [User, Group,\
                        models.Company, models.Inventory, models.Catalog, models.Account,\
                        models.Order, models.Transaction, models.Order_Item \
                        , models.Item, ]] \
                + [models.BetUrls, models.CountUrls ]
    urls = [url(item.url[1:], include(ItemModels[i].urls)) for i, item in enumerate(items)]
