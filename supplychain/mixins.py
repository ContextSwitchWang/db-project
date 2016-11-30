from django.contrib.auth.mixins import PermissionRequiredMixin
from utils import get_permission_codename
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext as _
from . import models
from django.contrib.auth.models import Permission

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

def perm_exists(model, perm):
    try:
        Permission.objects.get(codename="%s_%s" % (perm, model._meta.model_name))
        return True
    except:
        return False
class dashboardItemsMixin(object):
    """ add dashboard items and urls to web page  """
    items = [
        item(_('User Management'), _('View or Edit User'), _("You can add, edit or delete users and their attributes here."), '/users/', User),
        item(_('Group Management'), _('View or Edit Group'), _("You can add, edit or delete groups and their attributes here."), '/groups/', Group),
        item(_('Companys'), _('View or Edit Companys'), _("You can add, edit or delete companys and their attributes here."), '/companys/', models.Company),
        item(_('Bet'), _('Bet Here!'), _("You can Bets here"), '/bets/', models.Bet),
        item(_('Bet'), _('Bet Here!'), _("You can Bets here"), '/counts/', models.CountModel),
    ]
    def get_context_data(self, **kwargs):
        context = super(dashboardItemsMixin, self).get_context_data(**kwargs)
        perms = [get_permission_codename(item.model, 'view') for item in self.items]
        context['item_list'] = [item for i,item in enumerate(self.items) if not perm_exists(item.model, 'view') or self.request.user.has_perm(perms[i])]
        return context
