# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.conf import settings
from django.db import models
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.conf.urls import url
from django import forms
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
# Create your models here.

#Informative relations: which is basicly static
#Include the Company, Inventory, (Item) Catalog, Account,
#Note: SITE for Inventory, subcatagory for catalog not implement
class Company(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 200)
    #C_ET ???
    address = models.CharField(max_length = 200)
    phone = models.CharField(max_length = 20)
    contact = models.CharField(max_length = 200)
    notes = models.CharField(max_length = 200)

    DISTRIBUTOR = 'DISTRIBUTOR'
    SUPPLIER = 'SUPPLIER'
    MANUFACTURER = 'MANUFACTURER'
    company_type = (
        (DISTRIBUTOR, 'DISTRIBUTOR'),
        (SUPPLIER, 'SUPPLIER'),
        (MANUFACTURER, 'MANUFACTURER'),
    )
    companytype = models.CharField(max_length = 20, choices = company_type, default = DISTRIBUTOR)



class Inventory(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 200)
    size = models.IntegerField()
    price = models.FloatField()
    address = models.CharField(max_length = 200)

class Catalog(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 200)
    unit_price = models.FloatField()
    spec = models.CharField(max_length = 200)
    size = models.FloatField()
    PRODUCT = 'PRODUCT'
    COMPONENT = 'COMPONENT'
    catalog_type = (
        (PRODUCT, 'PRODUCT'),
        (COMPONENT, 'COMPONENT'),
    )
    catalogtype = models.CharField(max_length = 20, choices = catalog_type, default = PRODUCT)

class Account(models.Model):
    id = models.AutoField(primary_key = True)
    bank = models.CharField(max_length = 200)
    bill_address = models.CharField(max_length = 200)
    #may need add constrain for this kind of information
    rounting_number = models.CharField(max_length = 20)
    account_number = models.CharField(max_length = 20)
    account_owner = models.CharField(max_length = 200)
    #Not quite sure is company a foreign key of company, what about myself
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    notes = models.CharField(max_length = 200)

#Key relations: Order, Item, Transaction, Order_Item list
class Order(models.Model):
    id = models.AutoField(primary_key = True)
    #
    date = models.DateField(auto_now_add = True)
    price = models.FloatField()
    #foreign Key - the supply or distribute company
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    notes = models.CharField(max_length = 200)
    BUYIN = 'BUYIN'
    SELLOUT = 'SELLOUT'
    order_type = (
        (BUYIN, 'BUYIN'),
        (SELLOUT, 'SELLOUT'),
    )
    ordertype = models.CharField(max_length = 20, choices = order_type, default = BUYIN)


class Item(models.Model):
    #SN is id
    id = models.AutoField(primary_key = True)

    UNAVAILABLE = 'UNAVAILABLE'
    AVAILABLE = 'AVAILABLE'
    ITEM_STATE = (
        (UNAVAILABLE , 'UNAVAILABLE'),
        (AVAILABLE, 'AVAILABLE'),
    )
    state = models.CharField(max_length = 20, choices = ITEM_STATE, default = AVAILABLE)

    catalog = models.ForeignKey(Catalog, on_delete=models.CASCADE)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    notes = models.CharField(max_length = 200)

class Transaction(models.Model):
    id = models.AutoField(primary_key = True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    fr_account = models.ForeignKey(Account, related_name="%(class)s_fr_related", on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name="%(class)s_to_related", on_delete=models.CASCADE)
    #cash_oh = models.FloatField()
    #cash_ib = models.FloatField()
    amount = models.FloatField()
    UNSTART = 'UNSTART'
    PENDING = 'PENDING'
    COMPELTED = 'COMPELTED'
    TRANSACTION_STATE = (
        (UNSTART, 'UNSTART'),
        (PENDING, 'PENDING'),
        (COMPELTED, 'COMPELTED'),
    )
    state = models.CharField(max_length = 20, choices = TRANSACTION_STATE, default = UNSTART)
    notes = models.CharField(max_length = 200)

class Order_Item(models.Model):
    order_id = models.ForeignKey(Order, on_delete = models.CASCADE)
    item_id = models.ForeignKey(Item, on_delete = models.CASCADE)

#End of all relations
#Create views include:
#capital report:
"""capital report:
looks like:
accout1 money_in money_out  balance
accout2 money_in money_out  balance
"""
#order report:
"""active order report:
looks like:
order1 order_type(buy or sell) item_state capital_state(should pay) (acually pay)
order2 item_state capital_state
"""

"""inventory report:
looks like:
catagory1 inventory1 number
catagory1 inventory2 number
catagory2 inventory1 number
catagory2 inventory2 number
"""

class Bet(models.Model):
    class Meta:
        default_permissions = []
    created_by = models.OneToOneField(
            settings.AUTH_USER_MODEL,
            on_delete=models.CASCADE,
            primary_key=True
            )
    HI = 'HI'
    TR = 'TR'
    BET_CHOICES = (
            (HI, 'Hillary'),
            (TR, 'Trump'))
    bet = models.CharField(
            max_length = 2,
            choices=BET_CHOICES)

class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['bet']

class BetView(FormView):
    template_name = 'supplychain/bet.html'
    form_class = BetForm
    success_url = '/thanks/'
    bet = None
    raise_exception = True
    def getOdds(self):
        bet = Bet.objects.get(created_by=self.request.user)
        total = Bet.objects.count()
        your = Bet.objects.filter(bet=bet.bet).count()
        if total != 0:
            return  your / total
        else:
            return 'No count Now!'

    def form_valid(self, form):
        newbet = form.save(commit=False)
        newbet.created_by = self.request.user
        self.bet = newbet.bet
        newbet.save()
        return redirect('bets_display')

class BetUrls(object):
    urls = urlpatterns = [
            url(r'^$', login_required(BetView.as_view()), name='bets_display'),
        ]

class CountModel(models.Model):
    class Meta:
        default_permissions = []
    created_by = models.CharField(
            max_length = 20,
            primary_key=True
            )
    BET_CHOICES = (
            ('A', 'A建议'),
            ('B', 'B单独开群'),
            ('C', 'C不建议'),
            ('D', 'D无所谓'),
            )
    choice = models.CharField(
            max_length = 2,
            choices=BET_CHOICES)

class CountModelForm(forms.ModelForm):
    class Meta:
        model = CountModel
        fields = ['choice', 'created_by']

class CountModelView(FormView):
    template_name = 'supplychain/count.html'
    form_class = CountModelForm
    def getCounts(self):
        return CountModel.objects.all().values('choice').annotate(total=Count('choice'))

    def form_valid(self, form):
        new = form.save(commit=True)
        return redirect('counts_display')

class BetUrls(object):
    urls = urlpatterns = [
            url(r'^$', login_required(BetView.as_view()), name='bets_display'),
        ]

class CountUrls(object):
    urls = urlpatterns = [
            url(r'^$', CountModelView.as_view(), name='counts_display'),
        ]

class Status(models.Model):
    pass
