# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from django.conf import settings
from django.db import models
from django.views.generic.edit import FormView
from django.conf.urls import url
from django import forms
from django.shortcuts import redirect
from django.db.models import Count
from django.contrib.auth.decorators import login_required, permission_required
# Create your models here.
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
