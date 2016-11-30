from mixins import objectsViewPermissionMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic
from django.contrib.auth.models import User
from mixins  import dashboardItemsMixin
from django.template.loader  import TemplateDoesNotExist, get_template
from django.http import HttpResponse
class displayView(dashboardItemsMixin, objectsViewPermissionMixin, PermissionRequiredMixin, generic.ListView):
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

class updateView(dashboardItemsMixin, objectsViewPermissionMixin, PermissionRequiredMixin, generic.UpdateView):
    """ update page """
    pass

class createView(dashboardItemsMixin, objectsViewPermissionMixin, PermissionRequiredMixin, generic.CreateView):
    """ update page """
    pass

class ModelAllViews(object):
    """ generate views for listing, add and update """
    def __init__(self, model, fields=None):
        super(ModelAllViews, self).__init__()
        self.model = model
        self.opts = model._meta
        model_name = self.opts.verbose_name.title()

        fields = fields if fields else '__all__'
        def get_absolute_url(self):
            from django.core.urlresolvers import reverse
            return reverse('%s_%s_update' % (self._meta.app_label, self._meta.model_name), kwargs={'pk':str(self.pk)})
        self.model.get_absolute_url = get_absolute_url
        self.updatecls = type("%s_update_view" % self.opts.model_name, 
                    (updateView,), 
                    dict(model=self.model, 
                        template_name=self.get_template_name('update'), 
                        fields=fields,
                        model_name=model_name))

        self.createcls = type("%s_create_view" % self.opts.model_name, 
                    (createView,), 
                    dict(model=self.model, 
                        template_name=self.get_template_name('create'), 
                        fields=fields))
        self.displaycls = type("%s_display_view" % self.opts.model_name, 
                    (displayView,), 
                    dict(model=self.model,
                        template_name=self.get_template_name('display'),
                        model_name=model_name,
                        opts=self.opts))
    def get_template_name(self, view):
        name = "supplychain/%s_%s.html" % (self.opts.model_name, view)
        try: 
            get_template(name)
            return name
        except TemplateDoesNotExist:
            return "supplychain/object_%s.html" % view
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
