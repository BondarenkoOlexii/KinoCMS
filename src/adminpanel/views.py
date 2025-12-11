from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    return render(request, 'custom_admin/dashboard.html')

@login_required
@user_passes_test(is_admin)
def theme(request):
    return render(request, 'custom_admin/theme.html')