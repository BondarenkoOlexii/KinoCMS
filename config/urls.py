"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from src.frontend.views import main_page, table_cinema_page, cinema_page, pages, table_stock_pages, stock_page, afisha, contact, film, profile, schedule, booking

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('adminpanel/', include('src.adminpanel.urls')),
    path('i18n/', include('django.conf.urls.i18n')),

    path('', main_page, name='main_page'),
    path('table_cinema_pages', table_cinema_page, name='table_cinema_page'),
    path('cinema_pages/<int:pk>', cinema_page, name='cinema_pages'),
    path('table_stock_pages/<str:content_type>', table_stock_pages, name='table_stock_pages'),
    path('stocks/<int:pk>', stock_page, name='stocks'),
    path('afisha/<str:content_type>', afisha, name='afisha'),
    path('film_page/<int:pk>', film, name='film_page'),
    path('page/<str:content_type>', pages, name='pages'),
    path('contacts', contact, name='contacts'),
    path('user_profile/<int:pk>', profile, name='user_profile'),
    path('schedule', schedule, name='schedule_site'),
    path('booking/', booking, name='booking')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
