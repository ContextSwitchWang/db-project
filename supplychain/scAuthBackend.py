from django.conf import settings
from django.contrib.auth.models import User

class GuestBackend(object):
    """
    add guest account, that is, an account that doesn't have
    to check password
    """

    def authenticate(self, username=None, password=None):
        if username == settings.GUEST_LOGIN:
            try:
                user = User.objects.get(username=username)
                return user
            except User.DoesNotExist:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None