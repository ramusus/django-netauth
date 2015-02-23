from django.conf import settings
from django.utils.translation import ugettext as _


ACTIVATION_REQUIRED_TEXT = getattr(settings, "NETAUTH_ACTIVATION_REQUIRED_TEXT", _('To complete registration, check your email and activate your account'))
REGISTRATION_DISABLED = getattr(settings, "NETAUTH_REGISTRATION_DISABLED", _('We are sorry, but registration is disabled. Come back later'))
FILL_OPENID_URL = getattr(settings, "NETAUTH_FILL_OPENID_URL", _('Please fill openid url field'))
OPENID_CANCELED = getattr(settings, "NETAUTH_OPENID_CANCELED", _('You have cancelled OpenID authentication'))
OPENID_FAILED = getattr(settings, "NETAUTH_OPENID_FAILED", _('OpenID authentication failed. Reason: %s'))
SUCCESS_LOGOUT = getattr(settings, "NETAUTH_SUCCESS_LOGOUT", _('You have successfully logged out'))
ACCOUNTS_MERGED = getattr(settings, "NETAUTH_ACCOUNTS_MERGED", _('Your existing account was merged with new authentication account'))
NOT_ACTIVATED = getattr(settings, "NETAUTH_NOT_ACTIVATED",  _('Your account is not activated. Please activate it first.'))
SUCCESSFULLY_AUTHENTICATED = getattr(settings, "NETAUTH_SUCCESSFULLY_AUTHENTICATED", _('You have successfully authenticated'))

OAUTH_INVALID_RESPONSE = getattr(settings,
    "NETAUTH_OAUTH_INVALID_RESPONSE",
    _('Invalid response received from OAuth server, please start the authentication process again')
)

FACEBOOK_INVALID_RESPONSE = getattr(settings,
    "NETAUTH_FACEBOOK_INVALID_RESPONSE",
    _('Invalid response received from Facebook server, please start the authentication process again')
)

INVALID_RESPONSE_FROM_OPENID = getattr(settings,
    "NETAUTH_INVALID_RESPONSE_FROM_OPENID",
    _('Invalid response received from OpenID server, please start the authentication process again')
)

VKONTAKTE_INVALID_RESPONSE = getattr(settings,
    "NETAUTH_VKONTAKTE_INVALID_RESPONSE",
    _('Invalid response received from VKontakte server, please start the authentication process again')
)

TWITTER_INVALID_RESPONSE = getattr(settings,
    "NETAUTH_TWITTER_INVALID_RESPONSE",
    _('Invalid response received from Twitter server, please start the authentication process again')
)

