from django.urls import path
from .views import dashboard, theme

urlpatterns = [
    path('', dashboard, name='custom_dashboard'),
    path('theme.html', theme, name='theme')
]