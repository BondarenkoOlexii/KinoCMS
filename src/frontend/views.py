from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator

from src.news.models import NewsStockModel, NewsThourghtImage
from src.cinema.models import Cinema, Film, Session, Hall, FilmThourghtImage, CinemaThourghtImage
from src.page.models import Page, PageThourghtImage, Contacts, BannerThourghtImage, Banner
from src.user.models import User
from src.user.forms import UserForm, CustomChangePassword

# Create your views here


def table_cinema_page(request):
    items = Cinema.objects.all()
    image_items = CinemaThourghtImage.objects.all()
    return render(request, 'table_cinema_pages.html', {'items': items, 'image_items': image_items })

def cinema_page(request, pk):
    item = Cinema.objects.get(id=pk)
    image_item = CinemaThourghtImage.objects.filter(images_info=item)
    return render(request, 'cinema_pages.html', {'item':item, 'image_item':image_item})

def pages(request, content_type):
    item = Page.objects.get(type=content_type)
    image_item = PageThourghtImage.objects.filter(images_info=item)

    return render(request, 'pages.html', {'item':item, 'image_item':image_item})

def contact(request):
    items = Contacts.objects.all()
    return render(request, 'contacts.html', {'items':items})



def table_stock_pages(request, content_type):
    items = NewsStockModel.objects.filter(type=content_type)

    items_per_page = 10
    paginator = Paginator(items, items_per_page)

    item_number = request.GET.get('page')
    item_obj = paginator.get_page(item_number)

    current_page_ids = [item.id for item in item_obj]
    image_items = NewsThourghtImage.objects.filter(images_info_id__in=current_page_ids)

    return render(request, 'table_stock_pages.html', {'items': item_obj, 'image_items': image_items, 'type': content_type})

def stock_page(request, pk):
    item = NewsStockModel.objects.get(id=pk)
    image_item = NewsThourghtImage.objects.filter(images_info=item)
    return render(request, 'stocks.html', {'item':item, 'image_item':image_item})

def afisha(request, content_type):
    today = timezone.now().date()
    if content_type == 'afisha':
        afisha_items = Film.objects.filter(start_time__lte=today, end_time__gte=today)
        items_ids = afisha_items.values_list('id', flat=True)
        image_items = FilmThourghtImage.objects.filter(images_info_id__in=afisha_items)
        return render(request, 'afisha.html', {'items':afisha_items, 'image_items':image_items, 'type':content_type})
    elif content_type == 'soon':
        soon_items = Film.objects.filter(start_time__gt=today)
        items_ids = soon_items.values_list('id', flat=True)
        image_items = FilmThourghtImage.objects.filter(images_info_id__in=soon_items)
        return render(request, 'afisha.html', {'items':soon_items, 'image_items':image_items, 'type':content_type})


def film(request, pk):
    item = Film.objects.get(pk=pk)
    image_item = FilmThourghtImage.objects.filter(images_info=item)


    days = Session.objects.values_list('day', flat=True).distinct().order_by('day')
    selected_day = request.GET.get('day')
    items = Session.objects.filter(day=selected_day).order_by('start_time')


    return render(request, 'film_page.html', {'item': item, 'image_item':image_item, 'days': days, 'schedules': items})



@login_required
def profile(request, pk):
    if request.user.id != pk:
        raise PermissionDenied


    password_form = None
    item = get_object_or_404(User,id=pk)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=item)
        password_form = CustomChangePassword(user=item, data=request.POST)
        if form.is_valid() and password_form.is_valid():
            form.save()
            password_form.save()
            update_session_auth_hash(request, item)
            return redirect('profile', pk=item.id)
        else:
            print(f"Ошибка UserForm:\n{form.errors.as_text()}")
    else:
        form = UserForm(instance=item)
        password_form = CustomChangePassword(user=item)

    return render(request, 'user_profile.html', {'item': item, 'form':form, 'password_form': password_form})


def main_page(request):
    today = timezone.now().date()

    afisha_items = Film.objects.filter(start_time__lte=today, end_time__gte=today)
    afisha_items_ids = afisha_items.values_list('id', flat=True)
    afisha_image_items = FilmThourghtImage.objects.filter(images_info_id__in=afisha_items)

    #afisha_image_items_first = afisha_image_items.filter(image_type='gallery')[:1]

    unique_list = {}

    for img in afisha_image_items.filter(image_type='gallery'):
        if img.images_info_id not in unique_list:
            unique_list[img.images_info_id] = img

    afisha_image_items_first = list(unique_list.values())

    soon_items = Film.objects.filter(start_time__gt=today)
    soon_items_ids = soon_items.values_list('id', flat=True)
    soon_image_items = FilmThourghtImage.objects.filter(images_info_id__in=soon_items)

    stock = NewsStockModel.objects.filter(type='stock')
    stock_items_ids = stock.values_list('id', flat=True)
    stock_images = NewsThourghtImage.objects.filter(images_info_id__in=stock_items_ids)


    speed = Banner.objects.first()
    main_banner = BannerThourghtImage.objects.filter(image_type='main').order_by('?').first()


    context = {
               'afisha_items': afisha_items, 'afisha_image_items': afisha_image_items, 'afisha_image_items_first': afisha_image_items_first,
               'soon_items': soon_items, 'soon_image_items': soon_image_items,
               'main_banner': main_banner
               }

    return render(request, 'main.html', context)


def schedule(request):
    all_cinema = Cinema.objects.all()
    all_cinema_hall = Hall.objects.all()
    all_film = Film.objects.all()


    # Фільтри
    items = Session.objects.all().order_by('start_time')

    #day_choosed = Session.objects.values_list('day', flat=True)


    cinema_search_query = request.GET.get('cinema_id')
    hall_search_query = request.GET.get('hall_id')
    film_search_query = request.GET.get('film_id')
    date_search_query = request.GET.get('date_id')
    film_type_search_query = request.GET.get('FilmType')

    if cinema_search_query:
        items = items.filter(hall_id__cinema_id=cinema_search_query)

    if hall_search_query:
        items = items.filter(hall_id=hall_search_query)

    if film_search_query:
        items = items.filter(film_id=film_search_query)

    if date_search_query:
        items = items.filter(day=date_search_query)

    if film_type_search_query:
        items = items.filter(film_id__type=film_type_search_query)

    # Таблиця
    days = Session.objects.values_list('day', flat=True).distinct().order_by('day')


    return render(request, 'schedule.html', {"items":items, 'days': days, 'all_cinema': all_cinema, 'all_cinema_hall': all_cinema_hall, 'all_film': all_film})




def booking(request):

    if request.method == "POST":
        pass
    else:
        film_id = request.GET.get("film")
        hall_id = request.GET.get("hall")
        day_id = request.GET.get("day")
        start_time_id = request.GET.get("time")

        if not all([film_id, hall_id, day_id, start_time_id]):
            print(film_id, hall_id, day_id, start_time_id)
            return redirect('schedule_site')


        #item = Session.objects.filter(film_id=film_id) & Session.objects.filter(hall_id=hall_id) & Session.objects.filter(day=day_id) & Session.objects.filter(start_time=start_time_id)
        item = Session.objects.filter(
            film_id=film_id,
            hall_id=hall_id,
            day=day_id,
            start_time=start_time_id
        ).first()
        film_item = Film.objects.get(id=film_id)
        image_item = FilmThourghtImage.objects.filter(images_info=film_id).first()
        return render(request, 'booking.html', {"item": item, "image_item": image_item, "film_item": film_item})

