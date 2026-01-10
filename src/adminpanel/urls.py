from django.urls import path
from .views import dashboard, theme
from src.news.views import news_stocks, table_news, table_news_delete, update_news
from src.page.views import page, table_page, update_pages, delete_pages
from src.user.views import user, table_user, update_user, delete_user
from src.authorization.views import logout_user
urlpatterns = [
    path('', dashboard, name='custom_dashboard'),
    path('theme.html', theme, name='theme'),
    path('news_stocks.html', news_stocks, name='news_stocks'),
    path('page.html', page, name='pages'),
    path('admin_users.html', user, name='admin_users'),

    path('table_news_stocks.html', table_news, name='table_news_stocks'),
    path('table_pages.html', table_page, name='table_page'),
    path('table_user.html', table_user, name='table_user'),

    path('logout/', logout_user, name='logout'),

    path('delete/<int:pk>', table_news_delete, name='delete_news'),
    path('delete/<int:pk>', delete_pages, name='delete_page'),
    path('admin_users/delete/<int:pk>', delete_user, name='delete_user'),

    path('update/<int:pk>', update_news, name='update_news'),
    path('update/<int:pk>', update_pages, name='update_pages'),
    path('admin_users/update/<int:pk>', update_user, name='update_user')
]