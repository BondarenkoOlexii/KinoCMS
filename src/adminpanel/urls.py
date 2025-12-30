from django.urls import path
from .views import dashboard, theme
from src.news.views import news_stocks, table_news, table_news_delete, update_news
from src.authorization.views import logout_user
urlpatterns = [
    path('', dashboard, name='custom_dashboard'),
    path('theme.html', theme, name='theme'),
    path('news_stocks.html', news_stocks, name='news_stocks'),
    path('table_news_stocks.html', table_news, name='table_news_stocks'),
    path('logout/', logout_user, name='logout'),

    path('delete/<int:pk>', table_news_delete, name='delete_news'),
    path('update/<int:pk>', update_news, name='update_news')
]