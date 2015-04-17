from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

from netauth import settings
from netauth.models import NetID


class ExtraForm(forms.Form):

    username = forms.CharField(min_length=3, max_length=25, label="Display Name")

    def clean_username(self):
        try:
            get_user_model().objects.get( username = self.cleaned_data[ 'username' ] )
            raise forms.ValidationError(_(u'This username name is already taken'))
        except get_user_model().DoesNotExist:
            return self.cleaned_data['username']

    def save(self, request, identity, provider):
        user = get_user_model().objects.create(username=self.cleaned_data['username'])
        if settings.ACTIVATION_REQUIRED:
            user.is_active = False
        user.save()
        NetID.objects.get_or_create(identity=identity, provider=provider, defaults={'user': user})
        return user

