from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_migrate

def add_view_permissions(sender, **kwargs):
    """
    Adding a view permission too all our 
    content types.
    """

    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission

    # for each of our content types
    for content_type in ContentType.objects.all():
        if not content_type._meta.default_permissions:
            continue
        # build our permission slug
        codename = "view_%s" % content_type.model

        # if it doesn't exist..
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            # add it
            Permission.objects.create(content_type=content_type,
                                      codename=codename,
                                      name="Can view %s" % content_type.name)
            print "Added view permission for %s" % content_type.name

class SupplychainConfig(AppConfig):
    name = 'supplychain'
    verbose_name = _("Supply Chain Management")
    def ready(self):
        # check for all our view permissions
#        post_migrate.connect(add_view_permissions)
        pass

