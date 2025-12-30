from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import resolve_url

class AccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        if request.user.is_superuser:
            return resolve_url('/adminpanel/')
        return ('/')