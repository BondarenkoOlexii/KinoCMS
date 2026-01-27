from collections import Counter
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from src.user.models import User
from src.cinema.models import Cinema, Film
from src.page.models import Page


def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='Admin').exists())


@login_required
@user_passes_test(is_admin)
def dashboard(request):
    users = User.objects.all()
    user_item = users.count()

    user_sex_list = [item.sex for item in User.objects.all()]

    stats = Counter(user_sex_list)

    film_item = Film.objects.all().count()
    cinema_item = Cinema.objects.all().count()
    page_item = Page.objects.all().count()

    context = {
               'user_items': user_item, 'labels' : list(stats.keys()), 'counts': list(stats.values()),

               'film_items': film_item,'cinema_items': cinema_item, 'page_items': page_item
               }

    return render(request, 'custom_admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def theme(request):
    return render(request, 'custom_admin/theme.html')



