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

class dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'supplychain/dashboard.html'

class objectsViewPermissionMixin(PermissionRequiredMixin):
    """ use with PermissionRequiredMixin """
    def get_permission_codename(self, perm):
       return "%s.%s_%s" % (self.model._meta.app_label, perm, self.model._meta.model_name)
    def get_permission_required(self):
        return (self.get_permission_codename('view'),)

class ModelAllViews(object):
    """ generate views for listing, add and update """
    def __init__(self, model, fields=None):
        super(ModelAllViews, self).__init__()
        self.model = model
        self.opts = model._meta
        class displayView(objectsViewPermissionMixin, PermissionRequiredMixin, generic.ListView):
            """ a class that should be general and work on all kinds of models  
                display all objects line by line, with delete functionality"""
            def post(self, request):
                try:
                    pk = request.POST['delete']
                    obj = self.model.objects.get(pk=pk)
                    obj.delete()
                except KeyError:
                    return HttpResponse('invalid argument')
                return HttpResponse('successful')
        
        class updateView(objectsViewPermissionMixin, PermissionRequiredMixin, generic.UpdateView):
            """ update page """
            pass
        
        class createView(objectsViewPermissionMixin, PermissionRequiredMixin, generic.CreateView):
            """ update page """
            pass

        fields = fields if fields else '__all__'
        def get_absolute_url(self):
            from django.core.urlresolvers import reverse
            return reverse('%s_%s_update' % (self._meta.app_label, self._meta.model_name), kwargs={'pk':str(self.pk)})
        self.model.get_absolute_url = get_absolute_url
        self.updatecls = type("%s_update_view" % self.opts.model_name, 
                    (updateView,), 
                    dict(model=self.model, 
                        template_name=self.get_update_template_name(), 
                        fields=fields))

        self.createcls = type("%s_create_view" % self.opts.model_name, 
                    (createView,), 
                    dict(model=self.model, 
                        template_name=self.get_create_template_name(), 
                        fields=fields))
        self.displaycls = type("%s_display_view" % self.opts.model_name, 
                    (displayView,), 
                    dict(model=self.model, template_name=self.get_template_name()))
    def get_template_name(self):
        return "supplychain/%s_display.html" % self.opts.model_name
    def get_update_template_name(self):
        return "supplychain/%s_update.html" % self.opts.model_name
    def get_create_template_name(self):
        return "supplychain/%s_create.html" % self.opts.model_name
    def get_model(self):
        return self.model
    def get_urls(self):
        from django.conf.urls import url
        info = self.opts.app_label, self.opts.model_name
        urlpatterns = [
            url(r'^$', self.displaycls.as_view(), name='%s_%s_displaylist' % info),
            url(r'^create/$', self.createcls.as_view(), name='%s_%s_create' % info),
            url(r'^(?P<pk>.+)/update/$', self.updatecls.as_view(), name='%s_%s_update' % info),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()

# generate our models here
userAllView = ModelAllViews(User)
