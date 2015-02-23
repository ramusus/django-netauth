from django.contrib import messages, auth
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from netauth import settings, lang
from netauth.utils import str_to_class, get_backend


def logout(request):
    auth.logout(request)
    messages.success(request, lang.SUCCESS_LOGOUT)
    return redirect(settings.LOGOUT_URL)


def begin(request, provider):
    """
        Display authentication form. This is also the first step
        in registration. The actual login is in social_complete
        function below.
    """
    # store url to where user will be redirected
    request.session['next_url'] = request.GET.get("next") or settings.LOGIN_REDIRECT_URL

    # start the authentication process
    backend = get_backend(provider)
    return backend.begin(request, dict(request.REQUEST.items()))


#redirect_decorator
def complete(request, provider):
    """
        After first step of net authentication, we must validate the response.
        If everything is ok, we must do the following:
        1. If user is already authenticated:
            a. Try to login him again (strange variation but we must take it to account).
            b. Create new netID record in database.
            c. Merge authenticated account with newly created netID record.
            d. Redirect user to 'next' url stored in session.
        2. If user is anonymouse:
            a. Try to log him by identity and redirect to 'next' url.
            b. Create new  netID record in database.
            c. Try to automaticaly fill all extra fields with information returned form
            server. If successfull, login the user and redirect to 'next' url.
            d. Redirect user to extra page where he can fill all extra fields by hand.
    """
    # merge data from POST and GET methods
    data = request.GET.copy()
    data.update(request.POST)

    # In case of skipping begin step.
    if 'next_url' not in request.session:
        request.session['next_url'] = request.GET.get("next") or settings.LOGIN_REDIRECT_URL

    backend = get_backend(provider)
    response = backend.validate(request, data)

    if isinstance(response, HttpResponseRedirect):
        return response
    if request.user.is_authenticated():
        success = backend.login_user(request)
        backend.merge_accounts(request)
    else:
        success = backend.login_user(request)
        if not success and not settings.REGISTRATION_ALLOWED:
            messages.warning(request, lang.REGISTRATION_DISABLED)
            return redirect(settings.REGISTRATION_DISABLED_REDIRECT)
    if success:
        return redirect(request.session.pop('next_url', settings.LOGIN_REDIRECT_URL))
    return backend.complete(request, response)

def extra(request, provider):
    """
        Handle registration of new user with extra data for profile
    """
    identity = request.session.get('identity', None)
    if not identity:
        raise Http404

    if request.method == "POST":
        form = str_to_class(settings.EXTRA_FORM)(request.POST)
        if form.is_valid():
            user = form.save(request, identity, provider)
            del request.session['identity']
            if not settings.ACTIVATION_REQUIRED:
                user = auth.authenticate(identity=identity, provider=provider)
                if user:
                    auth.login(request, user)
                    return redirect(request.session.pop('next_url', settings.LOGIN_REDIRECT_URL))
            else:
                messages.warning(request, lang.ACTIVATION_REQUIRED_TEXT)
                return redirect(settings.ACTIVATION_REDIRECT_URL)
    else:
        initial = request.session['extra']
        form = str_to_class(settings.EXTRA_FORM)(initial=initial)

    return render_to_response('netauth/extra.html', {'form': form }, context_instance=RequestContext(request))
