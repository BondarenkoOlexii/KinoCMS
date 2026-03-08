import json
from collections import Counter
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

from src.frontend.views import booking
from src.user.models import User
from src.cinema.models import Cinema, Film, Session, Booking
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


##################################################################
    session_item = Session.objects.distinct('day').order_by('day')
    session_day = [str(item.day) for item in session_item]

    booking_items = Booking.objects.all()

    booking_count = {}
    for item in booking_items:
        key = item.session.day

        if str(key) in booking_count:
            booking_count[str(key)] += 1
        else:
            booking_count[str(key)] = 1

    sorted_booking = []
    for key in session_day:
        if key in booking_count:
            i = booking_count.get(key, 0)
        else:
            i = 0
        sorted_booking.append(i)


    context = {
               'user_items': user_item, 'labels' : list(stats.keys()), 'counts': list(stats.values()),

               'film_items': film_item,'cinema_items': cinema_item, 'page_items': page_item,

                'session_dates':session_day , 'booking_count': sorted_booking
               }

    return render(request, 'custom_admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def theme(request):
    return render(request, 'custom_admin/theme.html')



