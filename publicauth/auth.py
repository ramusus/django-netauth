from django.contrib.auth.models import User
from publicauth.models import PublicID


class PublicBackend(object):
    """ Add this Authentication Backend to
        AUTHENTICATION_BACKENDS tuple in your settings.py
    """
    supports_object_permissions = False
    supports_anonymous_user = True

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, identity=None, provider=None):
        """ Authenticate user by public identity.
        """
        if identity:
            try:
                user = PublicID.objects.get(identity=identity, provider=provider).user
                return user
            except PublicID.DoesNotExist:
                return None
        else:
            return None

