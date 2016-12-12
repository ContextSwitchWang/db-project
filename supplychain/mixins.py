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
        item(_('Status'), _('View Status'), _("You can view the status of your business here."), '/status/', models.Status),
        item(_('User Management'), _('View or Edit User'), _("You can add, edit or delete users and their attributes here."), '/users/', User),
        item(_('Group Management'), _('View or Edit Group'), _("You can add, edit or delete groups and their attributes here."), '/groups/', Group),

        item(_('Companys'), _('View or Edit Companys'), _("You can add, edit or delete companys and their attributes here."), '/companys/', models.Company),
        item(_('Inventory'), _('View or Edit Inventory'), _("You can add, edit or delete Inventory and their attributes here."), '/Inventory/', models.Inventory),
        item(_('Catalog'), _('View or Edit Catalog'), _("You can add, edit or delete Catalog and their attributes here."), '/Catalog/', models.Catalog),
        item(_('Account'), _('View or Edit Account'), _("You can add, edit or delete Account and their attributes here."), '/Account/', models.Account),
        item(_('Order'), _('View or Edit Order'), _("You can add, edit or delete Order and their attributes here."), '/Order/', models.Order),
        item(_('Transaction'), _('View or Edit Transaction'), _("You can add, edit or delete Transaction and their attributes here."), '/Transaction/', models.Transaction),
        item(_('Order_Item'), _('View or Edit Order_Item'), _("You can add, edit or delete Order_Item and their attributes here."), '/OrderItem/', models.Order_Item),
        item(_('Item'), _('View or Edit Item'), _("You can add, edit or delete Item and their attributes here."), '/Item/', models.Item),

        item(_('Bet'), _('Bet Here!'), _("You can Bets here"), '/bets/', models.Bet),
        item(_('Bet'), _('Bet Here!'), _("You can Bets here"), '/counts/', models.CountModel),
    ]
    def get_context_data(self, **kwargs):
        context = super(dashboardItemsMixin, self).get_context_data(**kwargs)
        perms = [get_permission_codename(item.model, 'view') for item in self.items]
        context['item_list'] = [item for i,item in enumerate(self.items) if not perm_exists(item.model, 'view') or self.request.user.has_perm(perms[i])]
        return context
