from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import translation

@receiver(user_logged_in)
def set_language(sender, request, user, **kwargs):
    if hasattr(user, 'language'):
        request.session['_language'] = user.language
        translation.activate(user.language)