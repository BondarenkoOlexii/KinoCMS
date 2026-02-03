from django.urls import path
from .views import dashboard, theme
from src.news.views import news_stocks, table_news, table_news_delete, update_news
from src.page.views import page, banner, table_page, update_pages, delete_pages, update_main_page
from src.user.views import user, table_user, update_user, delete_user, distribution, choise_users, delete_file, progress_view
from src.cinema.views import film, cinema, hall, table_film, table_cinema, update_film, update_cinema, update_hall, delete_film, delete_cinema, delete_hall
from src.authorization.views import logout_user


urlpatterns = [
    path('', dashboard, name='custom_dashboard'),
    path('theme.html', theme, name='theme'),
    path('news_stocks.html', news_stocks, name='news_stocks'),
    path('page.html', page, name='pages'),
    path('admin_users.html', user, name='admin_users'),
    path('film.html', film, name='film'),
    path('banner.html', banner, name='banner'),
    path('cinema.html', cinema, name='cinema'),
    path('cinema/hall.html/<int:cinema_id>', hall, name='hall'),
    path('distribution.html', distribution, name='distribution'),
    path('choise_users.html', choise_users, name='choise_users'),
    path('progress_view/<str:task_id>/', progress_view, name='progress_view'),

    path('table_news_stocks.html', table_news, name='table_news_stocks'),
    path('table_pages.html', table_page, name='table_pages'),
    path('table_user.html', table_user, name='table_user'),
    path('table_film.html', table_film, name='table_film'),
    path('table_cinema.html', table_cinema, name='table_cinema'),

    path('logout/', logout_user, name='logout'),

    path('delete/<int:pk>', table_news_delete, name='delete_news'),
    path('page/delete/<int:pk>', delete_pages, name='delete_page'),
    path('admin_users/delete/<int:pk>', delete_user, name='delete_user'),
    path('film/delete/<int:pk>', delete_film, name='delete_film'),
    path('cinema/update/<int:cinema_pk>/hall/delete/<int:hall_pk>', delete_hall, name='delete_hall'),
    path('cinema/delete/<int:pk>', delete_cinema, name='delete_cinema'),
    path('distribution/delete/<str:filename>/', delete_file, name='delete_file'),


    path('update/<int:pk>', update_news, name='update_news'),
    path('page/update/<int:pk>', update_pages, name='update_pages'),
    path('main_page/update/<int:pk>', update_main_page, name='update_main_page'),
    path('admin_users/update/<int:pk>', update_user, name='update_user'),
    path('film/update/<int:pk>', update_film, name='update_film'),
    path('cinema/update/<int:cinema_pk>/hall/update/<int:hall_pk>', update_hall, name='update_hall'),
    path('cinema/update/<int:pk>', update_cinema, name='update_cinema')

]