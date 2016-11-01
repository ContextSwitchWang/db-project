from django.contrib.auth.mixins import PermissionRequiredMixin
from utils import get_permission_codename
from django.contrib.auth.models import User

class objectsViewPermissionMixin(PermissionRequiredMixin):
    """ use with PermissionRequiredMixin """
    def get_permission_required(self):
        return (get_permission_codename(self.model, 'view'),)

class item(object):
    """ represent a dashbaord item """
    def __init__(self, name, short_desc, description, url, model):
        self.name = name
        self.short_desc = short_desc
        self.description = description
        self.url = url
        self.model = model

class dashboardItemsMixin(object):
    dashboard_items = [
        item('User Management', 'View or Edit user', "You can add, edit or delete users and their roles here.", '/users/', User),
    ]
    def get_context_data(self, **kwargs):
        context = super(dashboardItemsMixin, self).get_context_data(**kwargs)
        context['item_list'] = [item for item in self.dashboard_items if self.request.user.has_perm(get_permission_codename(item.model, 'view'))]
        return context
